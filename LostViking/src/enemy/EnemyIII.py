"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import ABC, abstractmethod

from LostViking.src.generic_loader.sound_loader import *
from LostViking.src.constants import SCREEN
from ..generic_items.PlaneEntity import BasicSpinPlaneEntity
from enum import Enum


class EnemyIIIActionPhase(Enum):
    MoveX = 0
    Idle = 1
    MoveDown = 2


class EnemyIIIAttackPhase(Enum):
    Idle = 0
    Attack = 1


class EnemyIII(BasicSpinPlaneEntity, ABC):
    SCORE = 100

    _STAY_DURATION = 500
    _ATTACK_INTERVAL = 100

    def __init__(self, position, side='L', **kwargs):
        BasicSpinPlaneEntity.__init__(self, start_position=position, **kwargs)

        self.action_status = EnemyIIIActionPhase.MoveX
        self.attack_status = EnemyIIIAttackPhase.Idle

        self.attack_interval = pygame.time.Clock()
        self.stay_duration = pygame.time.Clock()

        if side == 'L':
            self.side = -1
            self._speed_x = self.MAX_SPEED_X
        else:
            self.side = 1
            self._speed_x = -self.MAX_SPEED_X
        self.angle = 90 * -self.side

        self._speed_y = 0

        self._count_stay_time = self._STAY_DURATION

        self._attack_speed = 100
        self._count_attack_interval = self._ATTACK_INTERVAL

    '''
    def rotate1(self,_angle):  -180<_angle<180
        if self._angle > _angle:
           self._angle -= 2
        elif self._angle < _angle:
            self._angle += 2 
        angle_ = self._angle * math.pi / 180
    '''

    def aim(self, point):
        angle = self.cal_angle(self.rect.center, point)

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

        #angle_ = self._angle * math.pi / 180

    def _action(self):
        if self.stage1_flag:
            self._entrance()
        else:

            if self._count_stay_time < 0:
                self._leave()
            else:
                self._count_stay_time -= 1

            from ..groups import Player1_G
            player_point = Player1_G.sprites()[0].rect.center
            self.aim(player_point)

            self._count_attack_interval += 1
            if self._count_attack_interval > self._attack_speed:
                self._count_attack_interval = 0
                self._shoot()

    def _leave(self):
        if self.rect.top < SCREEN.get_h():
            self.rect.move_ip(0, self._speed_y)
        else:
            self.kill()

    def _entrance(self):
        if self._speed_x * self.side <= 0:
            self._speed_x += self.ACC_X * self.side
            self.rect.move_ip(self._speed_x, 0)
        else:
            self.stage1_flag = False
            self._set_image_type("Stop")

    @classmethod
    def _init_attributes(cls):
        cls.MAX_SPEED_DOWN = cls.MAX_SPEED_UP = 1
        cls.MAX_SPEED_X = 10
        # s = t*v0/2 => t = 2s/v0
        # v0 - a * t = 0 => a = v0**2 / 2s
        cls.ACC_X = round((cls.MAX_SPEED_X ** 2) / (SCREEN.get_w()*7/4), 2)
        cls.ACC_UP = cls.ACC_DOWN = 0
        cls._IS_SET_ATTRS = True

    @abstractmethod
    def _shoot(self):
        pass


"""

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
"""
