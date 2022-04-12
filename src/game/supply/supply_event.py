import pygame
import random

from src.util.type import Pos
from .SUPPLY_TYPE import SUPPLY_TYPE
from .SupplyBomb import SupplyBomb
from .SupplyLevel import SupplyLevel
from .SupplyLife import SupplyLife
from src.setting import SCREEN_WIDTH


EVENT_ADD_SUPPLY = pygame.event.custom_type()


def supply_event_config():
    pygame.time.set_timer(EVENT_ADD_SUPPLY, 15000)


def supply_events_handler(event):
    if event.type == EVENT_ADD_SUPPLY:
        add_supply(random.choice(
            [SUPPLY_TYPE.Bomb, SUPPLY_TYPE.Level, SUPPLY_TYPE.Life]))


def add_supply(supply_type: SUPPLY_TYPE):
    pos = Pos([random.randint(int(SCREEN_WIDTH/3), int(2 * SCREEN_WIDTH/3)), -50])
    if supply_type == SUPPLY_TYPE.Life:
        supply = SupplyLife(pos)
        supply.enter_action_enter_phase()
    elif supply_type == SUPPLY_TYPE.Bomb:
        supply = SupplyBomb(pos)
        supply.enter_action_enter_phase()
    elif supply_type == SUPPLY_TYPE.Level:
        supply = SupplyLevel(pos)
        supply.enter_action_enter_phase()
