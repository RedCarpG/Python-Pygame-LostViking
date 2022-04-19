from pygame.locals import *
import pygame
import pytest
from src.game.ui.BossUI import BossUI
from src.game.groups import *
from src.game.player import *

from src.helper.font import *
from src.game.ui import Scoreboard
from src.setting import *
from src.game.supply import *
from src.game.level.level1 import *
from src.util.type import Pos
from src.setting import *
from src.game.level.level1 import Level1


class Testboard:

    def load_testboard(self):
        load_font("arialbd.ttf", 20, "Testboard")

    def __init__(self, surface, player) -> None:
        self.load_testboard()
        self.surface = surface
        self.player = player
        self.Text_G = {
            'enemy': FontEntity(self.surface, get_font("Testboard"),
                                f"Enemy: {len(G_Enemys)}", (SCREEN_WIDTH / 4*3, 180), color=COLOR.RED),
        }

    def update(self):
        self.Text_G["enemy"].change_text(f"Enemy: {len(G_Enemys)}")

    def blit(self):
        for _, text in self.Text_G.items():
            text.blit()


def draw_path(sprite, screen):
    if hasattr(sprite, "path"):
        pygame.draw.circle(screen, COLOR.RED, sprite.path[0], 10)
        pygame.draw.line(screen, COLOR.GREEN,
                         sprite.rect.center, sprite.path[0])


def draw_speed(sprite, screen):
    if hasattr(sprite, "speed"):
        start_point = sprite.rect.center,
        end_point = [sprite.rect.center[0] + sprite.speed.x *
                     10, sprite.rect.center[1] + sprite.speed.y * 10]
        pygame.draw.line(screen, COLOR.WHITE, start_point, end_point, 5)


class TestGame:
    def __init__(self, screen) -> None:
        load_asset_player()
        load_asset_supply()
        self.screen = screen
        self.player = PlayerViking(pos=None)

        G_Player1.add(self.player)
        G_Players.add(self.player)

        self.clock = pygame.time.Clock()

        self.running = True
        self.scoreboard = Scoreboard(screen, self.player)
        self.testboard = Testboard(screen, self.player)
        self.bossUI = BossUI(self.screen)
        Level1(enable_event=False)

    def event(self):

        def test_key_event(event):
            if event.key == K_o:
                EnemyPhoenix(Pos([0, 200]), is_left=True)
            elif event.key == K_p:
                EnemyScout.add_enemy_scout(1)
            elif event.key == K_i:
                EnemyCarrier.add_enemy_carrier()
            elif event.key == K_u:
                EnemyInterceptor(Pos([200, 200]), [[100, 100], [200, 300]])

        for event in pygame.event.get():
            if detect_player_event(event, player1=self.player):
                pass
            elif event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                else:
                    test_key_event(event)

        detect_key_pressed(self.player)

    def run(self):

        while self.running:
            self.event()

            self.screen.fill(COLOR.BLACK)
            G_Player_Bullets.update()
            G_Enemy_Bullets.update()
            G_Enemys.update()
            G_Players.update()
            G_Bomb.update()
            G_Effects.update()
            G_Supplies.update()
            self.testboard.update()
            self.scoreboard.update()
            self.bossUI.update()

            self.testboard.blit()
            self.scoreboard.blit()
            self.bossUI.blit()
            for each in G_Enemys.sprites():
                pygame.draw.rect(self.screen, COLOR.RED, each.rect, 3)
                draw_path(each, self.screen)
                draw_speed(each, self.screen)
            for each in G_Enemy_Bullets.sprites():
                pygame.draw.rect(self.screen, COLOR.RED, each.rect, 3)
            G_Enemy_Bullets.draw(self.screen)
            G_Player_Bullets.draw(self.screen)
            G_Enemys.draw(self.screen)
            G_Supplies.draw(self.screen)
            G_Bomb.draw(self.screen)
            G_Players.draw(self.screen)
            G_Effects.draw(self.screen)
            # Display
            pygame.display.flip()

            self.clock.tick(60)


def test_enemy():
    # Init Environment
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption("Player Test")

    screen = pygame.display.set_mode(SCREEN_SIZE)

    game = TestGame(screen=screen)
    game.run()

    pygame.font.quit()
    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    test_enemy()

    import sys

    sys.exit()
