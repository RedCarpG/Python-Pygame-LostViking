
import random

from pygame.math import Vector2
from pygame.sprite import Group
from src.setting import SCREEN_HEIGHT, SCREEN_WIDTH
from src.game.generic_items.Enemy import EnemyI
from src.game.generic_items.Bullet import EnemyBullet
from src.helper.image import get_image
from src.util.type import Pos


class EnemyScout(EnemyI):

    MAX_HEALTH = 500
    SCORE = 500

    GROUP = Group()

    def __init__(self, pos: Pos):
        super().__init__(
            pos=pos,
            frames={
                "BASE": get_image("Enemy/Scout/ScoutBase.png"),
                "IDLE": get_image("Enemy/Scout/ScoutNormal.png"),
                "DESTROY": get_image("Enemy/Scout/ScoutDestroy.png"),
                "HIT": get_image("Enemy/Scout/ScoutHit.png"),
                "ATTACK": get_image("Enemy/Scout/ScoutAttack.png")
            },
            frame_size=None)
        self._speed.y = 2

    # --------------- Create function --------------- #

    @classmethod
    def add_enemy_scout(cls, num) -> bool:
        if len(cls.GROUP.sprites()) < 25:
            for i in range(num):
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = - 100

                EnemyScout(Pos([x, y]))
            return True
        return False

    def shoot(self, target):
        BulletScout(Pos(self.rect.center))


class BulletScout(EnemyBullet):

    DAMAGE = 100
    SPEED = 5

    def __init__(self, pos: Pos):
        super().__init__(
            pos,
            speed=Vector2([0, self.SPEED]),
            damage=self.DAMAGE,
            image=get_image("Enemy/bullet.png")
        )
