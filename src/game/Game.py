from pygame.locals import *
import pygame
import pytest


from src.helper.font import *
from src.helper.sound import *
from src.setting import *

from src.game.groups import *
from src.game.player import *
from src.game.ui import *
from src.game.supply import *
from src.game.level import *
from src.util.type import Pos


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        self.running = True

        load_music("music/bgm1.ogg", MAIN_VOLUME - 0.4)
        play_music()
        # Player
        load_asset_player()
        self.player = PlayerViking(pos=None)
        G_Player1.add(self.player)
        G_Players.add(self.player)
        # Supply
        load_asset_supply()
        # UI
        load_asset_ui()
        self.ui = UI(self.screen, self.player)
        self.scoreboard = Scoreboard(self.screen, self.player)
        self.fps_counter = FPSCounter(
            self.screen, self.clock, [SCREEN_WIDTH-100, 100])
        self.boss_ui = BossUI(self.screen)
        # Level
        self.level = Level1()

    def event(self):

        for event in pygame.event.get():
            if detect_player_event(event, player1=self.player):
                pass
            elif event.type == QUIT:
                self.running = False
            # --------------- Key Down Events ---------------
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif self.level.event_handler(event):
                continue
            else:
                supply_events_handler(event)

        detect_key_pressed(self.player)

    def run(self):
        while self.running:
            self.event()

            self.screen.fill(COLOR.BLACK)
            G_Enemy_Bullets.update()
            G_Player_Bullets.update()
            G_Players.update()
            G_Supplies.update()
            G_Enemys.update()
            G_Bomb.update()
            G_Effects.update()
            self.scoreboard.update()
            self.fps_counter.update()
            self.boss_ui.update()
            self.ui.update()

            self.boss_ui.blit()
            self.scoreboard.blit()
            self.fps_counter.blit()
            G_Bomb.draw(self.screen)
            G_Enemy_Bullets.draw(self.screen)
            G_Player_Bullets.draw(self.screen)
            G_Enemys.draw(self.screen)
            G_Players.draw(self.screen)
            G_Supplies.draw(self.screen)
            G_Effects.draw(self.screen)
            self.ui.blit()
            # Display
            pygame.display.flip()

            self.clock.tick(60)
