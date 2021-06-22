""" This file includes:
    -> PlayerNucBomb class which creates a bomb entity
    -> NucExplosion class which handles with the drawing of explosion image"""
from pygame.sprite import Sprite
from ..constants import SCREEN_HEIGHT
from ..generic_loader.image_loader import load_image
from ..groups import Player_NucBomb_G
from ..generic_items.BasicExplosion import BasicExplosion
from .player_interface import get_nuc_count


class PlayerNucBomb(Sprite):
    """ Player Nuclear Bomb
    -> Implements StraightBullet class :
            -> SingleImageHelper
            -> pygame.sprite.Sprite
    """
    IMAGE = None
    _Is_Already_Activate = False

    def __init__(self, init_position: (list, tuple)):
        if not hasattr(self, "INIT_FLAG") or not self.INIT_FLAG:
            raise Exception("!!!ERROR: class is not init! {}".format(self))
        Sprite.__init__(self, Player_NucBomb_G)
        # self._play_sound("NuclearMissile_Ready")

        # Set Image properties
        self.image = self.IMAGE
        # Set Rect & Position
        self.rect = self.image.get_rect()
        self.rect.center = init_position

        # Set Attributes
        self.accelerate = 0.2
        self.speed = -2

        self.explode_flag = False

    def update(self) -> None:
        if self.rect.bottom > SCREEN_HEIGHT // 3:
            self._move()
        else:
            NucExplosion(self.rect.center)
            PlayerNucBomb._Is_Already_Activate = False
            # self._play_sound("Explode")
            self.kill()
            del self

    def _move(self) -> None:
        self.rect.top -= self.speed
        self.speed += self.accelerate

    @classmethod
    def launch(cls, player_position) -> None:
        if cls._Is_Already_Activate or get_nuc_count() < 0:
            pass
            # cls._play_sound("Error")
        else:
            from .player_interface import dec_nuc_bomb
            dec_nuc_bomb()
            cls._Is_Already_Activate = True
            PlayerNucBomb(player_position)

    @classmethod
    def _init_image(cls) -> None:
        cls.IMAGE = load_image("PlayerPlane/bullet.png")
        cls._IS_SET_IMAGE = True

    # TODO Sound
    @classmethod
    def _init_sound(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG_SOUND") or not cls._INIT_FLAG_SOUND:
            cls._SOUND = dict()
            from LostViking.src.generic_loader.sound_loader import load_sound
            from LostViking.src.constants import MAIN_VOLUME
            cls._SOUND.setdefault("NuclearLaunch_Detected",
                                  load_sound("NuclearLaunch_Detected.wav",
                                             MAIN_VOLUME - 0.1))
            cls._SOUND.setdefault("NuclearMissile_Ready", load_sound("NuclearMissile_Ready.wav", MAIN_VOLUME - 0.1))
            cls._SOUND.setdefault("Error", load_sound("Error.wav", MAIN_VOLUME))
            # TODO Sound here
            cls._SOUND.setdefault("Explode", load_sound("Player_Explo.wav", MAIN_VOLUME))
            cls._INIT_FLAG_SOUND = True

    @classmethod
    def init(cls):
        if not hasattr(cls, "INIT_FLAG") or not cls.INIT_FLAG:
            cls._init_image()
            cls.INIT_FLAG = True


class NucExplosion(BasicExplosion):

    def __init__(self, init_position):
        BasicExplosion.__init__(self, init_position=init_position)

    @classmethod
    def _init_image(cls) -> None:
        cls.IMAGE = dict()
        # TODO Image here
        cls.IMAGE["BASE"] = [load_image("PlayerPlane/PlayerPlane_explode1.png"),
                             load_image("PlayerPlane/PlayerPlane_explode2.png"),
                             load_image("PlayerPlane/PlayerPlane_explode3.png"),
                             load_image("PlayerPlane/PlayerPlane_explode4.png"),
                             load_image("PlayerPlane/PlayerPlane_explode5.png"),
                             load_image("PlayerPlane/PlayerPlane_explode6.png")]

        cls._IS_SET_IMAGE = True
