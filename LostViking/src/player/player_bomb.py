""" This file includes:
    -> PlayerNucBomb class which creates a bomb entity
    -> Explosion class which handles with the drawing of explosion image"""

from ..generic_items.graphic_helper import SingleImageHelper
from ..constants import SCREEN
from ..generic_loader.image_loader import load_image
from ..generic_items.graphic_helper import LoopImageHelper
from ..groups import Player_NucBomb_G, NucBomb_Explosion_G
from .player_interface import get_nuc_count
import pygame


class PlayerNucBomb(SingleImageHelper, pygame.sprite.Sprite):
    """ Player Nuclear Bomb
    -> Implements StraightBullet class :
            -> SingleImageHelper
            -> pygame.sprite.Sprite
    """
    _Is_Already_Activate = False

    _SOUND = {}

    def __init__(self, init_position: (list, tuple)):
        SingleImageHelper.__init__(self)
        pygame.sprite.Sprite.__init__(self, Player_NucBomb_G)

        self.rect = self.image.get_rect()
        self.rect.center = init_position

        self.accelerate = 0.2
        self.speed = -2

        self.explode_flag = False

    def update(self) -> None:
        if self.rect.bottom > SCREEN.get_h() // 3:
            self._move()
        else:
            Explosion(self.rect.center)
            PlayerNucBomb._Is_Already_Activate = False
            self.kill()
            self._SOUND["Explode"].stop()
            self._SOUND["Explode"].play()

    def _move(self) -> None:
        self.rect.top -= self.speed
        self.speed += self.accelerate

    @classmethod
    def launch(cls, player_position) -> None:
        if cls._Is_Already_Activate or get_nuc_count() < 0:
            cls._SOUND["Error"].stop()
            cls._SOUND["Error"].play()
        else:
            from .player_interface import dec_nuc_bomb
            dec_nuc_bomb()
            cls._Is_Already_Activate = True
            cls._SOUND["NuclearLaunch_Detected"].stop()
            cls._SOUND["NuclearLaunch_Detected"].play()
            PlayerNucBomb(player_position)

    @classmethod
    def init_image(cls) -> None:
        cls._IMAGE = load_image("MyPlane/bullet.png")

        cls._INIT_FLAG_IMAGE = True

    @classmethod
    def init_sound(cls) -> None:
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("NuclearLaunch_Detected",
                              load_sound("NuclearLaunch_Detected.wav",
                                         MAIN_VOLUME - 0.1))
        cls._SOUND.setdefault("Error", load_sound("Error.wav", MAIN_VOLUME))
        # TODO Sound here
        cls._SOUND.setdefault("Explode", load_sound("Player_Explo.wav", MAIN_VOLUME))


class Explosion(LoopImageHelper, pygame.sprite.Sprite):

    def __init__(self, init_position):
        pygame.sprite.Sprite.__init__(self, NucBomb_Explosion_G)
        LoopImageHelper.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.center = init_position

    def update(self) -> None:
        if self._image_switch == len(self._main_image_type) - 1:
            self.kill()
        self._switch_image()

    @classmethod
    def init_image(cls) -> None:
        # TODO Image here
        cls._IMAGE["Base"] = [load_image("MyPlane/MyPlane_explode1.png"),
                              load_image("MyPlane/MyPlane_explode2.png"),
                              load_image("MyPlane/MyPlane_explode3.png"),
                              load_image("MyPlane/MyPlane_explode4.png"),
                              load_image("MyPlane/MyPlane_explode5.png"),
                              load_image("MyPlane/MyPlane_explode6.png")]

        cls._INIT_FLAG_IMAGE = True


def init_bomb():
    PlayerNucBomb.init_image()
    PlayerNucBomb.init_sound()
    Explosion.init_image()