from ..enemy.enemyPlane import EnemyI
from ..generic_loader.image_loader import load_image
from .level1_group import Enemy_Scout_G

import random
from ..constants import SCREEN


class EnemyScout(EnemyI):

    def __init__(self, pos):
        EnemyI.__init__(self, pos)
        self.add(Enemy_Scout_G)

    @classmethod
    def _init_image(cls):
        cls._IMAGE["Base"] = [load_image("Enemy/Enemy_Phoenix1.png")]
        cls._IMAGE.setdefault("Normal", [load_image("Enemy/Enemy_Phoenix1.png"),
                                         load_image("Enemy/Enemy_Phoenix2.png")])
        cls._IMAGE.setdefault("Explode", [load_image("Enemy/Destroy_Phoenix1.png"),
                                          load_image("Enemy/Destroy_Phoenix2.png"),
                                          load_image("Enemy/Destroy_Phoenix3.png"),
                                          load_image("Enemy/Destroy_Phoenix4.png"),
                                          load_image("Enemy/Destroy_Phoenix5.png"),
                                          load_image("Enemy/Destroy_Phoenix6.png")])
        cls._INIT_FLAG_IMAGE = True

    @classmethod
    def _init_sound(cls):
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("Explode", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                          load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])
        cls._INIT_FLAG_SOUND = True

    @classmethod
    def _init_speed(cls):
        cls._MAX_SPEED_DOWN = 5
        cls._INIT_FLAG_SPEED = True

    @classmethod
    def init(cls):
        cls._MAX_HEALTH = 100
        cls._SCORE = 100
        cls._init_image()
        cls._init_speed()
        cls._INIT_FLAG = True


# 生成敌机
def add_enemy_scout(num):
    for i in range(num):
        x = random.randint(50, SCREEN.get_w() - 50)
        y = random.randint(-0.5 * SCREEN.get_h(), 0 - 100)

        EnemyScout([x, y])
