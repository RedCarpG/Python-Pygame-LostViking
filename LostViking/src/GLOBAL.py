from LostViking.src.generic.sound import *
from LostViking.src.generic.image import *
from enum import Enum

# 主音量
MAIN_VOLUME = 1
# 颜色
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 背景卷动速度
BG_SPEED = 25


SOUNDS = {}
PHOENIX_IMAGE = {}
# SCOUT_IMAGE = {}
BULLET_IMAGE = {}
VIKING_IMAGE = {}
SUPPLY_IMAGE = {}
CARRIER_IMAGE = {}
INTERCEPTOR_IMAGE = {}

# 画面大小
class SCREEN:
    SIZE = WIDTH, HEIGHT = (1500, 1000)

    @classmethod
    def ChangeScreenSize(self, width, height):
        self.SIZE = (width, height)
        self.WIDTH = width
        self.HEIGHT = height

    @classmethod
    def getH(self):
        return self.HEIGHT

    @classmethod
    def getW(self):
        return self.WIDTH

    @classmethod
    def getS(self):
        return self.SIZE

class G():
    SCORE = 0
    LIFE = 3
    BOMB = 3


def LOAD_IMAGE():
    # 加载图片
    BULLET_IMAGE.clear()
    VIKING_IMAGE.clear()
    SUPPLY_IMAGE.clear()

    SUPPLY_IMAGE.setdefault("Life", load_image_alpha("Supply/bullet.png"))
    SUPPLY_IMAGE.setdefault("Bomb", load_image_alpha("Supply/bomb.png"))
    SUPPLY_IMAGE.setdefault("Bullet", load_image_alpha("Supply/bullet.png"))
    BULLET_IMAGE.setdefault("Viking_Bullet", load_image_alpha("MyPlane/bullet.png"))
    VIKING_IMAGE.setdefault("Body", load_image_alpha("MyPlane\Viking_body.png"))
    VIKING_IMAGE.setdefault("Invincible", load_image_alpha("MyPlane\Myplane_Invincible.png"))
    VIKING_IMAGE.setdefault("MoveUp", [load_image_alpha("MyPlane\Myplane_moveUp1.png"),
                                       load_image_alpha("MyPlane\Myplane_moveUp2.png")])
    VIKING_IMAGE.setdefault("MoveDown", [load_image_alpha("MyPlane\Myplane_moveDown1.png"),
                                         load_image_alpha("MyPlane\Myplane_moveDown2.png")])
    VIKING_IMAGE.setdefault("MoveNormal", [load_image_alpha("MyPlane\Myplane_moveNormal1.png"),
                                           load_image_alpha("MyPlane\Myplane_moveNormal2.png")])
    VIKING_IMAGE.setdefault("Explode", [load_image_alpha("MyPlane\Myplane_explode1.png"),
                                        load_image_alpha("MyPlane\Myplane_explode2.png"),
                                        load_image_alpha("MyPlane\Myplane_explode3.png"),
                                        load_image_alpha("MyPlane\Myplane_explode4.png"),
                                        load_image_alpha("MyPlane\Myplane_explode5.png"),
                                        load_image_alpha("MyPlane\Myplane_explode6.png")])

def LOAD_IMAGE_LEVER1():
    PHOENIX_IMAGE.clear()
    CARRIER_IMAGE.clear()
    INTERCEPTOR_IMAGE.clear()

    BULLET_IMAGE.setdefault("Phoenix_Bullet", load_image_alpha("Enemy/bullet.png"))
    BULLET_IMAGE.setdefault("Phoenix_Laser", load_image_alpha("Enemy/laser.png"))
    PHOENIX_IMAGE.setdefault("Normal", [load_image_alpha("Enemy\Enemy_Phoenix1.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix2.png")])
    PHOENIX_IMAGE.setdefault("Stop", [load_image_alpha("Enemy\Enemy_Phoenix_Stop1.png"),
                                      load_image_alpha("Enemy\Enemy_Phoenix_Stop2.png")])
    PHOENIX_IMAGE.setdefault("Shield", [load_image_alpha("Enemy\Sheild1.png"),
                                        load_image_alpha("Enemy\Sheild2.png"),
                                        load_image_alpha("Enemy\Sheild3.png"),
                                        load_image_alpha("Enemy\Sheild4.png"),
                                        load_image_alpha("Enemy\Sheild5.png")])
    PHOENIX_IMAGE.setdefault("Destroy", [load_image_alpha("Enemy\Destroy_Phoenix1.png"),
                                         load_image_alpha("Enemy\Destroy_Phoenix2.png"),
                                         load_image_alpha("Enemy\Destroy_Phoenix3.png"),
                                         load_image_alpha("Enemy\Destroy_Phoenix4.png"),
                                         load_image_alpha("Enemy\Destroy_Phoenix5.png"),
                                         load_image_alpha("Enemy\Destroy_Phoenix6.png")])
    PHOENIX_IMAGE.setdefault("Attack", [load_image_alpha("Enemy\Enemy_Phoenix_AttakLight1.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight2.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight3.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight4.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight5.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight6.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight7.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight8.png"),
                                        load_image_alpha("Enemy\Enemy_Phoenix_AttakLight9.png")])
    INTERCEPTOR_IMAGE.setdefault("Body", load_image_alpha("Enemy\Interceptor.png"))
    CARRIER_IMAGE.setdefault("Body", load_image_alpha("Enemy\Carrier.png"))

def UNLOAD_IMAGE_LEVER1():
    PHOENIX_IMAGE.clear()
    # SCOUT_IMAGE.clear()
    CARRIER_IMAGE.clear()
    INTERCEPTOR_IMAGE.clear()

def LOAD_SOUNDS():
    # 加载音效
    SOUNDS.clear()
    SOUNDS.setdefault("Shield", load_sound("Shield.wav", MAIN_VOLUME - 0.3))
    SOUNDS.setdefault("Player_Shoot", load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
    SOUNDS.setdefault("Laser", load_sound("Laser.wav", MAIN_VOLUME - 0.2))
    SOUNDS.setdefault("Explosion", [load_sound("Explo.wav", MAIN_VOLUME - 0.4),
                                    load_sound("Explo2.wav", MAIN_VOLUME - 0.2)])
    SOUNDS.setdefault("Player_Explo", load_sound("Player_Explo.wav", MAIN_VOLUME))
    SOUNDS.setdefault("NuclearLaunch_Detected", load_sound("NuclearLaunch_Detected.wav", MAIN_VOLUME - 0.1))
    SOUNDS.setdefault("NuclearMissle_Ready", load_sound("NuclearMissle_Ready.wav", MAIN_VOLUME - 0.1))
    SOUNDS.setdefault("UI1", load_sound("UI1.wav", MAIN_VOLUME - 0.2))
    SOUNDS.setdefault("Liftoff1", load_sound("Liftoff1.wav", MAIN_VOLUME))
    SOUNDS.setdefault("Liftoff2", load_sound("Liftoff2.wav", MAIN_VOLUME - 0.2))
    SOUNDS.setdefault("Error", load_sound("Error.wav", MAIN_VOLUME))
