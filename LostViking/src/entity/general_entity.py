from abc import abstractmethod, ABC

import pygame
from pygame.sprite import AbstractGroup


class GraphicEntity:
    """
    General Graphic Entity with changeable images
    """
    IMAGE = {"Base": [None]}

    INIT_FLAG = False

    def __init__(self):
        if not self.INIT_FLAG:
            self._init_image()
        self._image_switch = 0
        self._main_image_type = self.IMAGE["Base"]
        self.image = self._main_image_type[self._image_switch]

    # Switch image
    def _switch_image(self):
        self._image_switch = (self._image_switch + 1) % len(self._main_image_type)
        self.image = self._main_image_type[self._image_switch]

    def set_image_type(self, image_type):
        self._main_image_type = self.IMAGE[image_type]

    @classmethod
    @abstractmethod
    def _init_image(cls):
        pass


class MovableEntity(GraphicEntity, ABC):
    MAX_SPEED_X = 0
    MAX_SPEED_UP = 0
    MAX_SPEED_DOWN = 0

    def __init__(self, point=None):
        GraphicEntity.__init__(self)
        self._speed_x = 0
        self._speed_y = 0
        self._move_flag_x = False
        self._move_flag_y = False
        self.rect = self.image.get_rect()
        self._set_pos(point)

    def _move(self):
        self.rect.move_ip(self._speed_x, self._speed_y)

    # Set position
    def _set_pos(self, point=None):
        if point is None:
            self.rect.center = (int(pygame.display.get_surface().get_width() // 2),
                                int(pygame.display.get_surface().get_height() - self.rect.height // 2 - 30))
        else:
            self.rect.center = point

    @property
    def speed_x(self):
        return self._speed_x

    @speed_x.setter
    def speed_x(self, speed_x):
        if not isinstance(speed_x, int):
            raise ValueError('score must be an integer!')
        if speed_x < -self.MAX_SPEED_X or speed_x > self.MAX_SPEED_X:
            raise ValueError('score must between {} ~ {}!'.format(-self.MAX_SPEED_X, self.MAX_SPEED_X))
        self._speed_x = speed_x

    @property
    def speed_y(self):
        return self._speed_y

    @speed_y.setter
    def speed_y(self, speed_y):
        if not isinstance(speed_y, int):
            raise ValueError('score must be an integer!')
        if speed_y < -self.MAX_SPEED_UP or speed_y > self.MAX_SPEED_DOWN:
            raise ValueError('score must between {} ~ {}!'.format(-self.MAX_SPEED_UP, self.MAX_SPEED_DOWN))
        self._speed_y = speed_y


class InertialEntity(MovableEntity, ABC):
    ACC_X = 0
    ACC_UP = 0
    ACC_DOWN = 0

    def __init__(self, point=None):
        MovableEntity.__init__(self, point)

    # Speed down the plane when there's no movement commands on a X or Y direction
    def _inertial_deceleration(self):
        # If no speed
        if self._speed_x == 0 and self._speed_y == 0:
            return
        else:
            # If no move X command but speed_x != 0
            if not self._move_flag_x:
                if self._speed_x > 0:  # If it is moving right
                    self._speed_x -= self.ACC_X
                    if self._speed_x <= 0:
                        self._speed_x = 0
                elif self._speed_x < 0:  # If it is moving left
                    self._speed_x += self.ACC_X
                    if self._speed_x >= 0:
                        self._speed_x = 0
            # If no move Y command but speed_y != 0
            if not self._move_flag_y:
                if self._speed_y > 0:  # If it is moving down
                    self._speed_y -= self.ACC_UP
                    if self._speed_y <= 0:
                        self._speed_y = 0
                        self.set_image_type("MoveNormal")
                elif self._speed_y < 0:  # If it is moving up
                    self._speed_y += self.ACC_DOWN
                    if self._speed_y >= 0:
                        self._speed_y = 0
                        self.set_image_type("MoveNormal")

    def accelerate_up(self):
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y > -self.MAX_SPEED_UP:
            self._speed_y -= self.ACC_UP

    def accelerate_down(self):
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y < self.MAX_SPEED_DOWN:
            self._speed_y += self.ACC_DOWN

    def accelerate_left(self):
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x > -self.MAX_SPEED_X:
            self._speed_x -= self.ACC_X

    def accelerate_right(self):
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x < self.MAX_SPEED_X:
            self._speed_x += self.ACC_X
