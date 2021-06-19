from ..enemy.EnemyBoss import EnemyBoss
from .Enemy_Interceptor import EnemyInterceptor


class EnemyCarrier(EnemyBoss):
    MAX_INTERCEPTOR_NUMBER = 9

    SEND_INTERCEPTOR_INTERVAL = 10

    _ATTACK_SPEED = 500

    def __init__(self):
        EnemyBoss.__init__(self)

        self._count_send_interceptor_interval = self.SEND_INTERCEPTOR_INTERVAL
        self.enter_attack_phase()

    def _action_attack(self, *args, **kwargs):
        if EnemyInterceptor.NUM < self.MAX_INTERCEPTOR_NUMBER:
            if self._count_send_interceptor_interval <= 0:
                self._count_send_interceptor_interval = self.SEND_INTERCEPTOR_INTERVAL
                pos = self.rect.center
                EnemyInterceptor(pos, [[pos[0], pos[1] + 300]])
            else:
                self._count_send_interceptor_interval -= 1
        else:
            self.enter_attack_idle_phase()

    @classmethod
    def _init_image(cls):
        cls.IMAGE = dict()
        from ..generic_loader.image_loader import load_image
        cls.IMAGE["BASE"] = [load_image("Enemy/Carrier.png")]
        cls.IMAGE["IDLE"] = [load_image("Enemy/Carrier.png")]
        cls.IMAGE["EXPLODE"] = [load_image("Enemy/Carrier.png")]
        cls._IS_SET_IMAGE = True

    @classmethod
    def _init_sound(cls):
        cls._SOUND = dict()
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("Explode", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                          load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])


