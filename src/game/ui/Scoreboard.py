from src.helper.font import load_font, FontEntity, get_font
from src.setting import COLOR
from src.game.groups import *


def load_scoreboard():
    load_font("arialbd.ttf", 30, "Scoreboard")


class Scoreboard:

    def __init__(self, surface, player) -> None:
        load_scoreboard()
        self.surface = surface
        self.player = player
        self.Text_G = {
            'score': FontEntity(self.surface, get_font("Scoreboard"),
                                ("Score: " + str(self.player.score)), (0, 30), color=COLOR.WHITE),
            'level': FontEntity(self.surface, get_font("Scoreboard"),
                                f"Level: {self.player.level}", (0, 60), color=COLOR.WHITE),
            'bomb': FontEntity(self.surface, get_font("Scoreboard"),
                               ("Bomb: " + str(self.player.bomb_count)), (0, 90), color=COLOR.WHITE),
            'health': FontEntity(self.surface, get_font("Scoreboard"),
                                 ("Health: " + str(self.player.health)), (0, 120), color=COLOR.RED),
            'life': FontEntity(self.surface, get_font("Scoreboard"),
                               ("Life: " + str(self.player.life)), (0, 150), color=COLOR.RED),
        }

    def update(self):
        self.Text_G["score"].change_text(f"Score: {self.player.score}")
        self.Text_G["life"].change_text(f"Life: {self.player.life}")
        self.Text_G["health"].change_text(f"Health: {self.player.health}")
        self.Text_G["level"].change_text(f"Level: {self.player.level}")
        self.Text_G["bomb"].change_text(f"Bomb: {self.player.bomb_count}")

    def blit(self):
        for _, text in self.Text_G.items():
            text.blit()
