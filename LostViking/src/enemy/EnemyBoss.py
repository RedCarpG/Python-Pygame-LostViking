import random
from enum import Enum
from abc import ABC, abstractmethod
from ..generic_items.BasicPlaneEntity import BasicPlaneEntity
from ..groups import BOSS_G
from ..constants import SCREEN_WIDTH


class BossActionPhase(Enum):
    MoveDown = 0
    Idle = 1
    MoveX = 2


class BossAttackPhase(Enum):
    Idle = 0
    Attack = 1


class EnemyBoss(BasicPlaneEntity, ABC):
    MAX_HEALTH = 30000
    SCORE = 5000

    _STAY_DURATION = 200
    _MOVE_X_DURATION = 200
    _ATTACK_SPEED = 100

    def __init__(self, **kwargs):
        BasicPlaneEntity.__init__(self, **kwargs)
        self.add(BOSS_G)

        self.action_status = BossActionPhase.MoveDown
        self.attack_status = BossAttackPhase.Idle

        self._speed_y = self.MAX_SPEED_DOWN
        self._move_x_direction = None

        self._count_action_idle = self._STAY_DURATION
        self._count_action_move_x = self._MOVE_X_DURATION
        self._count_attack_interval = self._ATTACK_SPEED

        self.set_pos([SCREEN_WIDTH // 2, -self.rect.height])

    # -------------------- Main action states --------------------
    def _action_phase(self):
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

    # -------------------- Sub action states --------------------
    def enter_action_move_down_phase(self):
        self.action_status = BossActionPhase.MoveDown

    def _action_move_down(self):
        self._move()
        if self.rect.top > 0:
            self._deceleration_y()
            if self._speed_y == 0:
                self.enter_action_idle_phase()

    def enter_action_idle_phase(self):
        self._count_action_idle = self._STAY_DURATION
        self.action_status = BossActionPhase.Idle

    def _action_idle(self):
        if self._count_action_idle <= 0:
            self.enter_action_move_x_phase()
        else:
            self._count_action_idle -= 1

    def enter_action_move_x_phase(self):
        self.action_status = BossActionPhase.MoveX
        self._count_action_move_x = self._MOVE_X_DURATION
        self._move_x_direction = random.choice([1, -1])

    def _action_move_x(self):
        self._move()
        if not self._count_action_move_x:
            # Decelerate in X direction and enter idle phase
            self._deceleration_x()
            if self._speed_x == 0:
                self.enter_action_idle_phase()
        else:
            # Accelerate (if not max) and count down
            if self._move_x_direction == -1:
                self._accelerate_left()
            else:
                self._accelerate_right()
            self._count_action_move_x -= 1

    # -------------------- Attack States --------------------
    def enter_attack_phase(self):
        self.attack_status = BossAttackPhase.Attack

    @abstractmethod
    def _action_attack(self, *args, **kwargs):
        pass

    def enter_attack_idle_phase(self):
        self.attack_status = BossAttackPhase.Idle
        self._count_attack_interval = self._ATTACK_SPEED

    def _action_attack_idle(self):
        if self._count_attack_interval <= 0:
            self.enter_attack_phase()
        else:
            self._count_attack_interval -= 1

    # -------------------- Behaviors --------------------
    def _move(self) -> None:
        super()._move()
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self._move_x_direction = -self._move_x_direction
            self._speed_x = -self._speed_x

    # -------------------- Interface --------------------
    def get_health(self):
        return self._health

    # -------------------- Init --------------------
    @classmethod
    def _init_attributes(cls) -> None:
        cls.MAX_SPEED_X = 1
        cls.MAX_SPEED_DOWN = cls.MAX_SPEED_UP = 2
        cls.ACC_X = 0.1
        cls.ACC_DOWN = cls.ACC_UP = 0.2
        cls.MAX_HEALTH = 30000
        cls.SCORE = 5000
        cls._IS_SET_ATTRS = True

