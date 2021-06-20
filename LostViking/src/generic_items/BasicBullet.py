""" Basic classes for bullets
Includes:
    -> BasicBullet()
    -> BasicSpinBullet()
"""
from abc import ABC, abstractmethod
import pygame
import math

from LostViking.src.constants import SCREEN
from LostViking.src.groups import Bullet_G
from .ImageEntity import SingleImageEntity


class BasicBullet(SingleImageEntity, ABC):
    """ Basic Bullet Class
    """

    MAX_SPEED_X = 0
    MAX_SPEED_Y = 0

    _IS_SET_ATTRS = False

    def __init__(self,
                 init_position: (list, tuple),
                 speed: (list, tuple) = None, **kwargs):
        # Check Initialization
        if not hasattr(self, "INIT_FLAG") or not self.INIT_FLAG:
            raise Exception("!!!ERROR: Class is not init! {}".format(self.__class__))
        SingleImageEntity.__init__(self)
        self.add(Bullet_G)

        # Set Attributes
        if speed:
            self._speed_x = speed[0]
            self._speed_y = speed[1]
        else:
            self._speed_x = self.MAX_SPEED_X
            self._speed_y = self.MAX_SPEED_Y

        # Set Position
        self.rect.center = init_position

    # General update method for bullets
    def update(self):
        if self._hit_screen_edge():
            self.kill()
        else:
            self._move()

    # General get hit method for bullets
    def hit(self):
        self.kill()
        del self

    # General movement method
    def _move(self):
        self.rect.move_ip(self._speed_x, self._speed_y)

    # General method to detect whether in screen
    def _hit_screen_edge(self):
        if self.rect.top > SCREEN.get_h() \
                or self.rect.bottom < 0 \
                or self.rect.right < 0 \
                or self.rect.left > SCREEN.get_w():
            return True
        return False

    @classmethod
    @abstractmethod
    def _init_attrs(cls):
        cls.MAX_SPEED_X = 0
        cls.MAX_SPEED_Y = 0
        cls._IS_SET_ATTRS = False

    @classmethod
    def init(cls):
        cls._init_image()
        cls._init_attrs()
        cls.INIT_FLAG = True


class BasicSpinBullet(BasicBullet, ABC):

    def __init__(self, init_position: (list, tuple), angle=0):
        self.angle = angle
        angle = angle * math.pi / 180.0
        speed_x_ = round(self.MAX_SPEED_X * math.sin(angle))
        speed_y_ = round(self.MAX_SPEED_Y * math.cos(angle))

        BasicBullet.__init__(self,
                             init_position=init_position,
                             speed=[speed_x_, speed_y_])
        # Rotate Image
        self.image = pygame.transform.rotate(self.image, self.angle)

    def _trans_image(self):
        image_ = pygame.transform.rotate(self.image, self.angle)
        temp = self.rect.center
        self.rect = image_.get_rect()
        self.rect.center = temp
        return image_

