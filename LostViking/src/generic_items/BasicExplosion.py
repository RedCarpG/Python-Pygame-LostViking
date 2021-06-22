from abc import ABC
from .ImageEntity import LoopImageEntity
from ..groups import Explosion_G


class BasicExplosion(LoopImageEntity, ABC):

    def __init__(self, init_position):
        # Check Initialization
        if not hasattr(self, "INIT_FLAG") or not self.INIT_FLAG:
            raise Exception("!!!ERROR: class is not init! {}".format(self))
        LoopImageEntity.__init__(self)
        self.add(Explosion_G)

        self.rect.center = init_position

    def update(self) -> None:
        if self._switch_image():
            self.kill()
            del self

    @classmethod
    def init(cls):
        if not hasattr(cls, "INIT_FLAG") or not cls.INIT_FLAG:
            cls._init_image()
            cls.INIT_FLAG = True
