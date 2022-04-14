from tkinter.messagebox import NO
from src.game.generic_items.Enemy import EnemyBoss
# from .Enemy_Interceptor import EnemyInterceptor
from src.game.animation import AttachEffect
from src.helper.image import get_image
from src.util.type import Pos


class EnemyCarrier(EnemyBoss):
    MAX_INTERCEPTOR_NUMBER = 9

    SEND_INTERCEPTOR_INTERVAL = 10

    ATTACK_SPEED = 500

    def __init__(self):
        EnemyBoss.__init__(
            self,
            frames={
                "BASE": get_image("Enemy/Carrier/CarrierBase.png"),
                "IDLE": get_image("Enemy/Carrier/CarrierNormal.png"),
                "DESTROY": get_image("Enemy/Carrier/CarrierDestroy.png"),
                "HIT": get_image("Enemy/Carrier/CarrierHit.png"),
                "ATTACK": get_image("Enemy/Carrier/CarrierAttack.png")
            },
            frame_size=None
        )
        self.intercepter_count = 0

        self._count_send_interceptor_interval = self.SEND_INTERCEPTOR_INTERVAL

    # --------------- Override Methods --------------- #
    def shoot(self, *args, **kwargs):
        from .Scout import EnemyScout
        EnemyScout(Pos(self.rect.center))
        pass
        # if EnemyInterceptor.NUM < self.MAX_INTERCEPTOR_NUMBER:
        #     if self._count_send_interceptor_interval <= 0:
        #         self._count_send_interceptor_interval = self.SEND_INTERCEPTOR_INTERVAL
        #         pos = self.rect.center
        #         EnemyInterceptor(pos, [[pos[0], pos[1] + 300]])
        #     else:
        #         self._count_send_interceptor_interval -= 1
        # else:
        #     self.enter_attack_idle_phase()

    def attack(self, target):
        if self._count_attack_interval > 0:
            self._count_attack_interval -= 1
        else:

            if self.intercepter_count < self.MAX_INTERCEPTOR_NUMBER:

                if self._count_send_interceptor_interval > 0:
                    self._count_send_interceptor_interval -= 1
                else:
                    self._count_send_interceptor_interval = self.SEND_INTERCEPTOR_INTERVAL

                    def _attack_cb():
                        if self.is_active:
                            self.shoot(target)

                    AttachEffect(
                        self,
                        frames={
                            "IDLE": self.frames["ATTACK"]
                        },
                        frame_size=None,
                        enable_rotate=False,
                        cb_func=_attack_cb
                    )
                    self.intercepter_count += 1
            else:
                self._count_attack_interval = self.ATTACK_SPEED

    @classmethod
    def add_enemy_carrier(cls):
        EnemyCarrier()
