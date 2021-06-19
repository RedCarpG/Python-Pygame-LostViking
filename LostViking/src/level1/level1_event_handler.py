import pygame
from .level1_event_type import EVENT_CREATE_SCOUT, EVENT_CREATE_PHOENIX, EVENT_CREATE_CARRIER
from .level1_constant import *
import random
from ..constants import SCREEN
from .Enemy_Scout import EnemyScout
from .Enemy_Phoenix import EnemyPhoenix
from .Enemy_Carrier import EnemyCarrier
from .level1_group import Enemy_Scout_G
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# Create Enemy
def add_enemy_scout(num):
    for i in range(num):
        x = random.randint(50, SCREEN.get_w() - 50)
        y = random.randint(-0.5 * SCREEN.get_h(), 0 - 100)

        EnemyScout([x, y])


def add_enemy_phoenix():
    x1 = SCREEN.get_w()
    x2 = 0
    y = 200
    EnemyPhoenix((x1, y), 'R')
    EnemyPhoenix((x2, y), 'L')


def add_enemy_carrier():
    EnemyCarrier()


def level1_event_config():
    pygame.time.set_timer(EVENT_CREATE_SCOUT, SPAWN_SPEED_SCOUT)
    pygame.time.set_timer(EVENT_CREATE_PHOENIX, SPAWN_SPEED_PHOENIX)
    pygame.time.set_timer(EVENT_CREATE_CARRIER, SPAWN_SPEED_CARRIER)
    # pygame.time.set_timer(Game.CREATE_SUPPLY, 40000)


def level1_events_handler(event):
    if event.type == EVENT_CREATE_SCOUT:
        if len(Enemy_Scout_G.sprites()) < 25:
            add_enemy_scout(1)
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
