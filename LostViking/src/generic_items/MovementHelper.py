"""
General entities for inheriting by classes
with interface to get position and speed
Includes:
    -> StaticMoveHelper
    -> InertialMoveHelper
"""
import pygame
from abc import ABC, abstractmethod
import warnings


class StaticMoveHelper(ABC):
    """ Movable class with speed
    To implement this Class :
        -> set _init_speed()
        -> (optional) set self.start_position
    """

    def __init__(self):

        self._speed_x = 0
        self._speed_y = 0
        if hasattr(self, "image"):
            self.rect = self.image.get_rect()
        else:
            warnings.warn("WARNING: Attribute image is not set for {}".format(self))
            self.rect = pygame.rect.Rect(0, 0, 0, 0)

        self.start_position = (0, 0)

    def _move(self) -> None:
        """ Move its rect by its _speed_x and _speed_y"""
        self.rect.move_ip(self._speed_x, self._speed_y)

    # Position
    def set_pos(self, point=None) -> None:
        """ Move its rect to a point, or a default position """
        if point is None:
            self.rect.center = self.start_position
        else:
            self.rect.center = point

    def get_position(self) -> (list, tuple):
        return self.rect.center

    # Speed
    def get_speed(self):
        return self._speed_x, self._speed_y

    @classmethod
    @abstractmethod
    def _init_speed(cls):
        cls._INIT_FLAG_SPEED = False
        cls._MAX_SPEED_L = 0
        cls._MAX_SPEED_R = 0
        cls._MAX_SPEED_UP = 0
        cls._MAX_SPEED_DOWN = 0


class InertialMoveHelper(StaticMoveHelper, ABC):
    """
    Movement Helper with acceleration/deceleration
    To implement this Class :
        -> set _init_speed() (from StaticMoveHelper)
        -> set _init_acc()
        -> (optional) set self.start_position (from StaticMoveHelper)
    """

    def __init__(self):
        StaticMoveHelper.__init__(self)

        # Move Flags for detecting
        self._move_flag_x = False
        self._move_flag_y = False

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
                        if hasattr(self, "_set_image_type"):
                            self._set_image_type("MoveNormal")
                elif self._speed_y < 0:  # If it is moving up, decelerate by _ACC_DOWN
                    self._speed_y += self._ACC_DOWN
                    if self._speed_y >= 0:
                        self._speed_y = 0
                        if hasattr(self, "_set_image_type"):
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

    @classmethod
    @abstractmethod
    def _init_acc(cls):
        cls._ACC_L = 0
        cls._ACC_R = 0
        cls._ACC_UP = 0
        cls._ACC_DOWN = 0
        cls._INIT_FLAG_ACC = False
