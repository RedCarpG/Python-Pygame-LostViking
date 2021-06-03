from abc import ABC

from ..GLOBAL import *
from ..generic.image import *
from ..basic_items.image_helper import SingleImageHelper
import math
import abc


class StraightBullet(SingleImageHelper, pygame.sprite.Sprite, ABC):
    _MAX_SPEED = 0

    def __init__(self, position):
        SingleImageHelper.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed_y = self._MAX_SPEED

    def update(self):
        if self._hit_screen_edge():
            self.kill()
        else:
            self._move()

    def hit(self):
        self.kill()

    def _move(self):
        self.rect.move_ip(0, self.speed_y)

    def _hit_screen_edge(self):
        if self.rect.top > SCREEN.get_h() \
                or self.rect.bottom < 0 or self.rect.right < 0 \
                or self.rect.left > SCREEN.get_w():
            return True
        return False


class SpinBullet(SingleImageHelper, pygame.sprite.Sprite, ABC):
    _MAX_SPEED = 0

    def __init__(self, position, angle=0):
        SingleImageHelper.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.angle = angle
        angle = angle * math.pi / 180.0
        self._speed_x = float(self._MAX_SPEED * math.sin(angle))
        self._speed_y = float(self._MAX_SPEED * math.cos(angle))
        self.image = pygame.transform.rotate(self.image, self.angle)

    def update(self):
        if self.whenkill():
            self.kill()
        else:
            self.move()

    def move(self):
        self.rect.move_ip(self._speed_x, self._speed_y)

    def _trans_image(self):
        temp = self.rect.center
        image_ = pygame.transform.rotate(self.image, self.angle)
        self.rect = image_.get_rect()
        self.rect.center = temp
        return image_

    def hit(self):
        self.kill()

    def _hit_screen_edge(self):
        if self.rect.top > SCREEN.get_h() \
                or self.rect.bottom < 0 or self.rect.right < 0 \
                or self.rect.left > SCREEN.get_w():
            return True
        return False


class Bullet_Viking(Bullet):
    _MAX_SPEED = 15

    def __init__(self, position, angle):
        self.MaxSpeed = self._MAX_SPEED
        Bullet.__init__(self, position, angle)

    def setImage(self):
        self.image = BULLET_IMAGE["Viking_Bullet"]


class Bullet_Phoenix(Bullet):
    PHOENIX_BULLET_SPEED = 15

    def __init__(self, position, angle):
        self.MaxSpeed = self.PHOENIX_BULLET_SPEED
        Bullet.__init__(self, position, angle)

    def setImage(self):
        self.image = BULLET_IMAGE["Phoenix_Laser"]


class Bullet_Interceptor(Bullet):
    INTERCEPTOR_BULLET_SPEED = 5

    def __init__(self, position, angle):
        self.MaxSpeed = self.INTERCEPTOR_BULLET_SPEED
        Bullet.__init__(self, position, angle)

    def setImage(self):
        self.image = BULLET_IMAGE["Phoenix_Bullet"]
