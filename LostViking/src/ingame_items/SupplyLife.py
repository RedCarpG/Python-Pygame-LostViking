from ..generic_items.BasicSupply import BasicSupply, SupplyType
from ..generic_loader.image_loader import load_image


class SupplyLife(BasicSupply):
    def __init__(self, position=None):
        BasicSupply.__init__(self, position)
        self.type = SupplyType.Life

    def get_by_player(self, player):
        pass
        # if G.LIFE < 5:
        #     G.LIFE += 1
        # self.kill()

    @classmethod
    def _init_image(cls):
        cls.IMAGE = dict()
        cls.IMAGE["BASE"] = [load_image("Supply/bullet.png")]
        cls.IMAGE["IDLE"] = [load_image("Supply/bullet.png")]
        cls._IS_SET_IMAGE = True
