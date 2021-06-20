import abc
from abc import abstractmethod, ABC
import warnings
import math
from pygame.transform import rotate

from ..groups import Destroyed_Plane_G
from .ImageEntity import LoopImageEntity


class BasicPlaneEntity(LoopImageEntity, ABC):

    MAX_SPEED_X = 0
    MAX_SPEED_UP = 0
    MAX_SPEED_DOWN = 0
    ACC_X = None
    ACC_UP = None
    ACC_DOWN = None

    MAX_HEALTH = 100

    _IS_SET_ATTRS = False

    def __init__(self, **kwargs):
        # Check Initialization
        if not hasattr(self, "INIT_FLAG") or not self.INIT_FLAG:
            raise Exception("!!!ERROR: Class is not init! {}".format(self.__class__))
        if not self._IS_SET_ATTRS:
            warnings.warn("!!!ERROR: Entity SPEED is not set! {}".format(self.__class__))
        LoopImageEntity.__init__(self)

        # Set basic properties
        self.is_active = True

        self._speed_x = kwargs.pop("speed_x", 0)
        self._speed_y = kwargs.pop("speed_y", 0)
        self._health = kwargs.pop("health", self.MAX_HEALTH)
        self.set_pos(kwargs.pop("start_point", (0, 0)))

    def update(self, *args, **kwargs) -> None:
        """ Update method from Sprite, is called per frame """
        if self.is_active:
            self._switch_image()
            self._action(*args, **kwargs)
        else:
            self._destroy()

    def hit(self, damage=100, **kwargs) -> None:
        """
        This function is called in collision detection
        """
        if self._damaged(damage):
            self.is_active = False
            self.kill()
            self.add(Destroyed_Plane_G)
            self._image_switch = 0
            self._set_image_type("EXPLODE")

    # --------------- Behaviors --------------- #

    @abc.abstractmethod
    def _action(self, *args, **kwargs) -> None:
        """ Method to be override for behaviors
        """
        pass

    def _damaged(self, damage, **kwargs) -> bool:
        if self._health > 0:
            self._health -= damage
            return False
        else:
            self._health = 0
            return True

    def _move(self) -> None:
        """ Move its rect by its _speed_x and _speed_y"""
        self.rect.move_ip(self._speed_x, self._speed_y)

    def _destroy(self) -> None:
        finished = self._switch_image()
        if finished:
            self.kill()
            del self

    # --------------- Properties --------------- #

    # Position
    def set_pos(self, point) -> None:
        """ Move its rect to a point, or a default position """
        self.rect.center = point

    def get_position(self) -> tuple:
        return self.rect.center

    # Speed
    def get_speed(self) -> tuple:
        return self._speed_x, self._speed_y

    # --------------- Acceleration --------------- #

    def _accelerate_up(self) -> None:
        """ In crease the _speed_y by _ACC_UP (negative)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y > -self.MAX_SPEED_UP:
            self._speed_y -= self.ACC_UP

    def _accelerate_down(self) -> None:
        """ In crease the _speed_x by _ACC_DOWN (positive)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y < self.MAX_SPEED_DOWN:
            self._speed_y += self.ACC_DOWN

    def _accelerate_left(self) -> None:
        """ In crease the _speed_x by _ACC_L (negative)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x > -self.MAX_SPEED_X:
            self._speed_x -= self.ACC_X

    def _accelerate_right(self) -> None:
        """ In crease the _speed_x by _ACC_R (positive)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x < self.MAX_SPEED_X:
            self._speed_x += self.ACC_X

    # --------------- Deceleration --------------- #

    def _deceleration_x(self) -> int:
        """ Decrease the _speed_x or _speed_y to 0 automatically
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        if self._speed_x > 0:  # If it is moving right, decelerate by _ACC_L
            self._speed_x -= self.ACC_X
            if self._speed_x <= 0:
                self._speed_x = 0
                return 1
        elif self._speed_x < 0:  # If it is moving left, decelerate by _ACC_R
            self._speed_x += self.ACC_X
            if self._speed_x >= 0:
                self._speed_x = 0
                return 1
        return 0

    def _deceleration_y(self) -> int:
        """ Decrease the _speed_x or _speed_y to 0 automatically
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        if self._speed_y > 0:  # If it is moving down, decelerate by _ACC_UP
            self._speed_y -= self.ACC_UP
            if self._speed_y <= 0:
                self._speed_y = 0
            return 1
        elif self._speed_y < 0:  # If it is moving up, decelerate by _ACC_DOWN
            self._speed_y += self.ACC_DOWN
            if self._speed_y >= 0:
                self._speed_y = 0
                return 1
        return 0

    # --------------- Init Methods --------------- #
    @classmethod
    @abstractmethod
    def _init_image(cls) -> None:
        """ Override this method to load images """
        cls.IMAGE = dict()
        cls.IMAGE["BASE"] = []
        cls.IMAGE["IDLE"] = []
        cls.IMAGE["EXPLODE"] = []
        cls._IS_SET_IMAGE = False

    @classmethod
    @abstractmethod
    def _init_attributes(cls) -> None:
        """ Override this method to assign speed """
        cls.MAX_HEALTH = 100
        cls.MAX_SPEED_X = 0
        cls.MAX_SPEED_UP = 0
        cls.MAX_SPEED_DOWN = 0
        cls.ACC_X = 0
        cls.ACC_UP = 0
        cls.ACC_DOWN = 0
        cls._IS_SET_ATTRS = False

    @classmethod
    def init(cls) -> None:
        """
        Call this method to init, INIT_FLAG is used to
        determine whether the class is initialized
        """
        if not hasattr(cls, "INIT_FLAG") or not cls.INIT_FLAG:
            cls._init_image()
            cls._init_attributes()
            cls.INIT_FLAG = True


class BasicSpinPlaneEntity(BasicPlaneEntity, ABC):

    def __init__(self, **kwargs):
        # Init
        BasicPlaneEntity.__init__(self, **kwargs)
        # Angle
        self.angle = 0

    def _switch_image(self, switch_rate=0) -> bool:
        """
        This method rewrites the method from LoopImageEntity
        :param switch_rate: switch rate between each change
        :return: True if loop finished, False if loop not finished
        """
        if self._image_switch_interval >= switch_rate:
            self._image_switch = (self._image_switch + 1) % len(self._main_image_type)
            self.image = self._main_image_type[self._image_switch]
            self._image_switch_interval = 0

            # Rotate Image
            self.image = rotate(self._main_image_type[self._image_switch], self.angle)
            temp = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = temp

            if self._image_switch == 0:
                return True
        else:
            self._image_switch_interval += 1

        return False

    def aim(self, point) -> None:
        """ Aim the plane at a target point
        :param point
        """
        self.angle = self.cal_angle(self.rect.center, point)

    @classmethod
    def cal_angle(cls, base_point, target_point) -> int:
        """ Calculate angle between two points
        :param base_point
        :param target_point
        :return int angle degree value
        """
        if base_point[1] == target_point[1]:
            if target_point[0] > base_point[0]:
                angle = 90
            else:
                angle = -90
        elif base_point[0] == target_point[0]:
            if target_point[1] > base_point[1]:
                angle = 0
            else:
                angle = 180
        else:
            angle = math.atan((target_point[0] - base_point[0]) / (target_point[1] - base_point[1]))
            angle = angle * 360 / 2 / math.pi
            if base_point[1] > target_point[1]:
                if base_point[0] < target_point[0]:
                    angle += 180
                else:
                    angle -= 180
        return angle
