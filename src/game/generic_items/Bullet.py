
from collections.abc import Sequence
from abc import ABC, abstractmethod
import pygame
from pygame import Surface, Vector2

from src.setting import SCREEN_HEIGHT, SCREEN_WIDTH
from src.util import if_in_screen
from src.util.type import Pos

from src.game.groups import G_Bullet


class Bullet(pygame.sprite.Sprite, ABC):
    """ Basic Bullet Class
    """

    def __init__(self,
                 pos: Pos,
                 speed: Vector2,
                 image: pygame.Surface, **kwargs):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(center=pos.to_list())
        self.speed = speed

        G_Bullet.add(self)

    def update(self):
        # General update method for bullets
        if if_in_screen(self.rect):
            self.kill()
        else:
            self._move()

    def hit(self):
        # General get hit method for bullets
        self.kill()
        del self

    def _move(self):
        self.rect.move_ip(self.speed.x, self.speed.y)
