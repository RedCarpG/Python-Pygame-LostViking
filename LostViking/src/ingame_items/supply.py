from LostViking.src.generic_loader.image_loader import *
from enum import Enum
import abc
import random
from ..player.PlayerWeapon import PlayerBullet1


class SUPPLY_TYPE(Enum):
    Life = 0
    Bullet1 = 1
    Bomb = 2


class Supply(pygame.sprite.Sprite):
    def __init__(self, position=[-1, -1]):
        pygame.sprite.Sprite.__init__(self)
        self.setImage()
        self.rect = self.image.get_rect()
        self.width = [0, SCREEN.get_w() - self.rect.width]
        self.height = [SCREEN.getH() // 3, 2 * SCREEN.getH() // 3]
        self.setPos(position)
        self.speed = [2, 2]
        self.direction = [random.randint(-1, 1), random.randint(-1, 1)]
        self.lastTime = 2000
        self.score = 1000
        self.type = None

    def setPos(self, point=[-1, -1]):
        if point == [-1, -1]:
            self.rect.left, self.rect.top = [random.randint(0, SCREEN.get_w() - self.rect.width),
                                             random.randint(-1 * SCREEN.getH(), 0 - self.rect.height)]
        else:
            self.rect.left, self.rect.top = point

    def update(self):
        if self.rect.top > 0:
            self.lastTime -= 1
            if not self.lastTime:
                self.kill()
        self.move()

    @abc.abstractmethod
    def setImage(self):
        pass

    @abc.abstractmethod
    def catched(self, player):
        pass

    def move(self):
        if self.rect.left <= self.width[0]:
            self.direction[0] = 1
        elif self.rect.left >= self.width[1]:
            self.direction[0] = -1
        if self.rect.top <= self.height[0]:
            self.direction[1] = 1
        elif self.rect.top >= self.height[1]:
            self.direction[1] = -1
        self.rect.move_ip(self.speed[0] * self.direction[0], self.speed[1] * self.direction[1])

    @staticmethod
    def create(type, postion=[-1, -1]):
        if type == SUPPLY_TYPE.Life:
            return Supply_Life(postion)
        elif type == SUPPLY_TYPE.Bullet1:
            return Supply_Bullet1(postion)
        elif type == SUPPLY_TYPE.Bomb:
            return Supply_Bomb(postion)
        return Supply_Bullet1(postion)


class Supply_Bullet1(Supply):
    def __init__(self, position=[-1, -1]):
        Supply.__init__(self, position)
        self.type = SUPPLY_TYPE.Bullet1

    def setImage(self):
        self.image = SUPPLY_IMAGE["Bullet"]

    def catched(self, player):
        player.set_bullet_type(PlayerBulletType.Bullet1)
        self.kill()


class Supply_Bomb(Supply):
    def __init__(self, position=[-1, -1]):
        Supply.__init__(self, position)
        self.type = SUPPLY_TYPE.Bomb

    def setImage(self):
        self.image = SUPPLY_IMAGE["Bomb"]

    def catched(self, player):
        if G.BOMB < 5:
            G.BOMB += 1
        self.kill()


class Supply_Life(Supply):
    def __init__(self, position=[-1, -1]):
        Supply.__init__(self, position)
        self.type = SUPPLY_TYPE.Life

    def setImage(self):
        self.image = SUPPLY_IMAGE["Life"]

    def catched(self, player):
        if G.LIFE < 5:
            G.LIFE += 1
        self.kill()
