"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import ABC

from LostViking.src.generic_loader.sound_loader import *
import math
import abc
from LostViking.src.constants import SCREEN
from ..groups import Enemy_G, Enemy_Destroyed_G
from ..generic_items.ImageHelper import LoopImageHelper
from ..generic_items.MovementHelper import StaticMoveHelper, InertialMoveHelper


class BasicEnemy(LoopImageHelper, pygame.sprite.Sprite, ABC):
    """
    Basic class, defines general properties of enemy plane
    """

    def __init__(self):
        # Init
        if not hasattr(self, "_INIT_FLAG") or not self._INIT_FLAG:
            raise Exception("!!! ERROR class not init! {}".format(self))

        LoopImageHelper.__init__(self)
        pygame.sprite.Sprite.__init__(self, Enemy_G)

        self._health = self._MAX_HEALTH

        self.score = self._SCORE

        self.is_active = True

        self._set_image_type("Normal")

    def update(self):
        if self.is_active:
            self._switch_image()
            self._action()
        else:
            self._destroy()

    def hit(self, damage=100):
        """
        This function is called in collision detection
        """
        if self._damaged(damage):
            self.is_active = False
            self.kill()
            self.add(Enemy_Destroyed_G)
            self._image_switch = 0
            self._set_image_type("Explode")

    def _damaged(self, damage) -> bool:
        if self._health > 0:
            self._health -= damage
            return False
        else:
            self._health = 0
            return True

    def _destroy(self):
        finished = self._switch_image()
        if finished:
            self.kill()
            del self

    @abc.abstractmethod
    def _action(self):
        pass

    @classmethod
    @abc.abstractmethod
    def init(cls):
        cls._INIT_FLAG = False
        cls._MAX_HEALTH = None
        cls._SCORE = None


class EnemyI(BasicEnemy, StaticMoveHelper, ABC):
    """ First type of Enemy """

    def __init__(self, position):
        BasicEnemy.__init__(self)
        StaticMoveHelper.__init__(self)
        self.is_active = True
        self.set_pos(position)
        self._set_image_type("Normal")

    def _move(self):
        """ Move its rect by its _speed_x and _speed_y"""
        self.rect.top += self._MAX_SPEED_DOWN

    def _action(self):
        if self.rect.top < SCREEN.get_h():
            self._move()
        else:
            self.kill()


class EnemyII(BasicEnemy, InertialMoveHelper, ABC):
    """ Second type of Enemy, shoot and track the player """

    def __init__(self, pos, path=None):
        BasicEnemy.__init__(self)
        InertialMoveHelper.__init__(self)
        self.angle = 0
        self.path = path
        self.current_path = 0

        self.rotate_flag = True
        self.move_flag = True

        self.set_pos(pos)

    def _switch_image(self, switch_rate=5):
        is_finished = LoopImageHelper._switch_image(self)
        temp = self.rect.center
        self.image = pygame.transform.rotate(self._main_image_type[self._image_switch], self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = temp
        return is_finished

    def aim(self, point):
        angle = _cal_angle(self.rect.center, point)

        self._rotate_angle(angle)

    def _rotate_angle(self, angle):
        self.angle = angle
        angle = angle * math.pi / 180
        self._speed_x = float(self._MAX_SPEED_L * math.sin(angle))
        self._speed_y = float(self._MAX_SPEED_DOWN * math.cos(angle))
        temp = self.rect.center
        self.image = pygame.transform.rotate(self._main_image_type[self._image_switch], self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = temp

    def _action(self):
        if self.move_flag:
            self._move()

        if self.rotate_flag:
            self.aim(self.path[self.current_path])
            self.rotate_flag = False
            self.move_flag = True

        if self.rect.collidepoint(self.path[self.current_path]):
            if self.current_path < len(self.path):
                self.current_path += 1
                self.rotate_flag = True
                self.move_flag = False
            else:
                self.kill()


class EnemyIII(BasicEnemy, InertialMoveHelper, ABC):

    def __init__(self, pos, side='L'):
        BasicEnemy.__init__(self)
        InertialMoveHelper.__init__(self)

        self.set_pos(pos)

        self.stage1_flag = True
        self.stage2_flag = False
        self.stage3_flag = False

        self.attack_interval = pygame.time.Clock()
        self.stay_duration = pygame.time.Clock()

        if side == 'L':
            self.side = -1
            self._speed_x = self._MAX_SPEED_L
            self.angle = 90
        else:
            self.side = 1
            self._speed_x = -self._MAX_SPEED_L

        self.angle = 90 * -self.side

        self._speed_y = self._MAX_SPEED_DOWN

        self._stay_time = 500

        self._attack_speed = 100
        self._attack_interval_count = 0

    '''
    def rotate1(self,angle):  -180<angle<180
        if self.angle > angle:
           self.angle -= 2
        elif self.angle < angle:
            self.angle += 2 
        angle_ = self.angle * math.pi / 180
    '''

    def _switch_image(self, switch_rate=5):
        is_finished = LoopImageHelper._switch_image(self)
        temp = self.rect.center
        self.image = pygame.transform.rotate(self._main_image_type[self._image_switch], self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = temp
        return is_finished

    def aim(self, point):
        angle = _cal_angle(self.rect.center, point)

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

        #angle_ = self.angle * math.pi / 180

    def _action(self):
        if self.stage1_flag:
            self._entrance()
        else:

            if self._stay_time < 0:
                self._leave()
            else:
                self._stay_time -= 1

            from ..groups import Player1_G
            player_point = Player1_G.sprites()[0].rect.center
            self.aim(player_point)

            self._attack_interval_count += 1
            if self._attack_interval_count > self._attack_speed:
                self._attack_interval_count = 0
                self._shoot()

    def _leave(self):
        if self.rect.top < SCREEN.get_h():
            self.rect.move_ip(0, self._speed_y)
        else:
            self.kill()

    def _entrance(self):
        if self._speed_x * self.side <= 0:
            self._speed_x += self._ACC_L * self.side
            self.rect.move_ip(self._speed_x, 0)
        else:
            self.stage1_flag = False
            self._set_image_type("Stop")

    @classmethod
    def _init_speed(cls):
        if not hasattr(cls, "_INIT_FLAG_SPEED") or not cls._INIT_FLAG_SPEED:
            cls._MAX_SPEED_R = cls._MAX_SPEED_L = 10
            cls._MAX_SPEED_DOWN = cls._MAX_SPEED_UP = 1
            cls._INIT_FLAG_SPEED = True

    @classmethod
    def _init_acc(cls):
        if not hasattr(cls, "_INIT_FLAG_SPEED") or not cls._INIT_FLAG_SPEED:
            cls._MAX_SPEED_L = 0
            cls._INIT_FLAG_SPEED = False
            cls._init_speed()
        if not hasattr(cls, "_INIT_FLAG_ACC") or not cls._INIT_FLAG_ACC:
            cls._ACC_L = cls._ACC_R = round((cls._MAX_SPEED_L ** 2) / (SCREEN.get_w()*7/4), 2)
            cls._INIT_FLAG_ACC = True
        # s = t*v0/2 => t = 2s/v0
        # v0 - a * t = 0 => a = v0**2 / 2s

    @abc.abstractmethod
    def _shoot(self):
        pass


def _cal_angle(point_rect, point):
    if point_rect[1] == point[1]:
        if point[0] > point_rect[0]:
            angle = 90
        else:
            angle = -90
    elif point_rect[0] == point[0]:
        if point[1] > point_rect[1]:
            angle = 0
        else:
            angle = 180
    else:
        angle = math.atan((point[0] - point_rect[0]) / (point[1] - point_rect[1]))
        angle = angle * 360 / 2 / math.pi
        if point_rect[1] > point[1]:
            if point_rect[0] < point[0]:
                angle += 180
            else:
                angle -= 180
    return angle


"""
class Enemy_Boss(Enemy):
    BOSS_Score = 5000
    BOSS_MaxHealth = 30000

    def __init__(self):
        Enemy.__init__(self)
        self.image_switch = 0
        self.mainImage = None
        self.image = self.mainImage[0]
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN.get_w() // 2, -self.rect.height]
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
"""
