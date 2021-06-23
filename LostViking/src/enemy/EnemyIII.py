"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import abstractmethod, ABC
from enum import Enum
from ..constants import SCREEN_HEIGHT, SCREEN_WIDTH
from ..generic_items.BasicPlaneEntity import BasicSpinPlaneEntity
from ..generic_items.inertial_behavior import decelerate
from ..groups import Enemy_G


class EnemyIIIActionPhase(Enum):
    Entrance = 0
    Stay = 1
    Leave = 2


class EnemyIIIAttackPhase(Enum):
    Idle = 0
    Attack = 1


class EnemyIIISide(Enum):
    Left = 1
    Right = -1


class EnemyIII(BasicSpinPlaneEntity, ABC):
    SCORE = 500

    _STAY_DURATION = 500
    _ATTACK_SPEED = 100

    def __init__(self, position, side='L', **kwargs):
        BasicSpinPlaneEntity.__init__(self, start_point=position, **kwargs)
        self.add(Enemy_G)

        self.action_status = EnemyIIIActionPhase.Entrance
        self.attack_status = EnemyIIIAttackPhase.Idle

        self._count_action_stay = self._STAY_DURATION

        self._count_attack_interval = self._ATTACK_SPEED

        if side == 'L':
            self.side = EnemyIIISide.Left
        else:
            self.side = EnemyIIISide.Right

        self.enter_action_entrance_phase()

    # --------------- Override Methods --------------- #
    def update(self, *args, **kwargs) -> None:
        super().update(self, *args, **kwargs)
        self._rotate_image()

    def aim(self, point):
        angle = self.cal_angle(self.rect.center, point)

        if self.rect.center[0] > point[0] and self.angle > 90:
            self.angle += 2
        elif self.rect.center[0] < point[0] and self.angle < -90:
            self.angle -= 2
        elif self.angle > angle:
            self.angle -= 2
        elif self.angle < angle:
            self.angle += 2

        if self.angle < -180:
            self.angle = 180
        if self.angle > 180:
            self.angle = -180

    # --------------- Main action status --------------- #
    def _action_phase(self, *args, **kwargs):
        if self.action_status == EnemyIIIActionPhase.Entrance:
            self._action_entrance()
        else:
            if self.action_status == EnemyIIIActionPhase.Stay:
                self._action_stay()
            else:
                self._action_leave()

            if self.attack_status == EnemyIIIAttackPhase.Attack:
                self._action_attack(*args, **kwargs)
            else:
                self._action_attack_idle()

            from ..groups import Player1_G
            player_point = Player1_G.sprites()[0].rect.center
            self.aim(player_point)

    # --------------- Sub action status --------------- #
    def enter_action_entrance_phase(self):
        if self.side == EnemyIIISide.Left:
            self._speed_x = self.MAX_SPEED_X
            self.angle = 90
        else:
            self._speed_x = -self.MAX_SPEED_X
            self.angle = -90

        self._speed_y = 0
        self.action_status = EnemyIIIActionPhase.Entrance

    def _action_entrance(self):
        self._move()
        self._speed_x = decelerate(self._speed_x, self.ACC_X)
        if self._speed_x == 0:
            self.enter_action_stay_phase()
            self._set_image_type("STOP")

    def enter_action_stay_phase(self):
        self.action_status = EnemyIIIActionPhase.Stay
        self._speed_x = self._speed_y = 0
        self._count_action_stay = self._STAY_DURATION

    def _action_stay(self):
        self._count_action_stay -= 1
        if not self._count_action_stay:
            self.enter_action_leave_phase()

    def enter_action_leave_phase(self):
        self.action_status = EnemyIIIActionPhase.Leave
        self._speed_x = 0
        self._speed_y = self.MAX_SPEED_DOWN

    def _action_leave(self):
        if self.rect.top < SCREEN_HEIGHT:
            self._move()
        else:
            self.kill()

    # --------------- Attack status --------------- #
    def enter_attack_idle_phase(self):
        self._count_attack_interval = self._ATTACK_SPEED
        self.attack_status = EnemyIIIAttackPhase.Idle

    def _action_attack_idle(self):
        if self._count_attack_interval <= 0:
            self.enter_attack_phase()
        else:
            self._count_attack_interval -= 1

    def enter_attack_phase(self):
        self.attack_status = EnemyIIIAttackPhase.Attack

    @abstractmethod
    def _action_attack(self, *args, **kwargs):
        pass

    # --------------- Init method --------------- #
    @classmethod
    def _init_attributes(cls):
        cls.MAX_SPEED_DOWN = cls.MAX_SPEED_UP = 1
        cls.MAX_SPEED_X = 10
        cls.SCORE = 500
        cls.MAX_HEALTH = 500
        # s = t*v0/2 => t = 2s/v0
        # v0 - a * t = 0 => a = v0**2 / 2s
        cls.ACC_X = round((cls.MAX_SPEED_X ** 2) / (SCREEN_WIDTH*7/4), 2)
        cls.ACC_UP = cls.ACC_DOWN = 0
        cls._IS_SET_ATTRS = True
