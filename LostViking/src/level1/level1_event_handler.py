import pygame
import logging
import sys
from .level1_event_type import EVENT_CREATE_SCOUT, EVENT_CREATE_PHOENIX, EVENT_CREATE_CARRIER
from .level1_constant import *
from .Enemy_Scout import add_enemy_scout
from .Enemy_Phoenix import add_enemy_phoenix
from .Enemy_Carrier import add_enemy_carrier

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def level_event_config():
    pygame.time.set_timer(EVENT_CREATE_SCOUT, SPAWN_SPEED_SCOUT)
    pygame.time.set_timer(EVENT_CREATE_PHOENIX, SPAWN_SPEED_PHOENIX)
    pygame.time.set_timer(EVENT_CREATE_CARRIER, SPAWN_SPEED_CARRIER)
    # pygame.time.set_timer(Game.CREATE_SUPPLY, 40000)


def level_events_handler(event):
    if event.type == EVENT_CREATE_SCOUT:
        if add_enemy_scout(1):
            logging.info('Create Scout')
        return True
    elif event.type == EVENT_CREATE_PHOENIX:
        add_enemy_phoenix()
        logging.info('Create Phoenix')
        return True
    elif event.type == EVENT_CREATE_CARRIER:
        add_enemy_carrier()
        logging.info('Create Carrier')
        pygame.time.set_timer(EVENT_CREATE_CARRIER, 0)
        pygame.time.set_timer(EVENT_CREATE_PHOENIX, 0)
        pygame.time.set_timer(EVENT_CREATE_SCOUT, 0)
        return True
    return False
