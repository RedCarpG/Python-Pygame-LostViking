from .Enemy_Scout import EnemyScout
from .Enemy_Phoenix import EnemyPhoenix, BulletPhoenix, Shield
from .Enemy_Carrier import EnemyCarrier
from .Enemy_Interceptor import EnemyInterceptor
from .level1_event_type import EVENT_CREATE_SCOUT, EVENT_CREATE_CARRIER, EVENT_CREATE_PHOENIX
from .level1_event_handler import level1_events_handler, level1_event_config
from .level1_group import *


def level1_init():
    EnemyScout.init()

    EnemyPhoenix.init()
    BulletPhoenix.init()
    Shield.init()

    EnemyCarrier.init()

    EnemyInterceptor.init()


def level1_del():
    del EnemyScout
    del EnemyPhoenix
    del BulletPhoenix
    del Shield
    del EnemyCarrier
    del EnemyInterceptor

    del Enemy_Scout_G
    del Enemy_Phoenix_G
    del Enemy_Interceptor_G


