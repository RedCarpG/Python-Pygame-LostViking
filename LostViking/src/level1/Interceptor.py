from ..enemy.EnemyII import EnemyII
from ..groups import Player1_G
from .Phoenix import BulletPhoenix
from ..constants import SCREEN
import random


class EnemyInterceptor(EnemyII):
    MOVE_RAD = 300

    NUM = 0

    MOVE_BOTTOM_LIMIT = int(SCREEN.get_h() * 2 / 3)
    MOVE_LEFT_LIMIT = int(SCREEN.get_w() / 5)
    MOVE_RIGHT_LIMIT = int(SCREEN.get_w() * 4 / 5)
    MOVE_UP_LIMIT = int(SCREEN.get_h() / 5)

    def __init__(self, position, path):
        EnemyII.__init__(self, position, path)

        self._speed_x = 0
        self._speed_y = self.MAX_SPEED_X

        EnemyInterceptor.NUM += 1

    def find_new_path(self):
        x = random.randint(max(self.MOVE_LEFT_LIMIT, self.rect.center[0] - self.MOVE_RAD),
                           min(self.MOVE_RIGHT_LIMIT, self.rect.center[0] + self.MOVE_RAD))
        y = random.randint(max(self.MOVE_UP_LIMIT, self.rect.center[1] - self.MOVE_RAD),
                           min(self.MOVE_BOTTOM_LIMIT, self.rect.center[1] + self.MOVE_RAD))
        self.path[0] = [x, y]

    def enter_action_move_phase(self):
        self.find_new_path()
        super().enter_action_move_phase()

    def _action_decelerate(self):
        self._move()
        self._deceleration_y()
        self._deceleration_x()
        if self._speed_y == 0 and self._speed_y == 0:
            self.enter_action_idle_phase()

    def _move(self) -> None:
        if self.rect.top < 0:
            self.rect.top = 0
            self._speed_y = -self._speed_y
            self.angle = 180 - self.angle
            # self.path[0][1] = -self.path[0][1]
            # self.aim(self.path[0])
        elif self.rect.bottom > self.MOVE_BOTTOM_LIMIT:
            self.rect.bottom = self.MOVE_BOTTOM_LIMIT
            self._speed_y = -self._speed_y
            self.angle = 180 - self.angle
            # self.path[0][1] = self.path[0][1] - self.MOVE_BOTTOM_LIMIT
            # self.aim(self.path[0])
        if self.rect.left < 0:
            self.rect.left = 0
            self._speed_x = -self._speed_x
            self.angle = -self.angle
            #self.path[0][0] = -self.path[0][0]
            # self.aim(self.path[0])
        elif self.rect.right > SCREEN.get_w():
            self.rect.right = SCREEN.get_w()
            self._speed_x = -self._speed_x
            self.angle = -self.angle
            #self.path[0][0] = 2 * SCREEN.get_w() - self.path[0][0]
            # self.aim(self.path[0])
        self.rect.move_ip(self._speed_x, self._speed_y)

    def _action_attack(self):
        if random.randint(0, 10) == 0:
            player_point = Player1_G.sprites()[0].rect.center
            angle = self.cal_angle(self.rect.center, player_point)
            BulletPhoenix(self.rect.center, angle)

    def __del__(self):
        EnemyInterceptor.NUM -= 1

    @classmethod
    def _init_image(cls):
        cls.IMAGE = dict()
        from ..generic_loader.image_loader import load_image
        cls.IMAGE["BASE"] = [load_image("Enemy/Interceptor.png")]
        cls.IMAGE["IDLE"] = [load_image("Enemy/Interceptor.png")]
        cls.IMAGE["EXPLODE"] = [load_image("Enemy/Interceptor.png")]
        cls._IS_SET_IMAGE = True

    @classmethod
    def _init_attributes(cls):
        super()._init_attributes()
        cls._STAY_DURATION = 10
        cls.MAX_SPEED_X = 10
        cls.SCORE = 200
        cls.MAX_HEALTH = 200
