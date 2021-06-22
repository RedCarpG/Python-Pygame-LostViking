from .Enemy_Scout import EnemyScout
from .Enemy_Phoenix import EnemyPhoenix, BulletPhoenix, ShieldPhoenix
from .Enemy_Carrier import EnemyCarrier
from .Enemy_Interceptor import EnemyInterceptor
from .level1_group import *


def init_level():
    EnemyScout.init()

    EnemyPhoenix.init()
    BulletPhoenix.init()
    ShieldPhoenix.init()

    EnemyCarrier.init()

    EnemyInterceptor.init()

    # Init sound
    from ..generic_loader.sound_loader import load_sound
    from ..constants import MAIN_VOLUME
    load_sound("Explo.wav", MAIN_VOLUME - 0.4, "EXPLODE")
    load_sound("Explo2.wav", MAIN_VOLUME - 0.2, "EXPLODE2")

    load_sound("Shield.wav", MAIN_VOLUME - 0.3, "SHIELD")
    load_sound("Laser.wav", MAIN_VOLUME - 0.2, "LASER")

def end_level():
    del EnemyScout
    del EnemyPhoenix
    del BulletPhoenix
    del ShieldPhoenix
    del EnemyCarrier
    del EnemyInterceptor

    del Enemy_Scout_G
    del Enemy_Phoenix_G
    del Enemy_Interceptor_G
