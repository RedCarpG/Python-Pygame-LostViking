"""
Player controllable object
"""
import pygame

from LostViking.src.generic_loader.image_loader import load_image
from LostViking.src.generic_items.bullet import BasicBullet

Player_Bullet_G = pygame.sprite.Group()


class PlayerBullet1(BasicBullet):
    """ Player's Bullet 1 type,
    -> Implements StraightBullet class :
            -> SingleImageHelper
            -> pygame.sprite.Sprite
    + Created by shoot() from MyPlane
    - Deleted by self.hit() or self.kill() in self.update()
    """

    def __init__(self, init_position: (list, tuple), level: (list, tuple)):

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

    def _trans_image(self, angle):
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = temp

    @classmethod
    def init_image(cls):
        cls._IMAGE = load_image("MyPlane/bullet.png")

        cls._INIT_FLAG = True

