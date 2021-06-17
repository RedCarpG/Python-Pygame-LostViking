"""
Enemy Basic abstract classes, which defines its general behaviors,
Initialization should be made in the implementation of the class
"""
from abc import ABC
from LostViking.src.constants import SCREEN
from ..generic_items.PlaneEntity import BasicPlaneEntity


class EnemyI(BasicPlaneEntity, ABC):
    """ First type of Enemy """
    SCORE = 100

    def __init__(self, position, **kwargs):
        BasicPlaneEntity.__init__(self, start_position=position, **kwargs)

        self._speed_y = self.MAX_SPEED_DOWN

    def _action(self):
        if self.rect.top < SCREEN.get_h():
            self._move()
        else:
            self.kill()
