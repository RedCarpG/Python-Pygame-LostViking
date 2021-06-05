"""
General entities for inheriting by classes
Includes:
    -> MovableEntity
    -> InertialEntity
"""
import pygame
from abc import ABC
from LostViking.src.generic_items.graphic_helper import LoopImageHelper


class MovableEntity(LoopImageHelper, ABC):
    """ Movable class with speed """
    _MAX_SPEED_L = 0
    _MAX_SPEED_R = 0
    _MAX_SPEED_UP = 0
    _MAX_SPEED_DOWN = 0

    def __init__(self, point=None):
        LoopImageHelper.__init__(self)
        self._speed_x = 0
        self._speed_y = 0
        self._move_flag_x = False
        self._move_flag_y = False
        self.rect = self.image.get_rect()
        self._set_pos(point)

    def _move(self) -> None:
        """ Move its rect by its _speed_x and _speed_y"""
        self.rect.move_ip(self._speed_x, self._speed_y)

    # Set position
    def _set_pos(self, point=None) -> None:
        """ Move its rect to a point, or a default position """
        if point is None:
            self.rect.center = (int(pygame.display.get_surface().get_width() // 2),
                                int(pygame.display.get_surface().get_height() - self.rect.height // 2 - 30))
        else:
            self.rect.center = point

    def get_position(self) -> list:
        return self.rect.center

    @property
    def speed_x(self) -> int:
        return self._speed_x

    @speed_x.setter
    def speed_x(self, speed_x):
        if not isinstance(speed_x, int):
            raise ValueError('score must be an integer!')
        if speed_x < -self._MAX_SPEED_L or speed_x > self._MAX_SPEED_R:
            raise ValueError('score must between {} ~ {}!'.format(-self._MAX_SPEED_L, self._MAX_SPEED_R))
        self._speed_x = speed_x

    @property
    def speed_y(self) -> int:
        return self._speed_y

    @speed_y.setter
    def speed_y(self, speed_y):
        if not isinstance(speed_y, int):
            raise ValueError('score must be an integer!')
        if speed_y < -self._MAX_SPEED_UP or speed_y > self._MAX_SPEED_DOWN:
            raise ValueError('score must between {} ~ {}!'.format(-self._MAX_SPEED_UP, self._MAX_SPEED_DOWN))
        self._speed_y = speed_y


class InertialEntity(MovableEntity, ABC):
    """ MovableEntity with acceleration/deceleration
    """
    _ACC_L = 0
    _ACC_R = 0
    _ACC_UP = 0
    _ACC_DOWN = 0

    def __init__(self, point=None):
        MovableEntity.__init__(self, point)

    """ --------------------- Deceleration --------------------- """

    # Speed down the plane when there's no movement commands on a X or Y direction
    def _inertial_deceleration(self) -> None:
        """ Decrease the _speed_x or _speed_y to 0 automatically
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        # If no speed
        if self._speed_x == 0 and self._speed_y == 0:
            return
        else:
            # If no move X command but _speed_x != 0
            if not self._move_flag_x:

                if self._speed_x > 0:  # If it is moving right, decelerate by _ACC_L
                    self._speed_x -= self._ACC_L
                    if self._speed_x <= 0:
                        self._speed_x = 0
                elif self._speed_x < 0:  # If it is moving left, decelerate by _ACC_R
                    self._speed_x += self._ACC_R
                    if self._speed_x >= 0:
                        self._speed_x = 0

            # If no move Y command but _speed_y != 0
            if not self._move_flag_y:

                if self._speed_y > 0:  # If it is moving down, decelerate by _ACC_UP
                    self._speed_y -= self._ACC_UP
                    if self._speed_y <= 0:
                        self._speed_y = 0
                        self._set_image_type("MoveNormal")
                elif self._speed_y < 0:  # If it is moving up, decelerate by _ACC_DOWN
                    self._speed_y += self._ACC_DOWN
                    if self._speed_y >= 0:
                        self._speed_y = 0
                        self._set_image_type("MoveNormal")

    """ --------------------- Accelerations --------------------- """

    def _accelerate_up(self) -> None:
        """ In crease the _speed_y by _ACC_UP (negative)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y > -self._MAX_SPEED_UP:
            self._speed_y -= self._ACC_UP

    def _accelerate_down(self) -> None:
        """ In crease the _speed_x by _ACC_DOWN (positive)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y < self._MAX_SPEED_DOWN:
            self._speed_y += self._ACC_DOWN

    def _accelerate_left(self) -> None:
        """ In crease the _speed_x by _ACC_L (negative)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x > -self._MAX_SPEED_L:
            self._speed_x -= self._ACC_L

    def _accelerate_right(self) -> None:
        """ In crease the _speed_x by _ACC_R (positive)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x < self._MAX_SPEED_R:
            self._speed_x += self._ACC_R
