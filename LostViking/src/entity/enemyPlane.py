from LostViking.src.generic.image import *
from LostViking.src.generic.sound import *
import math
import abc
from LostViking.src.GLOBAL import SCREEN
from LostViking.src.generic.mytime import *


class Enemy(pygame.sprite.Sprite):

    Enemy_G = pygame.sprite.Group()
    EnemyHit_G = pygame.sprite.Group()
    EnemyDie_G = pygame.sprite.Group()
    BOSS = pygame.sprite.GroupSingle()

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class EnemyI(Enemy):

    def __init__(self, position):
        Enemy.__init__(self)
        self.image_switch = 0
        self.image = self.mainImage[0]
        self.rect = self.image.get_rect()
        self.active = True
        self.score = 0
        self.setPos(position)
        self.image_switch_interval = MYTIME(1)
        self.death_time = MYTIME(6)
        self.speed = [0, 0]
        self.ENEMYS.add(self)

    def update(self):
        self.change_image()
        if self.rect.top < SCREEN.getH():
            self.rect.top += self.speed[1]

    def hit(self, damage=100):
        self.health -= damage
        if self.health <= 0:
            self.active = False

    def destroy(self):
        self.image_switch = 0
        self.mainImage = self.crashImage
        self.destroySound.stop()
        self.destroySound.play()

    def change_image(self):
        self.image_switch_interval.tick()
        if self.image_switch_interval.check():
            self.image_switch = (self.image_switch + 1) % len(self.mainImage)
            self.image = self.mainImage[self.image_switch]

    def setPos(self, point):
        self.rect.center = point

    @abc.abstractmethod
    def LOAD(self):
        pass


class EnemyII(EnemyI):
    def __init__(self, pos, path):
        EnemyI.__init__(self, pos)
        self.angle = 0
        self.path = path
        self.current_path = 0
        self.rotate_flag = True

    def change_image(self):
        self.image_switch_interval.tick()
        if self.image_switch_interval.check():
            self.image_switch = (self.image_switch + 1) % len(self.mainImage)
            self.image = pygame.transform.rotate(self.mainImage[self.image_switch], self.angle)

    def update(self):
        self.change_image()
        self.action()

    def rotate(self, point):
        if self.rect.center[1] == point[1]:
            if point[0] > self.rect.center[0]:
                angle = 90
            else:
                angle = -90
        elif self.rect.center[0] == point[0]:
            if point[1] > self.rect.center[1]:
                angle = 0
            else:
                angle = 180
        else:
            angle = math.atan((point[0] - self.rect.center[0]) / (point[1] - self.rect.center[1]))
            angle = angle * 360 / 2 / math.pi
            if self.rect.center[1] > point[1]:
                if self.rect.center[0] < point[0]:
                    angle += 180
                else:
                    angle -= 180
        self.angle = angle
        angle = angle * math.pi / 180
        self.speed = [float(self.MaxSpeed * math.sin(angle)), float(self.MaxSpeed * math.cos(angle))]
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.mainImage[self.image_switch], self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = temp

    def rotate_angle(self, angle):
        self.angle = angle
        angle = angle * math.pi / 180
        self.speed = [float(self.MaxSpeed * math.sin(angle)), float(self.MaxSpeed * math.cos(angle))]
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.mainImage[self.image_switch], self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = temp

    def action(self):
        if self.move_flag:
            self.rect.move_ip(self.speed[0], self.speed[1])
        if self.rotate_flag:
            self.rotate(self.path[self.current_path])
            self.rotate_flag = False
            self.move_flag = True
        if self.rect.collidepoint(self.path[self.current_path]):
            if self.current_path < len(self.path):
                self.current_path += 1
                self.rotate_flag = True
                self.move_flag = False
            else:
                self.kill()

    @abc.abstractmethod
    def LOAD(self):
        pass


class EnemyIII(EnemyI):
    def __init__(self, pos):
        EnemyI.__init__(self, pos)
        self.angle = 0
        self.entrance_flag = True
        self.stay_duration = MYTIME(500)
        self.attack_interval = MYTIME(100)

    def change_image(self):
        self.image_switch_interval.tick()
        if self.image_switch_interval.check():
            self.image_switch = (self.image_switch + 1) % len(self.mainImage)
            temp = self.rect.center
            self.image = pygame.transform.rotate(self.mainImage[self.image_switch], self.angle)

            self.rect = self.image.get_rect()
            self.rect.center = temp

    def rotate(self, point):
        if self.rect.center[1] == point[1]:
            if point[0] > self.rect.center[0]:
                angle = 90
            else:
                angle = -90
        elif self.rect.center[0] == point[0]:
            if point[1] > self.rect.center[1]:
                angle = 0
            else:
                angle = 180
        else:
            angle = math.atan((point[0] - self.rect.center[0]) / (point[1] - self.rect.center[1]))
            angle = angle * 360 / 2 / math.pi
            if self.rect.center[1] > point[1]:
                if self.rect.center[0] < point[0]:
                    angle += 180
                else:
                    angle -= 180

        if self.rect.center[0] > point[0] and self.angle > 90:
            self.angle += 2
        elif self.rect.center[0] < point[0] and self.angle < -90:
            self.angle -= 2
        elif self.angle > angle:
            self.angle -= 2
        elif self.angle < angle:
            self.angle += 2

        if self.angle < -180:
            self.angle = 180
        if self.angle > 180:
            self.angle = -180

        angle_ = self.angle * math.pi / 180

    '''
    def rotate1(self,angle):  -180<angle<180
        if self.angle > angle:
           self.angle -= 2
        elif self.angle < angle:
            self.angle += 2 
        angle_ = self.angle * math.pi / 180
    '''

    def update(self, player_point):
        self.change_image()
        if self.entrance_flag:
            self.entrance()
        else:
            self.action(player_point)
            if self.stay_duration.tick() > 500:
                self.leave()

    def action(self, player_point):
        self.attack_interval.tick()
        if self.attack_interval.check():
            self.shoot()
        self.rotate(player_point)

    def leave(self):
        if self.rect.top < SCREEN.getH():
            self.rect.move_ip(0, self.speed[1])
        else:
            self.kill()

    @abc.abstractmethod
    def entrance(self):
        pass

    @abc.abstractmethod
    def LOAD(self):
        pass


class Enemy_Boss(Enemy):
    BOSS_Score = 5000
    BOSS_MaxHealth = 30000

    def __init__(self):
        Enemy.__init__(self)
        self.image_switch = 0
        self.image = self.mainImage[0]
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN.getW() // 2, -self.rect.height]
        self.active = True
        self.image_switch
        self.maxHealth = self.BOSS_MaxHealth
        self.health = self.BOSS_MaxHealth
        self.score = self.BOSS_Score
        self.image_switch_interval = MYTIME(60)
        self.BOSS.add(self)

    def update(self, point):
        self.change_image()
        self.action()
        self.attack(point)

    def hit(self, damage=100):
        self.health -= damage
        if self.health <= 0:
            self.active = False

    def destroy(self):
        self.image_switch = 0
        self.mainImage = self.crashImage
        self.destroySound.stop()
        self.destroySound.play()

    def change_image(self):
        self.image_switch_interval.tick()
        if self.image_switch_interval.check():
            self.image_switch = (self.image_switch + 1) % len(self.mainImage)
            self.image = self.mainImage[self.image_switch]

    @abc.abstractmethod
    def action(self):
        pass

    @abc.abstractmethod
    def LOAD(self):
        pass


class Enemy_ShooterI(EnemyI):
    def __init__(self, pos):
        EnemyI.__init__(self, pos)

    def update(self):
        self.change_image()
        self.action()
        self.shoot()

    def shoot(self):
        if self.whenShoot():
            self.attackSound.stop()
            self.attackSound.play()
            self.bullets.add(self.creatBullet())

    def shoot_blit(self):
        if self.attackImage:
            if self.attack_flag:
                if self.attack_animation < len(self.attackImage):
                    image = self.transImage(self.attackImage, self.attack_animation)
                    rect = image.get_rect()
                    rect.center = self.rect.center
                    # self.screen.blit(image, rect)
                else:
                    self.attack_animation = 0
                    self.attack_flag = False
                    self.attackSound.stop()
                    self.attackSound.play()
                    return True
            return False
        return True

    @abc.abstractmethod
    def whenShoot(self):
        pass

    @abc.abstractmethod
    def creatBullet(self):
        pass


class Enemy_ShooterII(Enemy_ShooterI, EnemyIII):
    def __init__(self, pos, bullets):
        Enemy_ShooterI.__init__(self, pos, bullets)
        EnemyII.__init__(self, pos)

    def update(self, point):
        self.change_image()
        self.action()
        self.spin(point)
        self.shoot()

    def spin(self, point):
        if not self.move_flag:
            self.rotate(A)

    def action(self):
        pass

    @abc.abstractmethod
    def creatBullet(self):
        pass

    @abc.abstractmethod
    def whenShoot(self):
        pass

    @abc.abstractmethod
    def action(self):
        pass
