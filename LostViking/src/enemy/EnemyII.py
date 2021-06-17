"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import ABC
import math
from ..generic_items.PlaneEntity import BasicSpinPlaneEntity
from ..groups import Enemy_G


class EnemyII(BasicSpinPlaneEntity, ABC):
    """ Second type of Enemy, shoot and track the player """
    SCORE = 100

    def __init__(self, position, path=None, **kwargs):
        BasicSpinPlaneEntity.__init__(self, start_position=position, **kwargs)
        self.add(Enemy_G)

        self.path = path
        self.current_path = 0

        self.rotate_flag = True
        self.move_flag = True

    def aim(self, point):
        angle = self.cal_angle(self.rect.center, point)

        self._rotate_angle(angle)

    def _rotate_angle(self, angle):
        BasicSpinPlaneEntity._rotate_angle(self, angle)
        angle = angle * math.pi / 180
        self._speed_x = float(self.MAX_SPEED_X * math.sin(angle))
        self._speed_y = float(self.MAX_SPEED_X * math.cos(angle))

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
