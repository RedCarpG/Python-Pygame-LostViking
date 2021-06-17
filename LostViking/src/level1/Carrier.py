import math

from ..enemy.enemyBoss import EnemyBoss, BossActionPhase, BossAttackPhase
from ..enemy.EnemyIII import BasicEnemy, cal_angle
from ..generic_items.MovementHelper import InertialMoveHelper


class EnemyCarrier(EnemyBoss):
    MAX_INTERCEPTOR_NUMBER = 9

    def __init__(self):
        EnemyBoss.__init__(self)

        self._count_sent_interceptor_interval = 10

    def _action_attack(self, point):
        self.enter_attack_idle_phase()
        """
        if EnemyInterceptor.NUM < 9:
            if self._count_sent_interceptor_interval <= 0:
                pos = self.rect.center
                EnemyInterceptor(pos, [[pos[0], pos[1] + 300], [0, 0]])
        else:
            self.enter_attack_idle_phase()
        """
    @classmethod
    def _init_image(cls):
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._INIT_FLAG_IMAGE:
            cls._IMAGE = dict()
            from ..generic_loader.image_loader import load_image
            cls._IMAGE["Base"] = [load_image("Enemy/Carrier.png")]
            cls._IMAGE.setdefault("Normal", [load_image("Enemy/Carrier.png")])
            cls._IMAGE.setdefault("Explode", [load_image("Enemy/Carrier.png")])

    @classmethod
    def _init_sound(cls):
        if not hasattr(cls, "_INIT_FLAG_SOUND") or not cls._INIT_FLAG_SOUND:
            cls._SOUND = dict()
            from LostViking.src.generic_loader.sound_loader import load_sound
            from LostViking.src.constants import MAIN_VOLUME
            cls._SOUND.setdefault("Explode", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                              load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])

    @classmethod
    def init(cls):
        super().init()
        if not hasattr(cls, "_INIT_FLAG") or not cls._INIT_FLAG:
            cls._init_image()
            cls._init_sound()
            cls._INIT_FLAG = True

"""
class EnemyInterceptor(EnemyII, InertialMoveHelper):
    _MAX_SPEED_DOWN = 10
    _MAX_SPEED_X = 10
    NUM = 0

    def __init__(self, pos, path):
        EnemyII.__init__(self)
        InertialMoveHelper.__init__(self)
        
        self._speed_x = 0
        self._speed_y = self._MAX_SPEED_DOWN
        self._move_rad = 200
        
        self._count_action_move_x = 80
        self._count_action_idle = 15
        self._count_attack_interval = 100
        
        self._destination = path
        
        self.set_pos(pos)
        
        self._angle = 0
        
        EnemyInterceptor.NUM += 1

    def _action(self):
        if self.action_status == BossActionPhase.MoveDown:
            self._action_move_down()
        else:
            if self.action_status == BossActionPhase.MoveX:
                self._action_move_x()
            else:
                self._action_idle()
            if self.attack_status == BossAttackPhase.Attack:
                self._action_attack()
            else:
                self._action_attack_idle()
                
        if self.stage1_flag:
            self.rect.move_ip(self.speed[0], self.speed[1])
            if self.rect.collidepoint(self.path[0]):
                self.stage1_flag = False
                self.current_path = 1
                self.move_flag = False
        else:
            if self.rotate_flag:
                x = random.randint(self.rect.center[0] - self._move_rad, self.rect.center[0] + self._move_rad)
                y = random.randint(self.rect.center[1] - self._move_rad, self.rect.center[1] + self._move_rad)
                self.path[1] = [x, y]
                self.rotate(self.path[self.current_path])
                self.rotate_flag = False
                self.move_flag = True

            if self.move_flag:
                self._move_interval.tick()
                if self.rect.collidepoint(self.path[self.current_path]):
                    self._move_interval.reset()
                    self.move_flag = False
                if self._move_interval.check():
                    self.move_flag = False
                self.rect.move_ip(self.speed[0], self.speed[1])
            else:
                if abs(self.speed[0]) > 0.1 or abs(self.speed[1]) > 0.1:
                    self.brake()
                    self.rect.move_ip(self.speed[0], self.speed[1])
                self.stay_interval.tick()
                if self.stay_interval.check():
                    self.rotate_flag = True
                    self.attack_flag = True

        if self.rect.top < 0 or self.rect.bottom > SCREEN.getH() - SCREEN.getH() / 3 or self.rect.left < 0 or self.rect.right > SCREEN.get_w():
            if self.rect.top < 0:
                self.rect.top = 0
                self.path[0][1] = -self.path[0][1]
            elif self.rect.bottom > SCREEN.getH() - SCREEN.getH() / 3:
                self.rect.bottom = SCREEN.getH() - SCREEN.getH() / 3
                self.path[0][1] = 2 * (SCREEN.getH() - SCREEN.getH() / 3) - self.path[0][1]
            if self.rect.left < 0:
                self.rect.left = 0
                self.path[0][0] = -self.path[0][0]
            elif self.rect.right > SCREEN.get_w():
                self.rect.right = SCREEN.get_w()
                self.path[0][0] = 2 * SCREEN.get_w() - self.path[0][0]
            self.rotate(self.path[0])

    def _action_attack(self, point):
        if self.attack_flag:
            if random.randint(0, 10) == 0:
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
                Bullet.BULLETS.add(Bullet_Interceptor(self.rect.center, angle))
        self.attack_flag = False

    def rotate(self, point):
        self._angle = cal_angle(self.rect.center, point)
        
        angle = self._angle * math.pi / 180
        self._speed_x = float(self._MAX_SPEED_X * math.sin(angle))
        self._speed_y = float(self._MAX_SPEED_Y * math.cos(angle))
        
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.mainImage[self.image_switch], self._angle)
        self.rect = self.image.get_rect()
        self.rect.center = temp

    def __del__(self):
        EnemyInterceptor.NUM -= 1

    @classmethod
    def _init_speed(cls):
        if not hasattr(cls, "_INIT_FLAG_SPEED") or not cls._INIT_FLAG_SPEED:
            cls._MAX_SPEED_R = cls._MAX_SPEED_L = 5
            cls._MAX_SPEED_DOWN = cls._MAX_SPEED_UP = 10
            cls._INIT_FLAG_SPEED = True

    @classmethod
    def _init_acc(cls):
        if not hasattr(cls, "_INIT_FLAG_ACC") or not cls._INIT_FLAG_ACC:
            cls._ACC_L = cls._ACC_R = 0.3
            cls._ACC_DOWN = cls._ACC_UP = 0.3
            cls._INIT_FLAG_ACC = True
            
    @classmethod
    def _init_image(cls):
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._INIT_FLAG_IMAGE:
            cls.IMAGE = dict()
            from ..generic_loader.image_loader import load_image
            cls.IMAGE["Base"] = [load_image("Enemy/Interceptor.png")]
            cls.IMAGE.setdefault("Normal", [load_image("Enemy/Interceptor.png")])
            cls.IMAGE.setdefault("Explode", [load_image("Enemy/Interceptor.png")])

    @classmethod
    def init(cls):
        cls.SCORE = 500
        cls.MAX_HEALTH = 1000
        cls._init_image()
"""