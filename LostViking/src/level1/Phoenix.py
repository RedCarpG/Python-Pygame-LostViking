from ..enemy.EnemyIII import EnemyIII
from .level1_group import Enemy_Phoenix_G
from ..groups import Enemy_Bullet_G, Shield_G
from ..generic_items.BasicBullet import BasicSpinBullet
from ..generic_items.ImageHelper import SingleImageHelper
from ..generic_items.SoundHelper import SoundHelper
from ..generic_items.ImageHelper import LoopImageHelper
import pygame


class EnemyPhoenix(SoundHelper, EnemyIII):

    def __init__(self, pos, side):
        SoundHelper.__init__(self)
        EnemyIII.__init__(self, pos, side)
        self.add(Enemy_Phoenix_G)

        self.shield = Shield(self)

    def __del__(self):
        self.shield.kill()
        del self.shield

    # Rewrite hit to add Shield
    def hit(self, damage=100):
        if self.shield.is_active:
            self.shield.hit(damage)
        else:
            super().hit(damage)

    def _shoot(self):
        BulletPhoenix(self.rect.center, self.angle)
        # Bullet.BULLETS.add(Bullet_Phoenix(self.rect.center, self._angle))

    @classmethod
    def _init_image(cls):
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._INIT_FLAG_IMAGE:
            cls._IMAGE = dict()
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
        if not hasattr(cls, "_INIT_FLAG_SOUND") or not cls._INIT_FLAG_SOUND:
            cls._SOUND = dict()
            from LostViking.src.generic_loader.sound_loader import load_sound
            from LostViking.src.constants import MAIN_VOLUME
            cls._SOUND.setdefault("Shield", load_sound("Shield.wav", MAIN_VOLUME - 0.3))
            cls._SOUND.setdefault("Laser", load_sound("Laser.wav", MAIN_VOLUME - 0.2))
            cls._SOUND.setdefault("Explode", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                              load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])
            cls._INIT_FLAG_SOUND = True

    @classmethod
    def init(cls):
        super().init()
        if not hasattr(cls, "_INIT_FLAG") or not cls._INIT_FLAG:
            cls._init_image()
            cls._init_sound()
            cls._MAX_HEALTH = 100
            cls._SCORE = 200
            cls._INIT_FLAG = True


class BulletPhoenix(SingleImageHelper, BasicSpinBullet):

    def __init__(self, position, angle):
        self.init()
        SingleImageHelper.__init__(self)
        BasicSpinBullet.__init__(self, position, angle)
        self.add(Enemy_Bullet_G)

    @classmethod
    def _init_image(cls):
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._INIT_FLAG_IMAGE:
            from ..generic_loader.image_loader import load_image
            cls._IMAGE = load_image("Enemy/laser.png")
            cls._INIT_FLAG_IMAGE = True

    @classmethod
    def init(cls):
        if not hasattr(cls, "_INIT_FLAG") or not cls._INIT_FLAG:
            cls._init_image()
            cls._MAX_SPEED_X = cls._MAX_SPEED_Y = 15
            cls._INIT_FLAG = True


class Shield(LoopImageHelper, SoundHelper, pygame.sprite.DirtySprite):

    def __init__(self, owner):
        if not hasattr(self, "_INIT_FLAG") or not self._INIT_FLAG:
            raise Exception("!!! ERROR class not init! {}".format(self))
        LoopImageHelper.__init__(self)
        SoundHelper.__init__(self)
        pygame.sprite.DirtySprite.__init__(self, Shield_G)

        self.health = self._MAX_HEALTH

        self.is_active = True
        self.dirty = 2
        self.visible = 0

        self.rect = self.image.get_rect()
        self._set_image_type("Normal")

        self.owner = owner

    def hit(self, damage):
        self._play_sound('Shield')
        if self.health <= 0:
            self.is_active = False
            self.health = 0
        else:
            self.health -= damage
            self.visible = 1

    def _reposition(self):
        self.rect.center = self.owner.rect.center

    def update(self):
        if self.visible:
            self._reposition()
            if self._switch_image():
                self.visible = 0

    @classmethod
    def _init_image(cls):
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._INIT_FLAG_IMAGE:
            cls._IMAGE = dict()
            from ..generic_loader.image_loader import load_image
            cls._IMAGE["Base"] = [load_image("Enemy/Shield1.png")]
            cls._IMAGE.setdefault("Normal", [load_image("Enemy/Shield1.png"),
                                             load_image("Enemy/Shield2.png"),
                                             load_image("Enemy/Shield3.png"),
                                             load_image("Enemy/Shield4.png"),
                                             load_image("Enemy/Shield5.png")])
            cls._INIT_FLAG_IMAGE = True

    @classmethod
    def _init_sound(cls):
        if not hasattr(cls, "_INIT_FLAG_SOUND") or not cls._INIT_FLAG_SOUND:
            cls._SOUND = dict()
            from ..generic_loader.sound_loader import load_sound
            from ..constants import MAIN_VOLUME
            cls._SOUND.setdefault("Shield", load_sound("Shield.wav", MAIN_VOLUME - 0.3))
            cls._INIT_FLAG_SOUND = True

    @classmethod
    def init(cls):
        if not hasattr(cls, "_INIT_FLAG") or not cls._INIT_FLAG:
            cls._init_sound()
            cls._init_image()
            cls._MAX_HEALTH = 900
            cls._INIT_FLAG = True
