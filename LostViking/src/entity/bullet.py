from GLOBAL import *
from LostViking.src.generic.image import *
import math
import abc


class Bullet(pygame.sprite.Sprite):
    BULLETS = pygame.sprite.Group()

    def __init__(self, position, angle=0):
        pygame.sprite.Sprite.__init__(self)

        self.setImage()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.angle = angle
        angle = angle * math.pi / 180.0
        self.speed = [float(self.MaxSpeed * math.sin(angle)), float(self.MaxSpeed * math.cos(angle))]
        self.image = pygame.transform.rotate(self.image, self.angle)

    def update(self):
        if self.whenkill():
            self.kill()
        else:
            self.move()

    def move(self):
        self.rect.move_ip(self.speed[0], self.speed[1])

    def transImage(self):
        temp = self.rect.center
        image_ = pygame.transform.rotate(self.image, self.angle)
        self.rect = image_.get_rect()
        self.rect.center = temp
        return image_

    def hit(self):
        self.kill()

    def whenkill(self):
        if self.rect.top > SCREEN.getH() \
                or self.rect.bottom < 50 or self.rect.right < 0 \
                or self.rect.left > SCREEN.getW():
            return True
        return False

    @abc.abstractmethod
    def setImage(self):
        pass


class Bullet_Viking(Bullet):
    VIKING_BULLET_SPEED = 15

    def __init__(self, position, angle):
        self.MaxSpeed = self.VIKING_BULLET_SPEED
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
