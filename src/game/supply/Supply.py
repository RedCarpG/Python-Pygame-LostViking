from enum import Enum
import abc
import random

import pygame
from pygame import Vector2
from pygame.sprite import spritecollideany

from src.game.animation import AnimeSprite
from src.setting import SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.groups import G_Supplies, G_Players
from src.util.type import Pos, Size
from src.util.inertial import accelerate, decelerate
from src.game.player import PlayerPlane

class SupplyStatus(Enum):
    Enter = 0
    Stay = 1
    Move = 2
    Leave = 3


class Supply(AnimeSprite, abc.ABC):
    STAY_PHASE_DURATION = 20
    MOVE_PHASE_DURATION = 1500
    SPEED_CHANGE_DURATION = 300

    MAX_SPEED = 2
    ACC = 0.01

    SCORE = 1000

    def __init__(self, pos: Pos, frames, frame_size: Size):
        super().__init__(frames, frame_size)

        self.is_active = True

        self.supply_type = None
        self.add(G_Supplies)

        self._direction = Vector2(
            random.choice([1, -1]),
            random.choice([1, -1])
        )
        self._speed = Vector2(0, 0)

        self.status = SupplyStatus.Stay
        self._count_status_duration = self.STAY_PHASE_DURATION
        self._count_speed_change_duration = self.SPEED_CHANGE_DURATION

        self.set_pos(pos)

    def update(self):
        self.anime()
        if self.is_active:
            if self.status == SupplyStatus.Enter:
                self._action_enter()
            elif self.status == SupplyStatus.Stay:
                self._action_stay()
            elif self.status == SupplyStatus.Move:
                self._action_move()
            else:
                self._action_leave()
            self.collide_player(G_Players)
        else:
            self.kill()

    @abc.abstractmethod
    def get_by_player(self, player: PlayerPlane):
        self.kill()

    def enter_action_enter_phase(self):
        self.status = SupplyStatus.Enter
        self._speed.y = self.MAX_SPEED
        self._speed.x = 0

    def enter_action_stay_phase(self):
        self.status = SupplyStatus.Stay
        self._count_status_duration = self.STAY_PHASE_DURATION

    def enter_action_move_phase(self):
        self.status = SupplyStatus.Move
        self._count_speed_change_duration = self.SPEED_CHANGE_DURATION
        self._count_status_duration = self.MOVE_PHASE_DURATION
        self._direction.x = random.choice([1, -1])
        self._direction.y = random.choice([1, -1])

    def enter_action_leave_phase(self):
        self.status = SupplyStatus.Leave
        self._speed.y = self.MAX_SPEED

    def set_pos(self, point: Pos):
        if point is None:
            self.rect.left, self.rect.top = [random.randint(
                0, SCREEN_WIDTH - self.rect.width), - self.rect.height]
        else:
            self.rect.center = point.to_list()

    def _action_enter(self):
        self._move()
        if self.rect.bottom > SCREEN_HEIGHT / 3:
            self._speed.y = decelerate(self._speed.y, self.ACC)
            if self._speed.y <= 0:
                self.enter_action_stay_phase()

    def _action_stay(self):
        if self._count_status_duration:
            self._count_status_duration -= 1
        else:
            self.enter_action_move_phase()

    def _action_move(self):
        self._move()

        if self._count_speed_change_duration:
            self._speed.x = accelerate(
                self._speed.x, self.MAX_SPEED, self._direction.x, self.ACC)
            self._speed.y = accelerate(
                self._speed.y, self.MAX_SPEED, self._direction.y, self.ACC)
            self._count_speed_change_duration -= 1
        else:
            self._speed.x = decelerate(self._speed.x, self.ACC)
            self._speed.y = decelerate(self._speed.y, self.ACC)

            if self._speed.y == 0 and self._speed.x == 0:
                self._count_speed_change_duration = self.SPEED_CHANGE_DURATION
                self._direction.x = random.choice([1, -1])
                self._direction.y = random.choice([1, -1])

        if self.rect.bottom > SCREEN_HEIGHT * 2 / 3 and self._speed.y > 0:
            self._speed.y = -self._speed.y
            self._direction.y = -self._direction.y

        if self._count_status_duration:
            self._count_status_duration -= 1
        else:
            self.enter_action_leave_phase()

    def _action_leave(self):
        if self.rect.top < SCREEN_HEIGHT:
            self._move()
        else:
            self.kill()

    def _move(self):
        if self.rect.left <= 0 and self._speed.x < 0:
            self._speed.x = -self._speed.x
            self._direction.x = -self._direction.x
        elif self.rect.right >= SCREEN_WIDTH and self._speed.x > 0:
            self._speed.x = -self._speed.x
            self._direction.x = -self._direction.x
        if self.rect.top <= 0 and self._speed.y < 0:
            self._speed.y = -self._speed.y
            self._direction.y = -self._direction.y
        self.rect.move_ip(self._speed.x, self._speed.y)

    def collide_player(self, player_group):
        player = spritecollideany(self, player_group)
        if player:
            player.add_score(self.SCORE)
            self.get_by_player(player)
