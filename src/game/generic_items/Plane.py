
from abc import ABC, abstractmethod
from pygame import Surface

from game.animation.AnimSprite import AnimSprite
from game.groups import *


class PlanyEntity(AnimSprite):

    MAX_HEALTH = 100

    def __init__(self, sprites, **kwargs):
        AnimSprite.__init__(self, sprites)

        self.is_active = True
        self.is_destroied = False
        self.state = None
        self._speed_x = 0
        self._speed_y = 0
        self._health = 0

    def update(self, *args, **kwargs) -> None:
        """ Update method from Sprite, is called per frame """
        if self.is_active:
            self._action_phase(*args, **kwargs)
        elif self.is_destroied:
            self._destroy_phase(*args, **kwargs)

    def hit(self, damage=100, **kwargs) -> None:
        """
        This function is called in collision detection
        """
        if self._damaged(damage):
            self.is_active = False
            self._set_image_state("DESTROYED")

    # --------------- Status --------------- #
    @abstractmethod
    def _action_phase(self, *args, **kwargs) -> None:
        """ Method to be override for behaviors
        """
        pass

    def _destroy_phase(self, *args, **kwargs) -> None:
        self.kill()
        del self

    # --------------- Behaviors --------------- #
    def _damaged(self, damage, **kwargs) -> bool:
        if self._health > 0:
            self._health -= damage
            return False
        else:
            self._health = 0
            return True

    def _move(self) -> None:
        self.rect.move_ip(self._speed_x, self._speed_y)

    def end_loop_hook(self):
        if self.current_state == "DESTROYED":
            self.is_destroied = True
    # --------------- Propertie Interface--------------- #

    @property
    def pos(self) -> tuple:
        return self.rect.center

    def set_pos(self, point) -> None:
        self.rect.center = point

    @property
    def speed(self) -> tuple:
        return self._speed_x, self._speed_y

    @property
    def health(self) -> int:
        return self._health
