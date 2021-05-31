import pygame
from enum import Enum
from LostViking.src.GLOBAL import *


class PlayerBulletType(Enum):
    Bullet1 = 0
    Bullet2 = 1


class PlayerBullet1(pygame.sprite.Sprite):
    PLAYER_BULLET_SPEED = 17

    def __init__(self, pos, lever):
        pygame.sprite.Sprite.__init__(self)
        self.damage = 150
        self.image = BULLET_IMAGE["Viking_Bullet"]
        self.MaxSpeed = self.PLAYER_BULLET_SPEED
        if lever == 1:
            self.speed = [0.5, -17]
        if lever == -1:
            self.speed = [-0.5, -17]
        elif lever == 2:
            self.speed = [5.8, -16]
            self.image = pygame.transform.rotate(self.image, -20)
        elif lever == -2:
            self.speed = [-5.8, -16]
            self.image = pygame.transform.rotate(self.image, 20)
        elif lever == 3:
            self.speed = [6, -15.8]
            self.image = pygame.transform.rotate(self.image, -21)
        elif lever == -3:
            self.speed = [-6, -15.8]
            self.image = pygame.transform.rotate(self.image, 21)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if self.whenkill():
            self.kill()
        else:
            self.move()

    def move(self):
        self.rect.move_ip(self.speed[0], self.speed[1])

    def whenkill(self):
        if self.rect.top > SCREEN.getH() \
                or self.rect.bottom < 50 or self.rect.right < 0 \
                or self.rect.left > SCREEN.getW():
            return True
        return False


class PlayerNucBomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = BULLET_IMAGE["Viking_Bullet"]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.accelerate = 0.2
        self.speed = -2
        self.explode_flag = False
        self.active = True

    def update(self):
        if self.active:
            if self.rect.bottom > SCREEN.getH() // 3:
                self.move()
            else:
                self.explode_flag = True
        else:
            self.kill()

    def move(self):
        self.rect.top -= self.speed
        self.speed += self.accelerate
