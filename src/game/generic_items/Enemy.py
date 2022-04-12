
from abc import ABC, abstractmethod
import random
from pygame import Vector2
from enum import Enum
from src.game.animation import AttachEffect

from src.game.animation import AnimeSprite, AnimeSprite
from src.game.groups import G_Enemys, G_Player1
from src.util.type import Pos, Size
from src.helper.sound import play_sound
from src.setting import SCREEN_HEIGHT
from src.util.angle import follow_angle
from src.util.inertial import decelerate
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class BaseEnemy(ABC):

    MAX_HEALTH = 100
    SCORE = 100

    def __init__(self) -> None:

        self.is_active = True
        self.state = None
        self._speed = Vector2(0, 0)

        self._score = self.SCORE

        self._health = self.MAX_HEALTH

    # --------------- Attributes --------------- #
    # ----- Speed
    @property
    def speed(self) -> tuple:
        return self._speed.x, self._speed.y

    # ----- Health
    @property
    def health(self) -> int:
        return self._health

    @property
    def score(self) -> int:
        return self._score


class EnemyI(AnimeSprite, BaseEnemy):

    MAX_HEALTH = 100
    SCORE = 100

    ATTACK_SPEED = 100
    SPEED_X = 0
    SPEED_Y = 1
    ACC_X = 0.2

    def __init__(self, pos: Pos, frames, frame_size: Size = None, *groups, **kwargs):
        BaseEnemy.__init__(self)
        AnimeSprite.__init__(self, frames, frame_size,
                             enable_rotate=kwargs.setdefault(
                                 "enable_rotate", False),
                             angle=kwargs.setdefault("angle", 0),
                             *groups)
        self.set_pos(pos)
        self.add(G_Enemys)

        self.attack_speed = self.ATTACK_SPEED
        self._count_attack_interval = self.ATTACK_SPEED

    # --------------- Super Methods Override --------------- #

    def update(self, *args, **kwargs) -> None:
        """ Update method from Sprite, is called per frame """
        super().update()
        self._move()
        if self.is_active:
            self.action(*args, **kwargs)

    def anime_end_loop_hook(self):
        if not self.is_active:
            self.kill()

    # --------------- Behaviors --------------- #

    def action(self, *args, **kwargs) -> None:
        """ Main method to be called in `self.update()`
        """
        if self.rect.top > SCREEN_HEIGHT + 100:
            self.kill()
        elif self.rect.top > 0:
            self.attack(None)

    def _move(self) -> None:
        self.rect.move_ip(self._speed.x, self._speed.y)

    def hit(self, damage=100, **kwargs) -> None:
        """ This function is called in collision detection
        """
        if self.is_active:
            self._health -= damage
            if self._health > 0:
                # Get Hit effect
                AttachEffect(
                    self,
                    frames={
                        "IDLE": self.frames["HIT"]
                    },
                    frame_size=self.frame_size,
                    angle=self.angle
                )
            else:
                # HP below 0
                self.destroy()
            return True
        else:
            return False

    def destroy(self) -> None:
        """ This method is called when the sprite's health decrease to 0
        The animation state will be set to `DESTROY` and the `self.anime_end_loop_hook()` can be called
        to kill the sprite after destroy animation
        """
        self._health = 0
        self.is_active = False
        self.set_anime_state("DESTROY")
        play_sound("EXPLODE")

    def attack(self, target):
        """ The method is called continuously to perfom a attack in the `self.update()` method 
            It counts down the attack interval and will call create a AttachEffect which
            will activate a callback function to call `self.shoot()` after its animation will be finished
        """
        if self._count_attack_interval > 0:
            self._count_attack_interval -= 1
        else:
            self._count_attack_interval = self.attack_speed

            def _attack_cb():
                if self.is_active:
                    self.shoot(target)

            AttachEffect(
                self,
                frames={
                    "IDLE": self.frames["ATTACK"]
                },
                frame_size=None,
                angle=self.angle,
                cb_func=_attack_cb
            )

    @abstractmethod
    def shoot(self, target):
        """ This method will be called after an attack animation is finished """
        pass

    # --------------- Attributes --------------- #
    # ----- Position

    @property
    def pos(self) -> tuple:
        return self.rect.center

    def set_pos(self, point: Pos) -> None:
        self.rect.center = point.to_list()


class EnemyIIActionPhase(Enum):
    Entrance = 0
    Stay = 1
    Leave = 2


class EnemyII(EnemyI):
    """ Enemy II has several different states and will target the player when shooting """

    STAY_DURATION = 1000

    SPEED_X = 10

    def __init__(
            self,
            pos: Pos,
            frames,
            frame_size: Size = None,
            is_left=True):

        self.is_left = is_left
        if is_left:
            self.angle = 90
        else:
            self.angle = -90

        super().__init__(pos, frames, frame_size,
                         **{"enable_rotate": True, "angle": self.angle})

        self._count_action_stay = self.STAY_DURATION

        self.state = EnemyIIActionPhase.Entrance

        self.enter_action_entrance_phase()

    # ---------- Override Method
    def destroy(self) -> None:
        from src.game.supply import get_random_supply
        if random.random() > 0.7:
            sup = get_random_supply()
            sup(Pos(self.pos))
        return super().destroy()

    # --------------- Main action status --------------- #

    def action(self, *args, **kwargs):
        if self.state == EnemyIIActionPhase.Entrance:
            self._action_entrance()
        else:
            if self.state == EnemyIIActionPhase.Stay:
                self._action_stay()
            else:
                self._action_leave()
            player = G_Player1.sprites()[0]
            self.aim(Pos(player.rect.center))
            self.attack(player)

    # --------------- Sub action status --------------- #

    def enter_action_entrance_phase(self):
        if self.is_left:
            self._speed.x = self.SPEED_X
        else:
            self._speed.x = -self.SPEED_X

        self._speed.y = 0
        self.state = EnemyIIActionPhase.Entrance
        self.set_anime_state("MOVE")

    def _action_entrance(self):
        self._speed.x = decelerate(self._speed.x, self.ACC_X)
        if self._speed.x == 0:
            self.enter_action_stay_phase()

    def enter_action_stay_phase(self):
        self.state = EnemyIIActionPhase.Stay
        self._speed.x = self._speed.y = 0
        self._count_action_stay = self.STAY_DURATION
        self.set_anime_state("IDLE")

    def _action_stay(self):
        self._count_action_stay -= 1
        if not self._count_action_stay:
            self.enter_action_leave_phase()

    def enter_action_leave_phase(self):
        self.state = EnemyIIActionPhase.Leave
        self._speed.x = 0
        self._speed.y = self.SPEED_Y

    def _action_leave(self):
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    # --------------- Aim --------------- #

    def aim(self, point: Pos):
        self.angle = follow_angle(
            Pos(self.rect.center), point, self.angle, rotation_speed=2)
