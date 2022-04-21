""" This file includes:
    -> PlayerNucBomb class which creates a bomb entity
    -> NucExplosion class which handles with the drawing of explosion image"""
from pygame.sprite import Sprite
import pygame

from src.game.player.PlayerPlane import PlayerPlane
from src.setting import SCREEN_HEIGHT
from src.helper.image import get_image
from src.helper.sound import play_sound
from src.util.type import Pos, Size
from src.game.groups import G_Bomb
from src.game.animation.Effect import Effect
from .PLAYER_EVENT_TYPE import EVENT_BOMB_EXPLODE


class PlayerNucBomb(Sprite):
    _IS_LAUNCHED = False

    def __init__(self, pos: Pos, player: PlayerPlane):
        super().__init__(G_Bomb)
        play_sound("BOMB_LAUNCH")
        self.player = player
        # Set Image properties
        self.image = get_image("PlayerPlane/Bomb.png")
        # Set Rect & Position
        self.rect = self.image.get_rect(center=pos)

        # Set Attributes
        self.accelerate = 0.5
        self.speed = -2

    def update(self) -> None:
        if self.rect.bottom > SCREEN_HEIGHT // 3:
            self._move()
        else:
            NucExplosion(Pos(self.rect.center))
            PlayerNucBomb._IS_LAUNCHED = False
            play_sound("BOMB_EXPLODE")
            trigger_bomb_explode_event(self)
            self.kill()

    # --------------- Behaviors --------------- #

    def _move(self) -> None:
        self.rect.top -= self.speed
        self.speed += self.accelerate

    @classmethod
    def launch(cls, pos: Pos, player) -> None:
        if cls._IS_LAUNCHED:
            return

        cls._IS_LAUNCHED = True
        PlayerNucBomb(pos, player)


class NucExplosion(Effect):

    def __init__(self, pos: Pos):
        super().__init__(
            pos=pos,
            frames={
                "IDLE": get_image("Bomb/NucExplosion.png")
            },
            frame_size=Size([400, 400])
        )


def trigger_bomb_explode_event(bomb):
    pygame.event.post(pygame.event.Event(
        EVENT_BOMB_EXPLODE, {"bomb": bomb, "player": bomb.player}))
