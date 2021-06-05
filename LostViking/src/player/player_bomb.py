from LostViking.src.generic_items.graphic_helper import SingleImageHelper
from LostViking.src.constants import SCREEN
from LostViking.src.generic_loader.image_loader import load_image
import pygame

Player_NucBomb_G = pygame.sprite.GroupSingle(None)


class PlayerNucBomb(SingleImageHelper, pygame.sprite.Sprite):
    """ Player Nuclear Bomb
    -> Implements StraightBullet class :
            -> SingleImageHelper
            -> pygame.sprite.Sprite
    """
    _Is_Already_Activate = False

    _NUC_BOMB_COUNT_MAX = 3
    _Nuc_Bomb_Count = 0

    _SOUND = {}

    def __init__(self, init_position: (list, tuple)):
        pygame.sprite.Sprite.__init__(self, Player_NucBomb_G)
        self.rect = self.image.get_rect()
        self.rect.center = init_position
        self.accelerate = 0.2
        self.speed = -2
        self.explode_flag = False
        self.active = True

    def update(self) -> None:
        if self.active:
            if self.rect.bottom > SCREEN.get_h() // 3:
                self.move()
            else:
                self.explode_flag = True
        else:
            self.dec_nuc_count()
            self.kill()

    def move(self) -> None:
        self.rect.top -= self.speed
        self.speed += self.accelerate

    @classmethod
    def launch(cls, player_position) -> None:
        if cls._Is_Already_Activate:
            cls._SOUND["Error"].stop()
            cls._SOUND["Error"].play()
        else:
            cls._Is_Already_Activate = True
            cls._SOUND["NuclearLaunch_Detected"].stop()
            cls._SOUND["NuclearLaunch_Detected"].play()
            PlayerNucBomb(player_position)

    @classmethod
    def get_nuc_count(cls) -> int:
        return cls._Nuc_Bomb_Count

    @classmethod
    def add_nuc_count(cls) -> None:
        if cls._Nuc_Bomb_Count < cls._NUC_BOMB_COUNT_MAX:
            cls._Nuc_Bomb_Count += 1

    @classmethod
    def dec_nuc_count(cls):
        cls._Nuc_Bomb_Count -= 1

    @classmethod
    def init_image(cls) -> None:
        cls._IMAGE = load_image("MyPlane/bullet.png")

        cls._INIT_FLAG = True

    @classmethod
    def init_sound(cls) -> None:
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("NuclearLaunch_Detected",
                              load_sound("NuclearLaunch_Detected.wav",
                                         MAIN_VOLUME - 0.1))
        cls._SOUND.setdefault("Error", load_sound("Error.wav", MAIN_VOLUME))

