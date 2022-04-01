"""
Player controllable object
"""
from collections.abc import Sequence
import pygame
from abc import ABC, abstractmethod
from src.helper.image import get_image
from src.game.generic_items.Bullet import Bullet
from src.game.groups import G_Player_Bullet
from src.util.type import Pos


class PlayerWeapon(ABC):
    LEVEL_MAX = 3

    BASIC_DMG = 150

    def __init__(self):
        self._damage = self.BASIC_DMG
        self._inc_dmg = 25
        self._level = 1
        self._bullet_type = None

    @property
    def level(self) -> int:
        return self._level

    def level_up(self) -> None:
        if self._level >= self.LEVEL_MAX:
            return
        self._level += 1
        self._damage += self._inc_dmg

    def level_down(self) -> None:
        if self._level <= 0:
            return
        self._level -= 1
        self._damage -= self._inc_dmg

    def reset_level(self) -> None:
        self._level = 0
        self._damage = self.BASIC_DMG

    @property
    def bullet(self):
        return self._bullet_type

    def set_bullet_type(self, bullet_type):
        self._bullet_type = bullet_type

    @abstractmethod
    def shoot(self, pos: Pos):
        return None


class PlayerWeaponViking(PlayerWeapon):

    BASIC_DMG = 150

    def __init__(self):
        PlayerWeapon.__init__(self)
        self._bullet_type = PlayerBulletViking
        self._inc_dmg = 150

    def shoot(self, pos: Pos):
        position1 = pos.move_x(-10)
        position2 = pos.move_x(10)
        self._bullet_type(position1, pygame.Vector2(0, -17), self._damage)
        self._bullet_type(position2, pygame.Vector2(0, -17), self._damage)

        if self._level >= 2:
            position1 = pos.move_x(-10)
            position2 = pos.move_x(10)
            self._bullet_type(
                position1, pygame.Vector2(-5, -17), self._damage, angle=20)
            self._bullet_type(position2, pygame.Vector2(
                5, -17), self._damage, angle=-20)

        if self._level >= 3:
            self._bullet_type(
                position1, pygame.Vector2(-10, -17), self._damage, angle=30)
            self._bullet_type(position2, pygame.Vector2(
                10, -17), self._damage, angle=-30)


class PlayerBulletViking(Bullet):

    def __init__(self, pos: Pos,
                 speed: Sequence[int, int],
                 damage,
                 angle=None):
        Bullet.__init__(self, pos=pos, speed=speed,
                        image=get_image("PlayerPlane/bullet.png"))
        self.damage = damage
        if angle:
            self._rotate(angle)
        G_Player_Bullet.add(self)

    def _rotate(self, angle: int) -> None:
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=temp)
