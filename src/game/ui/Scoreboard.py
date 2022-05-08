import pygame
from src.helper.font import load_font, FontEntity, get_font
from src.setting import COLOR
from src.game.groups import G_Player1


class Scoreboard:

    def __init__(self, surface) -> None:

        self.surface = surface
        self.player_g = G_Player1
        self.Text_G = {
            'score': FontEntity(self.surface, get_font("Scoreboard"),
                                ("Score: " + str(self.player_g.sprite.score)), (40, 30), color=COLOR.WHITE),
        }

    def update(self):
        self.Text_G["score"].change_text(
            f"Score: {self.player_g.sprite.score}")

    def blit(self):
        for _, text in self.Text_G.items():
            text.blit()
