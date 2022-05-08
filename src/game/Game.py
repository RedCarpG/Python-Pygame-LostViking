from pygame.locals import *
import pygame
from .custom_events import EVENT_RESTART, EVENT_RESUME, EVENT_START

from src.helper.image import *
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
        pygame.mouse.set_visible(False)

        # Player
        load_asset_player()
        self.player = PlayerViking(pos=None)
        G_Player1.add(self.player)
        G_Players.add(self.player)

        # Supply
        load_asset_supply()

        # UI
        load_asset_ui()
        self.ui = UI(self.screen)
        self.ui_pause = UIPause(self.screen)
        self.scoreboard = Scoreboard(self.screen)
        self.fps_counter = FPSCounter(
            self.screen, self.clock, [SCREEN_WIDTH-100, 30])

        self.level = None

    def event(self):

        self.player.detect_key_pressed()
        for event in pygame.event.get():

            # if self.pause

            if self.player.handle_event(event):
                pass
            elif detect_custom_event(event):
                self.ui.handle_event(event)

            elif event.type == QUIT:
                self.running = False
            # --------------- Key Down Events ---------------
            elif event.type == KEYUP:
                if event.key == K_TAB:
                    self.ui.toggle_hidden()
                elif event.key == K_ESCAPE:
                    self.paused()
            else:
                supply_events_handler(event)

    def run(self):

        self.intro()

        # Level
        self.level = Level1()
        self.level.start()

        while self.running:
            self.event()

            G_Enemy_Bullets.update()
            G_Player_Bullets.update()
            G_Players.update()
            G_Supplies.update()
            G_Enemys.update()
            G_Bomb.update()
            G_Effects.update()
            self.scoreboard.update()
            self.fps_counter.update()
            self.ui.update()
            self.level.update()

            self.screen.fill(COLOR.BLACK)
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

    def paused(self):
        self.pause = True
        while self.pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif self.ui_pause.handle_event(event):
                    pass
                elif event.type == EVENT_RESUME:
                    self.pause = False
                elif event.type == EVENT_RESTART:
                    self.restart()
                    self.pause = False
                    break

            self.ui_pause.blit()
            pygame.display.update()

    def intro(self):

        intro = True

        load_music("music/bgm.ogg", MAIN_VOLUME - 0.4)
        play_music()

        ui_intro = UIIntro(self.screen)
        while intro:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif ui_intro.handle_event(event):
                    pass
                elif event.type == EVENT_START:
                    intro = False

            G_Players.update()

            ui_intro.blit()

            self.screen.fill(COLOR.BLACK, self.player.rect)
            G_Players.draw(self.screen)
            pygame.display.update(self.player.rect)

            self.clock.tick(60)

    def restart(self):

        G_BOSS.empty()
        G_Enemy_Bullets.empty()
        G_Bomb.empty()
        G_Effects.empty()
        G_Enemys.empty()
        G_Player_Bullets.empty()
        G_Supplies.empty()
        G_Player1.empty()
        G_Players.empty()
        self.player = PlayerViking(pos=None)
        G_Player1.add(self.player)
        G_Players.add(self.player)

        self.level.start()
