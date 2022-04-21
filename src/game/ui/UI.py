import pygame
from src.game.animation.Effect import AttachEffect
from src.game.animation.AnimeSprite import AnimeSprite
from src.helper.font import FontEntity, get_font
from src.helper.image.image_loader import get_image
from src.setting import COLOR, SCREEN_HEIGHT
from src.util.type import Size


class UI:

    def __init__(self, surface, player) -> None:
        self.surface = surface
        self.player = player

        self.ui_bottomleft = get_image("UI/BottomLeft.png")
        self.ui_bottomleft_rect = self.ui_bottomleft.get_rect(
            bottom=SCREEN_HEIGHT)
        self.health_bar = get_image("UI/Healthbar.png")
        self.health_bar_rect = self.health_bar.get_rect().move(12, 58)
        self.health_rect = pygame.Rect(15, 61, 215, 20)
        self.health_text = FontEntity(self.ui_bottomleft, get_font("HealthBar"),
                                      (f"{self.player.health}/100"), (100, 63), color=COLOR.WHITE)
        self.heart_img = AnimeSprite(
            frames={
                "IDLE": get_image("UI/Heart.png")
            },
            frame_size=Size([23, 21]))
        self.heart_img.rect = pygame.Rect(
            (94, self.ui_bottomleft_rect.top+9), self.heart_img.frame_size.to_list())
        self.heart_blink = AttachEffect(
            ref=self.heart_img,
            frames={
                "IDLE": get_image("UI/HeartBlink.png")
            },
            frame_size=Size([23, 21]),
            enable_rotate=False,
            loop=True)
        self.player_img = get_image("UI/Viking.png")
        self.player_img_rect = self.player_img.get_rect()
        self.player_img_rect.center = (36, self.ui_bottomleft_rect.top + 30)

    def update(self):
        self.heart_img.update()
        self.heart_blink.update()
        self.health_rect.width = self.player.health/100*215
        self.health_text.change_text(f"{self.player.health}/100")

    def blit(self):
        for i in range(self.player.life):
            rect = pygame.Rect(
                (94 + i*30, self.ui_bottomleft_rect.top+9), self.heart_img.frame_size.to_list())
            self.surface.blit(
                self.heart_img.image, rect)
            if self.player.life == 1:
                self.surface.blit(
                    self.heart_blink.image, rect)
        pygame.draw.rect(self.ui_bottomleft, COLOR.BROWN,
                         pygame.Rect(15, 61, 215, 20))
        pygame.draw.rect(self.ui_bottomleft, COLOR.RED, self.health_rect)
        self.health_text.blit()
        self.ui_bottomleft.blit(self.health_bar, self.health_bar_rect)
        self.surface.blit(self.ui_bottomleft, self.ui_bottomleft_rect)
        self.surface.blit(self.player_img, self.player_img_rect)
