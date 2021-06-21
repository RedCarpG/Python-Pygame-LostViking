from ..enemy.EnemyI import EnemyI
from ..generic_loader.image_loader import load_image
from .level1_group import Enemy_Scout_G

import random
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT


class EnemyScout(EnemyI):

    def __init__(self, pos):
        EnemyI.__init__(self, pos)
        self.add(Enemy_Scout_G)

    @classmethod
    def _init_image(cls):
        cls.IMAGE = dict()
        cls.IMAGE["BASE"] = [load_image("Enemy/Enemy_Phoenix1.png")]
        cls.IMAGE["IDLE"] = [load_image("Enemy/Enemy_Phoenix1.png"),
                             load_image("Enemy/Enemy_Phoenix2.png")]
        cls.IMAGE["EXPLODE"] = [load_image("Enemy/Destroy_Phoenix1.png"),
                                load_image("Enemy/Destroy_Phoenix2.png"),
                                load_image("Enemy/Destroy_Phoenix3.png"),
                                load_image("Enemy/Destroy_Phoenix4.png"),
                                load_image("Enemy/Destroy_Phoenix5.png"),
                                load_image("Enemy/Destroy_Phoenix6.png")]
        cls._IS_SET_IMAGE = True

    @classmethod
    def _init_sound(cls):
        cls._SOUND = dict()
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("Explode", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                          load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])
        cls._IS_SET_SOUND = True


# Create event
def add_enemy_scout(num):
    if len(Enemy_Scout_G.sprites()) < 25:
        for i in range(num):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(-0.5 * SCREEN_HEIGHT, 0 - 100)

            EnemyScout([x, y])
        return True
    return False
