from pygame.locals import *
import pygame
import pytest


from src.helper.font import *
from src.setting import *

from src.game.groups import *
from src.game.player import *
from src.game.ui import Scoreboard


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        self.running = True

        self.player = None
        self.load_player()

        self.scoreboard = Scoreboard(self.screen, self.player)

    def load_player(self):
        load_asset_player()
        self.player = PlayerViking(pos=None)
        G_Player1.add(self.player)

    def event(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            # --------------- Key Down Events ---------------
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            detect_player_event(event, player1=self.player)

        detect_key_pressed(self.player)

    def run(self):

        while self.running:
            self.event()

            self.screen.fill(COLOR.BLACK)
            G_Player_Bullet.update()
            G_Player1.update()
            G_Bomb.update()
            G_Effect.update()
            self.scoreboard.update()

            G_Bomb.draw(self.screen)
            G_Player_Bullet.draw(self.screen)
            G_Player1.draw(self.screen)
            G_Effect.draw(self.screen)
            self.scoreboard.blit()
            # Display
            pygame.display.flip()

            self.clock.tick(60)
