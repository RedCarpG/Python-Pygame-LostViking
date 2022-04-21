"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import ABC
import math
from enum import Enum
import random
from pygame import Vector2

from src.util.inertial import decelerate
from src.util.type import Pos, Size
from src.util.angle import cal_angle
from .EnemyI import EnemyI


class EnemyIIActionPhase(Enum):
    Move = 0
    Decelerate = 1
    Idle = 2


class EnemyIII(EnemyI):
    """ Second type of Enemy, shoot and track the player """

    MAX_SPEED_Y = 5
    ACC_Y = 0.2

    ATTACK_SPEED = 0
    
    STAY_DURATION = 100

    DROP_SUPPLY_CHANCE = 0.3

    def __init__(
            self,
            pos: Pos,
            frames,
            frame_size: Size = None,
            path: list = None):

        self.angle = 0

        super().__init__(pos, frames, frame_size,
                         **{"enable_rotate": True, "angle": self.angle})

        self.path = path
        self.current_path = 0

        self.state = EnemyIIActionPhase.Move
        self._count_action_idle = self.STAY_DURATION
        self.enter_action_move_phase()

    # --------------- Override Methods --------------- #
    def aim(self, point: list):
        self.angle = cal_angle(Pos(self.rect.center), Pos(point))
        self._speed = Vector2(0, self.MAX_SPEED_Y).rotate(-self.angle)

    # --------------- Main action status --------------- #

    def action(self, *args, **kwargs):
        if self.state == EnemyIIActionPhase.Move:
            self._action_move()
        elif self.state == EnemyIIActionPhase.Decelerate:
            self._action_decelerate()
        else:
            self._action_idle()

    # --------------- Sub action status --------------- #
    def enter_action_move_phase(self):
        self.aim(self.path[0])
        self.state = EnemyIIActionPhase.Move

    def _action_move(self):
        self.aim(self.path[0])
        if self.rect.collidepoint(self.path[0]):
            self.enter_action_decelerate_phase()

    def enter_action_decelerate_phase(self):
        self.state = EnemyIIActionPhase.Decelerate

    def _action_decelerate(self):
        self._speed.x = decelerate(self._speed.x, self.ACC_Y)
        self._speed.y = decelerate(self._speed.y, self.ACC_Y)
        if self._speed.x == 0 and self._speed.y == 0:
            self.path.pop(0)
            if len(self.path) > 0:
                self.enter_action_idle_phase()
            else:
                self.kill()

    def enter_action_idle_phase(self):
        self._count_action_idle = self.STAY_DURATION
        self.state = EnemyIIActionPhase.Idle

    def _action_idle(self, *args, **kwargs):
        if not self._count_action_idle:
            from src.game.groups import G_Player1
            self.attack(G_Player1.sprite)
            self.enter_action_move_phase()
        else:
            self._count_action_idle -= 1
