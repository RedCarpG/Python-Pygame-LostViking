import random
from enum import Enum
from abc import ABC, abstractmethod
from .EnemyIII import BasicEnemy
from ..generic_items.MovementHelper import InertialMoveHelper
from ..constants import SCREEN


class BossActionPhase(Enum):
    MoveDown = 0
    Idle = 1
    MoveX = 2


class BossAttackPhase(Enum):
    Idle = 0
    Attack = 1


class EnemyBoss(BasicEnemy, InertialMoveHelper, ABC):
    SCORE = 5000
    MAX_HEALTH = 30000

    _STAY_DURATION = 200
    _MOVE_X_DURATION = 200
    _ATTACK_INTERVAL = 100

    def __init__(self):
        BasicEnemy.__init__(self)
        InertialMoveHelper.__init__(self)

        self.action_status = BossActionPhase.MoveDown
        self.attack_status = BossAttackPhase.Idle

        self._speed_y = self._MAX_SPEED_DOWN
        self._move_x_direction = None

        self._count_action_idle = self._STAY_DURATION
        self._count_action_move_x = self._MOVE_X_DURATION
        self._count_attack_interval = self._ATTACK_INTERVAL

        self.set_pos([SCREEN.get_w() // 2, -self.rect.height])

    def enter_action_idle_phase(self):
        self._count_action_idle = self._STAY_DURATION
        self.action_status = BossActionPhase.Idle

    def _action_idle(self):
        if self._count_action_idle <= 0:
            self.enter_action_move_x_phase()
        else:
            self._count_action_idle -= 1

    def enter_action_move_down_phase(self):
        self.action_status = BossActionPhase.MoveDown

    def _action_move_down(self):
        if self.rect.top < 0:
            if self.rect.bottom > 0:
                self._inertial_deceleration()
                if self._speed_y == 0:
                    self.enter_action_idle_phase()
            self._move()
        else:
            self.enter_action_idle_phase()

    def enter_action_move_x_phase(self):
        self.action_status = BossActionPhase.MoveX
        self._count_action_move_x = self._MOVE_X_DURATION
        self._move_x_direction = random.choice([1, -1])

    def _action_move_x(self):
        self._move()
        if self._move_x_direction == -1:
            self._accelerate_left()
        else:
            self._accelerate_right()
        if self._count_action_idle <= 0:
            self._move_flag_x = False
            self._move_flag_y = False
            self._inertial_deceleration()
            if self._speed_x == 0:
                self.enter_action_idle_phase()
        else:
            self._count_action_move_x -= 1

    def enter_attack_phase(self):
        self.attack_status = BossAttackPhase.Attack

    @abstractmethod
    def _action_attack(self, *args, **kwargs):
        pass

    def enter_attack_idle_phase(self):
        self.attack_status = BossAttackPhase.Idle
        self._count_attack_interval = self._ATTACK_INTERVAL

    def _action_attack_idle(self):
        if self._count_attack_interval <= 0:
            self.enter_attack_phase()
        else:
            self._count_attack_interval -= 1

    def _action(self):
        if self.action_status == BossActionPhase.MoveDown:
            self._action_move_down()
        else:
            if self.action_status == BossActionPhase.MoveX:
                self._action_move_x()
            else:
                self._action_idle()
            if self.attack_status == BossAttackPhase.Attack:
                self._action_attack()
            else:
                self._action_attack_idle()

    def _move(self) -> None:
        super()._move()
        if self.rect.left < 0 or self.rect.right > SCREEN.get_w():
            self.speed = -self.speed

    @classmethod
    def _init_speed(cls):
        if not hasattr(cls, "_INIT_FLAG_SPEED") or not cls._INIT_FLAG_SPEED:
            cls._MAX_SPEED_R = cls._MAX_SPEED_L = 2
            cls._MAX_SPEED_DOWN = cls._MAX_SPEED_UP = 2
            cls._INIT_FLAG_SPEED = True

    @classmethod
    def _init_acc(cls):
        if not hasattr(cls, "_INIT_FLAG_ACC") or not cls._INIT_FLAG_ACC:
            cls._ACC_L = cls._ACC_R = 0.1
            cls._ACC_DOWN = cls._ACC_UP = 0.1
            cls._INIT_FLAG_ACC = True

    @classmethod
    def init(cls):
        if not hasattr(cls, "_INIT_FLAG") or not cls._INIT_FLAG:
            cls._init_speed()
            cls._init_acc()
            cls._INIT_FLAG = True
