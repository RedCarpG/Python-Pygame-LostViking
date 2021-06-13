from ..enemy.enemyPlane import EnemyIII
from .level1_group import Enemy_Phoenix_G


class EnemyPhoenix(EnemyIII):

    def __init__(self, pos, side):
        EnemyIII.__init__(self, pos, side)
        self.add(Enemy_Phoenix_G)

        self.stay = 1000
        # self.attack_interval = MYTIME(100)
        # self.shield = Shield()

    """
    # 增加 Shield
    def hit(self, damage=100):
        if self.shield.active:
            self.shield.hit(damage)
        else:
            self.health -= damage
            if self.health <= 0:
                self.active = False
    """

    def _shoot(self):
        pass
        # Bullet.BULLETS.add(Bullet_Phoenix(self.rect.center, self.angle))

    @classmethod
    def _init_image(cls):
        if not cls._INIT_FLAG_IMAGE:
            from ..generic_loader.image_loader import load_image
            cls._IMAGE["Base"] = [load_image("Enemy/Enemy_Phoenix1.png")]
            cls._IMAGE.setdefault("Normal", [load_image("Enemy/Enemy_Phoenix1.png"),
                                             load_image("Enemy/Enemy_Phoenix2.png")])
            cls._IMAGE.setdefault("Explode", [load_image("Enemy/Destroy_Phoenix1.png"),
                                              load_image("Enemy/Destroy_Phoenix2.png"),
                                              load_image("Enemy/Destroy_Phoenix3.png"),
                                              load_image("Enemy/Destroy_Phoenix4.png"),
                                              load_image("Enemy/Destroy_Phoenix5.png"),
                                              load_image("Enemy/Destroy_Phoenix6.png")])
            cls._IMAGE.setdefault("Stop", [load_image("Enemy/Enemy_Phoenix_Stop1.png"),
                                           load_image("Enemy/Enemy_Phoenix_Stop2.png")])
            cls._IMAGE.setdefault("Attack", [load_image("Enemy/Enemy_Phoenix_AttackLight1.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight2.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight3.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight4.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight5.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight6.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight7.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight8.png"),
                                             load_image("Enemy/Enemy_Phoenix_AttackLight9.png")])
            cls._INIT_FLAG_IMAGE = True

    @classmethod
    def _init_sound(cls):
        if not cls._INIT_FLAG_SOUND:
            from LostViking.src.generic_loader.sound_loader import load_sound
            from LostViking.src.constants import MAIN_VOLUME
            cls._SOUND.setdefault("Shield", load_sound("Shield.wav", MAIN_VOLUME - 0.3))
            cls._SOUND.setdefault("Laser", load_sound("Laser.wav", MAIN_VOLUME - 0.2))
            cls._SOUND.setdefault("Explode", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                              load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])
            cls._INIT_FLAG_SOUND = True

    @classmethod
    def init(cls):
        if not cls._INIT_FLAG:
            cls._init_image()
            cls._init_acc()
            cls._init_speed()
            cls._init_sound()
            cls._MAX_HEALTH = 100
            cls._SCORE = 200
            cls._INIT_FLAG = True


"""
class Shield(pygame.sprite.Sprite):
    Shield_MaxHealth = 900
    SHIELDS = pygame.sprite.Group()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = Shield.Shield_MaxHealth
        self.image_switch = 0
        self.image = self.mainImage[0]
        self.active = True
        self.get_hit = False
        self.rect = self.image.get_rect()
        self.image_switch_interval = MYTIME(1)

    def hit(self, damage):
        SOUNDS["Shield"].stop()
        SOUNDS["Shield"].play()
        if self.health <= 0:
            self.active = False
        else:
            self.health -= damage
            self.get_hit = True
            Shield.SHIELDS.add(self)

    def update(self, rect):
        if self.get_hit:
            self.change_image()
        self.rect.center = rect.center

    def change_image(self):
        self.image_switch_interval.tick()
        if self.image_switch_interval.check():
            self.image_switch = (self.image_switch + 1) % len(self.mainImage)
            self.image = self.mainImage[self.image_switch]
            if self.image_switch == 0:
                self.get_hit = False
                Shield.SHIELDS.remove(self)

    @classmethod
    def LOAD(cls):
        cls.mainImage = PHOENIX_IMAGE["Shield"]
"""
