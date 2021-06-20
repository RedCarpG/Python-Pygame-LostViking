from .Enemy_Scout import EnemyScout
from .Enemy_Phoenix import EnemyPhoenix, BulletPhoenix, ShieldPhoenix
from .Enemy_Carrier import EnemyCarrier
from .Enemy_Interceptor import EnemyInterceptor
from .level1_group import *


def level1_init():
    EnemyScout.init()

    EnemyPhoenix.init()
    BulletPhoenix.init()
    ShieldPhoenix.init()

    EnemyCarrier.init()

    EnemyInterceptor.init()


def level1_del():
    del EnemyScout
    del EnemyPhoenix
    del BulletPhoenix
    del ShieldPhoenix
    del EnemyCarrier
    del EnemyInterceptor

    del Enemy_Scout_G
    del Enemy_Phoenix_G
    del Enemy_Interceptor_G