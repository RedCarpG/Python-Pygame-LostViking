from .generic_loader.sound_loader import *
from .generic_loader.image_loader import *
from enum import Enum

PLAYER_IMAGE = {}


# 主音量
MAIN_VOLUME = 0.5
# 背景卷动速度
BG_SPEED = 25


# Screen
class SCREEN(object):
    _SIZE = _WIDTH, _HEIGHT = (1000, 800)

    @classmethod
    def change_screen_size(cls, width, height):
        SCREEN._SIZE = (width, height)
        SCREEN._WIDTH = width
        SCREEN._HEIGHT = height

    @classmethod
    def get_h(cls):
        return SCREEN._HEIGHT

    @classmethod
    def get_w(cls):
        return SCREEN._WIDTH

    @classmethod
    def get_s(cls):
        return SCREEN._SIZE


class G(object):
    SCORE = 0
    LIFE = 3
    BOMB = 3


class RESOURCES(object):
    SOUNDS = {}
    IMAGES = {}
    PHOENIX_IMAGE = {}
    # SCOUT_IMAGE = {}
    BULLET_IMAGE = {}
    VIKING_IMAGE = {}
    SUPPLY_IMAGE = {}
    CARRIER_IMAGE = {}
    INTERCEPTOR_IMAGE = {}

    @classmethod
    def load_viking_image(cls):
        pass

    @classmethod
    def global_load_image(cls):
        # Load Images
        RESOURCES.BULLET_IMAGE.clear()
        RESOURCES.VIKING_IMAGE.clear()
        RESOURCES.SUPPLY_IMAGE.clear()

        RESOURCES.load_viking_image()
        RESOURCES.SUPPLY_IMAGE.setdefault("Life", _load_image_alpha("Supply/bullet.png"))
        RESOURCES.SUPPLY_IMAGE.setdefault("Bomb", _load_image_alpha("Supply/bomb.png"))
        RESOURCES.SUPPLY_IMAGE.setdefault("Bullet", _load_image_alpha("Supply/bullet.png"))
        RESOURCES.BULLET_IMAGE.setdefault("Viking_Bullet", _load_image_alpha("PlayerPlane/bullet.png"))

    @classmethod
    def global_load_image_level1(cls):
        RESOURCES.PHOENIX_IMAGE.clear()
        RESOURCES.CARRIER_IMAGE.clear()
        RESOURCES.INTERCEPTOR_IMAGE.clear()

        RESOURCES.BULLET_IMAGE.setdefault("Phoenix_Bullet", _load_image_alpha("BasicEnemy/bullet.png"))
        RESOURCES.BULLET_IMAGE.setdefault("Phoenix_Laser", _load_image_alpha("BasicEnemy/laser.png"))
        RESOURCES.PHOENIX_IMAGE.setdefault("Normal", [_load_image_alpha("BasicEnemy\Enemy_Phoenix1.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix2.png")])
        RESOURCES.PHOENIX_IMAGE.setdefault("Stop", [_load_image_alpha("BasicEnemy\Enemy_Phoenix_Stop1.png"),
                                                    _load_image_alpha("BasicEnemy\Enemy_Phoenix_Stop2.png")])
        RESOURCES.PHOENIX_IMAGE.setdefault("Shield", [_load_image_alpha("BasicEnemy\Sheild1.png"),
                                                      _load_image_alpha("BasicEnemy\Sheild2.png"),
                                                      _load_image_alpha("BasicEnemy\Sheild3.png"),
                                                      _load_image_alpha("BasicEnemy\Sheild4.png"),
                                                      _load_image_alpha("BasicEnemy\Sheild5.png")])
        RESOURCES.PHOENIX_IMAGE.setdefault("Destroy", [_load_image_alpha("BasicEnemy\Destroy_Phoenix1.png"),
                                                       _load_image_alpha("BasicEnemy\Destroy_Phoenix2.png"),
                                                       _load_image_alpha("BasicEnemy\Destroy_Phoenix3.png"),
                                                       _load_image_alpha("BasicEnemy\Destroy_Phoenix4.png"),
                                                       _load_image_alpha("BasicEnemy\Destroy_Phoenix5.png"),
                                                       _load_image_alpha("BasicEnemy\Destroy_Phoenix6.png")])
        RESOURCES.PHOENIX_IMAGE.setdefault("Attack", [_load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight1.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight2.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight3.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight4.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight5.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight6.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight7.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight8.png"),
                                                      _load_image_alpha("BasicEnemy\Enemy_Phoenix_AttakLight9.png")])
        RESOURCES.INTERCEPTOR_IMAGE.setdefault("Body", _load_image_alpha("BasicEnemy\Interceptor.png"))
        RESOURCES.CARRIER_IMAGE.setdefault("Body", _load_image_alpha("BasicEnemy\Carrier.png"))

    @classmethod
    def UNLOAD_IMAGE_LEVER1(cls):
        RESOURCES.PHOENIX_IMAGE.clear()
        # RESOURCES.SCOUT_IMAGE.clear()
        RESOURCES.CARRIER_IMAGE.clear()
        RESOURCES.INTERCEPTOR_IMAGE.clear()

    @classmethod
    def LOAD_SOUNDS(cls):
        # 加载音效
        RESOURCES.SOUNDS.clear()
        RESOURCES.SOUNDS.setdefault("Shield", _load_sound("Shield.wav", MAIN_VOLUME - 0.3))
        RESOURCES.SOUNDS.setdefault("Player_Shoot", _load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
        RESOURCES.SOUNDS.setdefault("Laser", _load_sound("Laser.wav", MAIN_VOLUME - 0.2))
        RESOURCES.SOUNDS.setdefault("NucExplosion", [_load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                                  _load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])
        RESOURCES.SOUNDS.setdefault("Player_Explo", _load_sound("Player_Explo.wav", MAIN_VOLUME))
        RESOURCES.SOUNDS.setdefault("NuclearLaunch_Detected",
                                    _load_sound("NuclearLaunch_Detected.wav", MAIN_VOLUME - 0.1))
        RESOURCES.SOUNDS.setdefault("NuclearMissle_Ready", _load_sound("NuclearMissile_Ready.wav", MAIN_VOLUME - 0.1))
        RESOURCES.SOUNDS.setdefault("UI1", _load_sound("UI1.wav", MAIN_VOLUME - 0.2))
        RESOURCES.SOUNDS.setdefault("Liftoff1", _load_sound("Liftoff1.wav", MAIN_VOLUME))
        RESOURCES.SOUNDS.setdefault("Liftoff2", _load_sound("Liftoff2.wav", MAIN_VOLUME - 0.2))
        RESOURCES.SOUNDS.setdefault("Error", _load_sound("Error.wav", MAIN_VOLUME))
