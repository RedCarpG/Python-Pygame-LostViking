
import random
import pygame
from .SUPPLY_TYPE import SUPPLY_TYPE
from .SupplyLife import SupplyLife
from .SupplyBomb import SupplyBomb
from .SupplyLevel import SupplyLevel
from .Supply import Supply


def get_supply_type(supply_type: SUPPLY_TYPE = None) -> Supply:
    if supply_type is None:
        supply_type = random.choice(SUPPLY_TYPE.get_types())
    if supply_type == SUPPLY_TYPE.Bomb:
        return SupplyBomb
    elif supply_type == SUPPLY_TYPE.Level:
        return SupplyLevel
    elif supply_type == SUPPLY_TYPE.Life:
        return SupplyLife
