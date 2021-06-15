from .Scout import EnemyScout
from .Phoenix import EnemyPhoenix, BulletPhoenix, Shield
from .level1_event_type import *
from .level1_event_handler import *
from .level1_group import *


def level1_init():
    EnemyScout.init()
    EnemyPhoenix.init()
    BulletPhoenix.init()
    Shield.init()
