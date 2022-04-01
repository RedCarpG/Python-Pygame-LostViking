""" This file includes:
    -> PlayerNucBomb class which creates a bomb entity
    -> NucExplosion class which handles with the drawing of explosion image"""
from pygame.sprite import Sprite
from src.setting import SCREEN_HEIGHT
from src.helper.image import get_image
from src.helper.sound import play_sound
from src.util.type import Pos, Size
from src.game.groups import G_Bomb
from src.game.generic_items.Effect import Effect


class PlayerNucBomb(Sprite):
    _IS_LAUNCHED = False

    def __init__(self, pos: Pos):
        Sprite.__init__(self, G_Bomb)
        play_sound("NUC_LAUNCH")

        # Set Image properties
        self.image = get_image("PlayerPlane/bullet.png")
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
            play_sound("NUC_EXPLODE")
            self.kill()
            del self

    # --------------- Behaviors --------------- #
    def _move(self) -> None:
        self.rect.top -= self.speed
        self.speed += self.accelerate

    @classmethod
    def launch(cls, pos: Pos) -> None:
        if cls._IS_LAUNCHED:
            return

        cls._IS_LAUNCHED = True
        PlayerNucBomb(pos)


class NucExplosion(Effect):

    def __init__(self, pos: Pos):
        Effect.__init__(
            self,
            pos=pos,
            frames={
                "IDLE": get_image("Bomb/NucExplosion.png")
            },
            frame_size=Size([96, 128])
        )
