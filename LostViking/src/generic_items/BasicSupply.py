from enum import Enum
import abc
import random

from ..generic_items.ImageEntity import LoopImageEntity
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..groups import Supply_G


class SupplyType(Enum):
    Life = 0
    Bullet1 = 1
    Bomb = 2


class SupplyStatus(Enum):
    Enter = 0
    Stay = 1
    Move = 2
    Leave = 3


class BasicSupply(LoopImageEntity, abc.ABC):
    STAY_PHASE_DURATION = 2000
    MOVE_PHASE_DURATION = 1000
    SPEED_CHANGE_DURATION = 30
    MAX_SPEED_STAY = 2
    ACC = 0.1
    MAX_SPEED_MOVE = 3
    SCORE = 1000

    def __init__(self, position=None):
        # Check Initialization
        if not hasattr(self, "INIT_FLAG") or not self.INIT_FLAG:
            raise Exception("!!!ERROR: Class is not init! {}".format(self.__class__))
        LoopImageEntity.__init__(self)
        self.add(Supply_G)

        self.is_active = True

        self.direction_x = random.choice([1, -1])
        self.direction_y = random.choice([1, -1])
        self._speed_x = 0
        self._speed_y = 0

        self.status = SupplyStatus.Stay
        self._count_status_duration = self.STAY_PHASE_DURATION
        self._count_speed_change_duration = self.SPEED_CHANGE_DURATION

        self.set_pos(position)

        self.type = None

    def update(self):
        # image_loop_finished = self._switch_image()
        if self.is_active:
            self._action_phase()
        else:
            self._destroy_phase()

    @abc.abstractmethod
    def get_by_player(self, player):
        pass

    # --------------- Main Status --------------- #
    def _action_phase(self):
        if self.status == SupplyStatus.Enter:
            self._action_enter()
        elif self.status == SupplyStatus.Stay:
            self._action_stay()
        elif self.status == SupplyStatus.Move:
            self._action_move()
        else:
            self._action_leave()

    def _destroy_phase(self):
        self.kill()

    # --------------- Action Status --------------- #

    def enter_action_enter_phase(self):
        self.status = SupplyStatus.Enter
        self._speed_y = self.MAX_SPEED_STAY
        self._speed_x = 0

    def _action_enter(self):
        self._move()
        if self.rect.bottom > SCREEN_HEIGHT / 3:
            if self._deceleration_y():
                self.enter_action_stay_phase()

    def enter_action_stay_phase(self):
        self._count_speed_change_duration = self.SPEED_CHANGE_DURATION
        self._count_status_duration = self.STAY_PHASE_DURATION
        self.status = SupplyStatus.Stay
        self.direction_x = random.choice([1, -1])
        self.direction_y = random.choice([1, -1])

    def _action_stay(self):
        if self._count_status_duration:
            self._count_status_duration -= 1
        else:
            self.enter_action_move_phase()

    def enter_action_move_phase(self):
        self._count_speed_change_duration = self.SPEED_CHANGE_DURATION
        self._count_status_duration = self.MOVE_PHASE_DURATION
        self.status = SupplyStatus.Move
        self._speed_y = random.randint(-self.MAX_SPEED_MOVE, self.MAX_SPEED_MOVE)
        self._speed_x = random.randint(-self.MAX_SPEED_MOVE, self.MAX_SPEED_MOVE)

    def _action_move(self):
        self._move()
        if self._count_speed_change_duration:
            self._speed_x = accelerate(self._speed_x, self.MAX_SPEED_STAY, self.direction_x, self.ACC)
            self._speed_y = accelerate(self._speed_y, self.MAX_SPEED_STAY, self.direction_y, self.ACC)
            self._count_speed_change_duration -= 1
        else:
            self._speed_x = decelerate(self._speed_x, self.ACC)
            self._speed_y = decelerate(self._speed_y, self.ACC)
            # self._deceleration_y()
            # self._deceleration_x()
            if self._speed_y == 0 and self._speed_x == 0:
                self._count_speed_change_duration = self.SPEED_CHANGE_DURATION
                self.direction_x = random.choice([1, -1])
                self.direction_y = random.choice([1, -1])
        if self.rect.bottom > SCREEN_HEIGHT * 2 / 3 and self._speed_y > 0:
            self._speed_y = -self._speed_y
            self.direction_y = -self.direction_y
        if self._count_status_duration:
            self._count_status_duration -= 1
        else:
            self.enter_action_leave_phase()

    def enter_action_leave_phase(self):
        self.status = SupplyStatus.Leave
        self._speed_y = self.MAX_SPEED_MOVE

    def _action_leave(self):
        if self.rect.top < SCREEN_HEIGHT:
            self._move()
        else:
            self.kill()

    # --------------- Behavior --------------- #
    def _move(self):
        if self.rect.left <= 0 and self._speed_x < 0:
            self._speed_x = -self._speed_x
            self.direction_x = -self.direction_x
        elif self.rect.right >= SCREEN_WIDTH and self._speed_x > 0:
            self._speed_x = -self._speed_x
            self.direction_x = -self.direction_x
        if self.rect.top <= 0 and self._speed_y < 0:
            self._speed_y = -self._speed_y
            self.direction_y = -self.direction_y
        self.rect.move_ip(self._speed_x, self._speed_y)

    def set_pos(self, point):
        if point is None:
            self.rect.left, self.rect.top = [random.randint(0, SCREEN_WIDTH - self.rect.width),
                                             random.randint(-1 * SCREEN_HEIGHT, 0 - self.rect.height)]
        else:
            self.rect.center = point

    # --------------- Deceleration --------------- #
    def _deceleration_x(self) -> bool:
        """ Decrease the _speed_x or _speed_y to 0 automatically
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        if self._speed_x > 0:  # If it is moving right, decelerate by _ACC_L
            self._speed_x -= self.ACC
            if self._speed_x <= 0:
                self._speed_x = 0
                return True
        elif self._speed_x < 0:  # If it is moving left, decelerate by _ACC_R
            self._speed_x += self.ACC
            if self._speed_x >= 0:
                self._speed_x = 0
                return True
        return False

    def _deceleration_y(self) -> bool:
        """ Decrease the _speed_x or _speed_y to 0 automatically
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        if self._speed_y > 0:  # If it is moving down, decelerate by _ACC_UP
            self._speed_y -= self.ACC
            if self._speed_y <= 0:
                self._speed_y = 0
                return True
        elif self._speed_y < 0:  # If it is moving up, decelerate by _ACC_DOWN
            self._speed_y += self.ACC
            if self._speed_y >= 0:
                self._speed_y = 0
                return True
        return False

    # --------------- Init --------------- #
    @classmethod
    def init(cls):
        cls._init_image()
        cls.INIT_FLAG = True


def accelerate(speed, max_speed, direction, acc):
    if direction == 1:
        if speed < max_speed:
            speed += acc
        else:
            speed = max_speed
    else:
        if speed > -max_speed:
            speed -= acc
        else:
            speed = -max_speed
    return speed


def decelerate(speed, acc):
    if speed > 0:  # If it is moving down, decelerate by _ACC_UP
        speed -= acc
        if speed <= 0:
            speed = 0
    elif speed < 0:  # If it is moving up, decelerate by _ACC_DOWN
        speed += acc
        if speed >= 0:
            speed = 0
    return speed
