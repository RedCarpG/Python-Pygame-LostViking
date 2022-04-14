import pygame
import random
from src.util.type import Pos
from .SUPPLY_TYPE import SUPPLY_TYPE
from .SupplyBomb import SupplyBomb
from .SupplyLevel import SupplyLevel
from .SupplyLife import SupplyLife
from src.setting import SCREEN_WIDTH
from .Supply import Supply


EVENT_ADD_SUPPLY = pygame.event.custom_type()


def supply_event_config():
    pygame.time.set_timer(EVENT_ADD_SUPPLY, 25000)


def supply_events_handler(event):
    if event.type == EVENT_ADD_SUPPLY:
        pos = Pos(
            [random.randint(int(SCREEN_WIDTH/3), int(2 * SCREEN_WIDTH/3)), -50])
        sup = get_supply()
        sup(pos)


def get_supply(supply_type: SUPPLY_TYPE = None) -> Supply:
    if supply_type is None:
        supply_type = random.choice(SUPPLY_TYPE.get_types())
    if supply_type == SUPPLY_TYPE.Bomb:
        return SupplyBomb
    elif supply_type == SUPPLY_TYPE.Level:
        return SupplyLevel
    elif supply_type == SUPPLY_TYPE.Life:
        return SupplyLife
