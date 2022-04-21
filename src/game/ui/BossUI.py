import pygame
from src.helper.font import FontEntity, get_font
from src.setting import COLOR, SCREEN_WIDTH
from src.game.groups import G_BOSS
from src.helper.image.image_loader import get_image
from src.setting import COLOR, SCREEN_HEIGHT


class BossUI:

    def __init__(self, surface) -> None:

        self.surface = surface
        self.boss_g = G_BOSS

        health_text = FontEntity(self.surface, get_font("HealthBar"),
                                 "/", (0, 0), color=COLOR.WHITE)
        health_text.move_center([SCREEN_WIDTH/2, 45])

        self.ui_midtop = get_image("UI/MidTop.png")
        self.ui_midtop_rect = self.ui_midtop.get_rect(
            midtop=(SCREEN_WIDTH/2, 0))
        self.health_bar = get_image("UI/MidTop_Healthbar.png")
        self.health_bar_rect = self.health_bar.get_rect().move(31, 12)
        self.health_rect = pygame.Rect(35, 15, 470, 20)
        self.health_text = FontEntity(self.ui_midtop, get_font("HealthBar"),
                                      "/", (273, 18), color=COLOR.BLACK)

    def update(self):
        if self.boss_g.sprite is not None:
            sprite = self.boss_g.sprite
            self.health_text.change_text(
                f"{sprite.health}/{sprite.MAX_HEALTH}")
            self.health_rect.width = sprite.health/sprite.MAX_HEALTH*470

    def blit(self):
        if self.boss_g.sprite is not None:
            pygame.draw.rect(self.ui_midtop, COLOR.BROWN,
                             pygame.Rect(35, 15, 470, 20))
            pygame.draw.rect(self.ui_midtop, COLOR.RED, self.health_rect)
            self.health_text.blit()
            self.ui_midtop.blit(self.health_bar, self.health_bar_rect)
            self.surface.blit(self.ui_midtop, self.ui_midtop_rect)
