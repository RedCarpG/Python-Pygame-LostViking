"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import ABC
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..generic_items.BasicPlaneEntity import BasicPlaneEntity
from ..groups import Enemy_G


class EnemyI(BasicPlaneEntity, ABC):
    """ First type of Enemy """
    SCORE = 100

    def __init__(self, position, **kwargs):
        BasicPlaneEntity.__init__(self, start_point=position, **kwargs)
        self.add(Enemy_G)

        self._speed_y = self.MAX_SPEED_DOWN

    def _action_phase(self):
        if self.rect.top < SCREEN_HEIGHT:
            self._move()
        else:
            self.kill()

    @classmethod
    def _init_attributes(cls):
        cls.MAX_HEALTH = 100
        cls.MAX_SPEED_X = 0
        cls.MAX_SPEED_UP = 0
        cls.MAX_SPEED_DOWN = 5
        cls.ACC_X = 0
        cls.ACC_UP = 0
        cls.ACC_DOWN = 0
        cls._IS_SET_ATTRS = True
