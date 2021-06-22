""" This file includes:
    -> PlayerNucBomb class which creates a bomb entity
    -> NucExplosion class which handles with the drawing of explosion image"""
from pygame.sprite import Sprite
from ..constants import SCREEN_HEIGHT
from ..generic_loader.image_loader import load_image
from ..generic_loader.sound_loader import load_sound, play_sound
from ..constants import MAIN_VOLUME
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
        play_sound("NUC_LAUNCH")

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
            play_sound("NUC_EXPLODE")
            self.kill()
            del self

    def _move(self) -> None:
        self.rect.top -= self.speed
        self.speed += self.accelerate

    @classmethod
    def launch(cls, player_position) -> None:
        if cls._Is_Already_Activate or get_nuc_count() < 0:
            pass
            play_sound("NUC_ERROR")
        else:
            from .player_interface import dec_nuc_bomb
            dec_nuc_bomb()
            cls._Is_Already_Activate = True
            PlayerNucBomb(player_position)

    @classmethod
    def _init_image(cls) -> None:
        cls.IMAGE = load_image("PlayerPlane/bullet.png")
        cls._IS_SET_IMAGE = True

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
