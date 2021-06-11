""" Basic classes for bullets
Includes:
    -> BasicBullet()
    -> StraightBullet()
"""
from abc import ABC

from LostViking.src.constants import SCREEN
from LostViking.src.generic_loader.image_loader import load_image
from LostViking.src.generic_items.ImageHelper import SingleImageHelper
import pygame
import math


class BasicBullet(SingleImageHelper, pygame.sprite.Sprite, ABC):
    """ Basic Bullet Class
    To implement this Class:
        -> Set _init_image() from SingleImageHelper
        -> Set set_speed(_speed_x, _speed_y) in __init__()
    """

    def __init__(self, init_position: (list, tuple), speed: (list, tuple)):
        SingleImageHelper.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self._speed_x = speed[0]
        self._speed_y = speed[1]
        self.rect = self.image.get_rect()
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


class SpinBullet(BasicBullet, ABC):
    _MAX_SPEED_X = 0
    _MAX_SPEED_Y = 0

    def __init__(self, init_position: (list, tuple), angle=0):
        self.angle = angle
        angle = angle * math.pi / 180.0
        speed_x_ = round(self._MAX_SPEED_X * math.sin(angle))
        speed_y_ = round(self._MAX_SPEED_Y * math.cos(angle))

        BasicBullet.__init__(self,
                             init_position=init_position,
                             speed=[speed_x_, speed_y_])

        self.image = pygame.transform.rotate(self.image, self.angle)

    def _trans_image(self):
        temp = self.rect.center
        image_ = pygame.transform.rotate(self.image, self.angle)
        self.rect = image_.get_rect()
        self.rect.center = temp
        return image_


"""
class BulletViking(StraightBullet):
    _MAX_SPEED = 15

    def __init__(self, init_position):
        StraightBullet.__init__(self, init_position=init_position, direction=[0, -1])
        self.MaxSpeed = self._MAX_SPEED

    @classmethod
    def init_image(cls):
        cls._IMAGE = load_image_alpha("PlayerPlane/bullet.png")
"""


class BulletPhoenix(SpinBullet):
    _MAX_SPEED = 15

    def __init__(self, position, angle):
        SpinBullet.__init__(self, position, angle)

    @classmethod
    def init_image(cls):
        cls._IMAGE = load_image("Enemy/laser.png")


class BulletInterceptor(SpinBullet):
    _MAX_SPEED = 5

    def __init__(self, position, angle):
        SpinBullet.__init__(self, position, angle)

    @classmethod
    def init_image(cls):
        cls._IMAGE = load_image("Enemy/laser.png")
