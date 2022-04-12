from pygame.locals import *
import pygame
import pytest
from src.game.groups import *
from src.game.player import *

from src.helper.font import *
from src.game.ui import Scoreboard
from src.setting import *
from src.game.supply import *
from src.game.level.level1 import *
from src.util.type import Pos
from src.setting import *


class Testboard:

    def load_testboard(self):
        load_font("arialbd.ttf", 25, "Testboard")

    def __init__(self, surface, player) -> None:
        self.load_testboard()
        self.surface = surface
        self.player = player
        self.Text_G = {
            'score': FontEntity(self.surface, get_font("Testboard"),
                                f"Score: {self.player.score}", (0, 30), color=COLOR.WHITE),
            'life': FontEntity(self.surface, get_font("Testboard"),
                               f"Life: {self.player.life}", (0, 60), color=COLOR.RED),
            'level': FontEntity(self.surface, get_font("Testboard"),
                                f"Level: {self.player.level}", (0, 90), color=COLOR.WHITE),
            'bomb': FontEntity(self.surface, get_font("Testboard"),
                               f"Bomb: {self.player.bomb_count}", (0, 120), color=COLOR.WHITE),
            'health': FontEntity(self.surface, get_font("Testboard"),
                                 f"HP: {self.player.health}", (0, 150), color=COLOR.RED),
            'enemy': FontEntity(self.surface, get_font("Testboard"),
                                f"Enemy: {len(G_Enemys)}", (0, 180), color=COLOR.RED),
        }

    def update(self):
        self.Text_G["score"].change_text(f"Score: {self.player.score}")
        self.Text_G["life"].change_text(f"Life: {self.player.life}")
        self.Text_G["health"].change_text(f"health: {self.player.health}")
        self.Text_G["level"].change_text(f"Level: {self.player.level}")
        self.Text_G["bomb"].change_text(f"Bomb: {self.player.bomb_count}")
        self.Text_G["enemy"].change_text(f"Enemy: {len(G_Enemys)}")

    def blit(self):
        for _, text in self.Text_G.items():
            text.blit()


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
        self.testboard = Testboard(screen, self.player)

    def event(self):

        def test_key_event(event):
            if event.key == K_o:
                EnemyPhoenix(Pos([0, 200]), is_left=True)
            if event.key == K_p:
                EnemyScout.add_enemy_scout(1)

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

            for each in G_Enemys.sprites():
                pygame.draw.rect(self.screen, COLOR.RED, each.rect, 3)
            for each in G_Enemy_Bullets.sprites():
                pygame.draw.rect(self.screen, COLOR.RED, each.rect, 3)
            G_Enemy_Bullets.draw(self.screen)
            G_Player_Bullets.draw(self.screen)
            G_Enemys.draw(self.screen)
            G_Supplies.draw(self.screen)
            G_Bomb.draw(self.screen)
            G_Players.draw(self.screen)
            G_Effects.draw(self.screen)
            self.testboard.blit()
            # Display
            pygame.display.flip()

            self.clock.tick(60)


def test_player():
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
    test_player()

    import sys

    sys.exit()
