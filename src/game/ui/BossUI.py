import pygame
from src.helper.font import load_font, FontEntity, get_font
from src.setting import COLOR, SCREEN_WIDTH
from src.game.groups import G_BOSS


class BossUI:

    def __init__(self, surface) -> None:
        load_font("arialbd.ttf", 20, "Boss")

        self.surface = surface
        self.boss_g = G_BOSS
        self.health_percentage = 1
        health_text = FontEntity(self.surface, get_font("Boss"),
                                 "/", (0, 0), color=COLOR.WHITE)
        health_text.move_center([SCREEN_WIDTH/2, 45])
        self.Text_G = {
            'health': health_text
        }

    def update(self):
        if self.boss_g.sprite is not None:
            self.health_percentage = self.boss_g.sprite.health / self.boss_g.sprite.MAX_HEALTH
            self.Text_G["health"].change_text(
                f"{self.boss_g.sprite.health}/{self.boss_g.sprite.MAX_HEALTH}")

    def blit(self):
        if self.boss_g.sprite is not None:
            sprite = self.boss_g.sprite
            pygame.draw.rect(self.surface, COLOR.GREEN, pygame.Rect(
                SCREEN_WIDTH/8, 30, SCREEN_WIDTH/4 * 3, 30))
            pygame.draw.rect(self.surface, COLOR.RED, pygame.Rect(
                SCREEN_WIDTH/8, 30, SCREEN_WIDTH/4 * 3 * self.health_percentage, 30))
            for _, text in self.Text_G.items():
                text.blit()
