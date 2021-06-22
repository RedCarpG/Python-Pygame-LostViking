from ..enemy.EnemyIII import EnemyIII
from .level1_group import Enemy_Phoenix_G
from ..groups import Enemy_Bullet_G
from ..generic_items.BasicBullet import BasicSpinBullet
from ..generic_items.BasicShield import BasicShield
from ..constants import SCREEN_WIDTH


class EnemyPhoenix(EnemyIII):

    def __init__(self, pos, side):
        EnemyIII.__init__(self, position=pos, side=side)
        self.add(Enemy_Phoenix_G)

        self.shield = ShieldPhoenix(self)

    def __del__(self):
        self.shield.kill()
        del self.shield

    # Rewrite hit to add Shield
    def hit(self, damage=100, **kwargs):
        if self.shield.is_active:
            self.shield.hit(damage)
        else:
            super().hit(damage)

    def _action_attack(self, *args, **kwargs):
        BulletPhoenix(self.rect.center, self.angle)
        self.enter_attack_idle_phase()

    @classmethod
    def _init_image(cls):
        cls.IMAGE = dict()
        from ..generic_loader.image_loader import load_image
        cls.IMAGE["BASE"] = [load_image("Enemy/Enemy_Phoenix1.png")]
        cls.IMAGE["IDLE"] = [load_image("Enemy/Enemy_Phoenix1.png"),
                             load_image("Enemy/Enemy_Phoenix2.png")]
        cls.IMAGE["EXPLODE"] = [load_image("Enemy/Destroy_Phoenix1.png"),
                                load_image("Enemy/Destroy_Phoenix2.png"),
                                load_image("Enemy/Destroy_Phoenix3.png"),
                                load_image("Enemy/Destroy_Phoenix4.png"),
                                load_image("Enemy/Destroy_Phoenix5.png"),
                                load_image("Enemy/Destroy_Phoenix6.png")]
        cls.IMAGE["STOP"] = [load_image("Enemy/Enemy_Phoenix_Stop1.png"),
                             load_image("Enemy/Enemy_Phoenix_Stop2.png")]
        cls.IMAGE["ATTACK"] = [load_image("Enemy/Enemy_Phoenix_AttackLight1.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight2.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight3.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight4.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight5.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight6.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight7.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight8.png"),
                               load_image("Enemy/Enemy_Phoenix_AttackLight9.png")]
        cls._IS_SET_IMAGE = True

    # TODO Sound
    @classmethod
    def _init_sound(cls):
        cls._SOUND = dict()
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("Shield", load_sound("Shield.wav", MAIN_VOLUME - 0.3))
        cls._SOUND.setdefault("Laser", load_sound("Laser.wav", MAIN_VOLUME - 0.2))
        cls._SOUND.setdefault("Explode", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                          load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])
        cls._INIT_FLAG_SOUND = True

    @classmethod
    def _init_attributes(cls):
        super()._init_attributes()
        cls.MAX_HEALTH = 100


class BulletPhoenix(BasicSpinBullet):

    def __init__(self, position, angle):
        BasicSpinBullet.__init__(self, position, angle)
        self.add(Enemy_Bullet_G)

    @classmethod
    def _init_image(cls):
        from ..generic_loader.image_loader import load_image
        cls.IMAGE = load_image("Enemy/laser.png")
        cls._IS_SET_IMAGE = True

    @classmethod
    def _init_attrs(cls):
        cls.MAX_SPEED_X = cls.MAX_SPEED_Y = 15
        cls._IS_SET_ATTRS = True


class ShieldPhoenix(BasicShield):

    def __init__(self, owner):
        BasicShield.__init__(self, owner)

    @classmethod
    def _init_image(cls):
        cls.IMAGE = dict()
        from ..generic_loader.image_loader import load_image
        cls.IMAGE["BASE"] = [load_image("Enemy/Shield1.png")]
        cls.IMAGE["IDLE"] = [load_image("Enemy/Shield1.png"),
                             load_image("Enemy/Shield2.png"),
                             load_image("Enemy/Shield3.png"),
                             load_image("Enemy/Shield4.png"),
                             load_image("Enemy/Shield5.png")]
        cls._IS_SET_IMAGE = True

    @classmethod
    def _init_attrs(cls):
        cls.MAX_HEALTH = 1000
        cls._IS_SET_ATTRS = True


def add_enemy_phoenix():
    x1 = SCREEN_WIDTH
    x2 = 0
    y = 200
    EnemyPhoenix((x1, y), 'R')
    EnemyPhoenix((x2, y), 'L')
