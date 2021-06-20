"""
Player controllable object
"""
import pygame
from ..generic_loader.image_loader import load_image
from ..generic_items.BasicBullet import BasicBullet
from ..groups import Player_Bullet_G


class PlayerBullet1(BasicBullet):
    """ Player's Bullet 1 type,
    -> Implements StraightBullet class :
            -> SingleImageHelper
            -> pygame.sprite.Sprite
    + Created by shoot() from PlayerPlane
    - Deleted by self.hit() or self.kill() in self.update()
    """
    _MAX_LEVEL = 0

    def __init__(self, init_position: (list, tuple),
                 speed: list[int, int]):
        BasicBullet.__init__(self, init_position=init_position,
                             speed=speed)
        self.damage = 150
        Player_Bullet_G.add(self)

    def _trans_image(self, angle: int) -> None:
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = temp

    @classmethod
    def shoot_bullets(cls, position: list[int, int], level: int):

        position1 = position[0] - 10, position[1]
        position2 = position[0] + 10, position[1]
        cls(position1, [0, -17])
        cls(position2, [0, -17])

        if level >= 2:
            position1 = position[0] - 15, position[1]
            position2 = position[0] + 15, position[1]
            cls(position1, [-5, -17])._trans_image(angle=20)
            cls(position2, [5, -17])._trans_image(angle=-20)

        if level >= 3:
            cls(position1, [-10, -17])._trans_image(angle=30)
            cls(position2, [10, -17])._trans_image(angle=-30)

    @classmethod
    def get_max_level(cls) -> int:
        return cls._MAX_LEVEL

    @classmethod
    def _init_image(cls) -> None:
        cls.IMAGE = load_image("PlayerPlane/bullet.png")
        cls._IS_SET_IMAGE = True

    @classmethod
    def _init_attrs(cls):
        cls._MAX_LEVEL = 3
        cls._IS_SET_ATTRS = True


# TODO Bullet2
class PlayerBullet2(BasicBullet):
    """ Player's Bullet 1 type,
    -> Implements StraightBullet class :
            -> SingleImageHelper
            -> pygame.sprite.Sprite
    + Created by shoot() from PlayerPlane
    - Deleted by self.hit() or self.kill() in self.update()
    """
    _MAX_LEVEL = 3

    def __init__(self, init_position: (list, tuple), level: (list, tuple)):
        if not hasattr(self, "_INIT_FLAG_SPEED") or not self.INIT_FLAG:
            raise Exception("!!!ERROR: class is not init! {}".format(self))

        self.damage = 150

        if level == 1:
            BasicBullet.__init__(self, init_position, [0, -17])
        if level == -1:
            BasicBullet.__init__(self, init_position, [0, -17])
        elif level == 2:
            BasicBullet.__init__(self, init_position, [5, -17])
            self._trans_image(angle=-20)
        elif level == -2:
            BasicBullet.__init__(self, init_position, [-5, -17])
            self._trans_image(angle=20)
        elif level == 3:
            BasicBullet.__init__(self, init_position, [10, -17])
            self._trans_image(angle=-30)
        elif level == -3:
            BasicBullet.__init__(self, init_position, [-10, -17])
            self._trans_image(angle=30)
        else:
            BasicBullet.__init__(self, init_position, [0, -17])

        pygame.sprite.Sprite.__init__(self, Player_Bullet_G)

    def _trans_image(self, angle: int) -> None:
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = temp

    @classmethod
    def get_max_level(cls) -> int:
        return cls._MAX_LEVEL

    @classmethod
    def _init_image(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._IS_SET_IMAGE:
            cls.IMAGE = load_image("PlayerPlane/bullet.png")

            cls._IS_SET_IMAGE = True

    @classmethod
    def _init_attrs(cls):
        cls._MAX_LEVEL = 3
        cls._IS_SET_ATTRS = True