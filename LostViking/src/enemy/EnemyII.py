"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import ABC
import math
from enum import Enum

from ..generic_items.BasicPlaneEntity import BasicSpinPlaneEntity
from ..groups import Enemy_G


class EnemyIIActionPhase(Enum):
    Move = 0
    Decelerate = 1
    Idle = 2


class EnemyII(BasicSpinPlaneEntity, ABC):
    """ Second type of Enemy, shoot and track the player """
    SCORE = 100
    _STAY_DURATION = 100

    def __init__(self, position, path=None, **kwargs):
        BasicSpinPlaneEntity.__init__(self, start_point=position, **kwargs)
        self.add(Enemy_G)

        self.path = path
        self.current_path = 0

        self.angle = 0

        self.action_status = EnemyIIActionPhase.Move
        #self.enter_action_move_phase()
        self._count_action_idle = self._STAY_DURATION

    def _action(self, *args, **kwargs):
        if self.action_status == EnemyIIActionPhase.Move:
            self._action_move()
        elif self.action_status == EnemyIIActionPhase.Decelerate:
            self._action_decelerate()
        else:
            self._action_idle()

    def enter_action_move_phase(self):
        self.aim(self.path[self.current_path])
        self.action_status = EnemyIIActionPhase.Move

    def _action_move(self):
        self._move()
        if self.rect.collidepoint(self.path[self.current_path]):
            self.enter_action_decelerate_phase()

    def enter_action_decelerate_phase(self):
        self.action_status = EnemyIIActionPhase.Decelerate

    def _action_decelerate(self):
        self._move()
        self._deceleration_y()
        self._deceleration_x()
        if self._speed_y == 0 and self._speed_y == 0:
            self.current_path += 1
            if self.current_path < len(self.path):
                self.enter_action_idle_phase()
            else:
                self.kill()

    def enter_action_idle_phase(self):
        self._count_action_idle = self._STAY_DURATION
        self.action_status = EnemyIIActionPhase.Idle

    def _action_idle(self, *args, **kwargs):
        if not self._count_action_idle:
            self._action_attack(*args, **kwargs)
            self.enter_action_move_phase()
        else:
            self._count_action_idle -= 1

    def _action_attack(self, *args, **kwargs):
        pass

    def aim(self, point):
        self.angle = self.cal_angle(self.rect.center, point)

        angle = self.angle * math.pi / 180
        self._speed_x = float(self.MAX_SPEED_X * math.sin(angle))
        self._speed_y = float(self.MAX_SPEED_X * math.cos(angle))

    @classmethod
    def _init_attributes(cls):
        cls.SCORE = 500
        cls.MAX_HEALTH = 500
        cls.MAX_SPEED_DOWN = cls.MAX_SPEED_UP = 0
        cls.MAX_SPEED_X = 10
        cls.ACC_X = 1
        cls.ACC_UP = cls.ACC_DOWN = 1
        cls._IS_SET_ATTRS = True
