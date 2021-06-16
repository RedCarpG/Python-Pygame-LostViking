from abc import ABC, abstractmethod
from .enemyPlane import BasicEnemy
from ..generic_items.MovementHelper import InertialMoveHelper
from ..constants import SCREEN


class EnemyBoss(BasicEnemy, InertialMoveHelper, ABC):
    _Score = 5000
    _MAX_HEALTH = 30000

    def __init__(self):
        BasicEnemy.__init__(self)
        InertialMoveHelper.__init__(self)

        self.set_pos([SCREEN.get_w() // 2, -self.rect.height])

    @classmethod
    def _init_speed(cls):
        if not hasattr(cls, "_INIT_FLAG_SPEED") or not cls._INIT_FLAG_SPEED:
            cls._MAX_SPEED_R = cls._MAX_SPEED_L = 10
            cls._MAX_SPEED_DOWN = cls._MAX_SPEED_UP = 2
            cls._INIT_FLAG_SPEED = True

    @classmethod
    def _init_acc(cls):
        if not hasattr(cls, "_INIT_FLAG_ACC") or not cls._INIT_FLAG_ACC:
            cls._ACC_L = cls._ACC_R = 0.1
            cls._ACC_DOWN = cls._ACC_UP = 0.1
            cls._INIT_FLAG_ACC = True

    @abstractmethod
    def _action(self):
        pass

    @classmethod
    def init(cls):
        if not hasattr(cls, "_INIT_FLAG") or not cls._INIT_FLAG:
            cls._init_speed()
            cls._init_acc()
            cls._INIT_FLAG = True
