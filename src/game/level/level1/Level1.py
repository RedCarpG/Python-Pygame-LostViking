import pygame
import logging
import sys
from src.setting import MAIN_VOLUME
from src.helper.sound.sound_loader import load_sound
from src.helper.image import load_image, del_image
from .Scout import EnemyScout
from .Phoenix import EnemyPhoenix

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Level1:
    EVENT_CREATE_SCOUT = pygame.event.custom_type()
    EVENT_CREATE_PHOENIX = pygame.event.custom_type()
    EVENT_CREATE_CARRIER = pygame.event.custom_type()

    SPAWN_SPEED_SCOUT = 1000
    SPAWN_SPEED_PHOENIX = 25000
    SPAWN_SPEED_CARRIER = 100000

    def __init__(self) -> None:
        load_image("Enemy/Scout/ScoutBase.png")
        load_image("Enemy/Scout/ScoutNormal.png")
        load_image("Enemy/Scout/ScoutDestroy.png")
        load_image("Enemy/Scout/ScoutHit.png")
        load_image("Enemy/Scout/ScoutAttack.png")
        load_image("Enemy/Phoenix/PhoenixBase.png")
        load_image("Enemy/Phoenix/PhoenixNormal.png")
        load_image("Enemy/Phoenix/PhoenixFast.png")
        load_image("Enemy/Phoenix/PhoenixDestroy.png")
        load_image("Enemy/Phoenix/PhoenixHit.png")
        load_image("Enemy/Phoenix/PhoenixAttack.png")
        load_image("Enemy/Phoenix/PhoenixShield.png")
        load_sound("Laser.wav", MAIN_VOLUME - 0.2, "LASER")
        load_sound("Shield.wav", MAIN_VOLUME - 0.4, "SHIELD")
        load_sound("Explo.wav", MAIN_VOLUME - 0.4, "EXPLODE")
        pygame.time.set_timer(self.EVENT_CREATE_SCOUT, self.SPAWN_SPEED_SCOUT)
        pygame.time.set_timer(self.EVENT_CREATE_PHOENIX,
                              self.SPAWN_SPEED_PHOENIX)
        # pygame.time.set_timer(self.EVENT_CREATE_CARRIER, self.SPAWN_SPEED_CARRIER)

    def event_handler(self, event):
        if event.type == self.EVENT_CREATE_SCOUT:
            if EnemyScout.add_enemy_scout(1):
                logging.info('Create Scout')
            return True
        elif event.type == self.EVENT_CREATE_PHOENIX:
            if EnemyPhoenix.add_enemy_phoenix():
                logging.info('Create Phoenix')
            return True
        elif event.type == self.EVENT_CREATE_CARRIER:
            # add_enemy_carrier()
            logging.info('Create Carrier')
            pygame.time.set_timer(self.EVENT_CREATE_CARRIER, 0)
            pygame.time.set_timer(self.EVENT_CREATE_PHOENIX, 0)
            pygame.time.set_timer(self.EVENT_CREATE_SCOUT, 0)
            return True
        return False

    def __del__(self) -> None:
        pygame.time.set_timer(self.EVENT_CREATE_CARRIER, 0)
        pygame.time.set_timer(self.EVENT_CREATE_PHOENIX, 0)
        pygame.time.set_timer(self.EVENT_CREATE_SCOUT, 0)
        del_image("Enemy/ScoutBase.png")
        del_image("Enemy/ScoutNormal.png")
        del_image("Enemy/ScoutDestroy.png")
        del_image("Enemy/ScoutHit.png")
