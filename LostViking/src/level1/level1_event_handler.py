import pygame
from .level1_event_type import *
import random
from ..constants import SCREEN
from .Scout import EnemyScout
from .Phoenix import EnemyPhoenix
from .level1_group import Enemy_Scout_G


# 生成敌机
def add_enemy_scout(num):
    for i in range(num):
        x = random.randint(50, SCREEN.get_w() - 50)
        y = random.randint(-0.5 * SCREEN.get_h(), 0 - 100)

        EnemyScout([x, y])


def add_enemy_phoenix():
    x1 = SCREEN.get_w() + 200
    x2 = - 200
    y = 200
    EnemyPhoenix((x1, y), 'L')
    EnemyPhoenix((x2, y), 'R')


def level1_events(event):
    if event.type == EVENT_CREATE_SCOUT:
        if len(Enemy_Scout_G.sprites()) < 25:
            add_enemy_scout(1)
            print("CREATE_Scout:")
        return True
    elif event.type == EVENT_CREATE_PHOENIX:
        add_enemy_phoenix()
        print("CREATE_Phoenix:")
        return True
    elif event.type == EVENT_CREATE_CARRIER:
        """
        pygame.time.set_timer(self.CREATE_Scout, 0)
        pygame.time.set_timer(self.CREATE_Phoenix, 0)
        pygame.time.set_timer(self.CREATE_Carrier, 0)
        pygame.time.set_timer(Game.CREATE_SUPPLY, 40000)
        add_enemy_Carrier()
        print("CREATE_Carrier:")
        """
        return True
    return False
