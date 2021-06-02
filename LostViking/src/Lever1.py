import random
from GLOBAL import *
from LostViking.LostViking import *
from LostViking.src.entity.enemyPlane import *
from LostViking.src.entity.bullet import *
from math import sin, cos
from LostViking.src.generic.mytime import *


# Enemy 类
class Enemy_Carrier(Enemy_Boss):
    mainImage = []
    crashImage = []
    shootImage = []
    sendInterceptorImage = []
    destroySound = None
    CARRIER_BULLET_NUMBER = 9

    def __init__(self):
        Enemy_Boss.__init__(self)
        self.move_interval = MYTIME(250)
        self.stay_interval = MYTIME(250)
        self.attack1_flag = False
        self.attack2_flag = False
        self.move_flag = False
        self.attack1_interval = MYTIME(2000, 1850)
        self.attack2_interval = MYTIME(1800, 900)
        self.sendI_interval = MyTime2(25)
        self.shoot_interval = MyTime2(25)
        self.speedY = 9
        self.speedX = 0
        self.directionX = 1
        self.accelerate = [0.1, 0.1]

    def action(self):
        if self.speedY > 0:
            self.rect.top += self.speedY
            self.speedY -= self.accelerate[1]
        else:
            if self.move_flag:
                self.move_interval.tick()
                if self.move_interval.check():
                    self.move_flag = False
            else:
                self.stay_interval.tick()
                if self.speedX > 0:
                    self.speedX -= self.accelerate[0]
                elif self.stay_interval.check():
                    self.move_flag = True
                    self.directionX = random.choice((-1, 1))
                    self.speedX = 2
            self.rect.left += self.speedX * self.directionX

            self.attack1_interval.tick()
            if self.attack1_interval.check():
                self.attack1_flag = True
            self.attack2_interval.tick()
            if self.attack2_interval.check():
                self.attack2_flag = True
            if self.rect.left < 0 or self.rect.right > SCREEN.get_w():
                self.directionX = -self.directionX

    def attack(self, point):
        if self.attack1_flag:
            if self.sendI_interval.check() and Enemy_Interceptor.NUM < 9:
                add_enemy_Interceptor(self.rect.center)

            if self.sendI_interval.check_count(9):
                self.attack1_flag = False
            self.sendI_interval.tick()

        if self.attack2_flag:
            if self.shoot_interval.check():
                if self.rect.center[1] == point[1]:
                    if point[0] > self.rect.center[0]:
                        angle = 90
                    else:
                        angle = -90
                elif self.rect.center[0] == point[0]:
                    if point[1] > self.rect.center[1]:
                        angle = 0
                    else:
                        angle = 180
                else:
                    angle = math.atan((point[0] - self.rect.center[0]) / (point[1] - self.rect.center[1]))
                    angle = angle * 360 / 2 / math.pi
                    if self.rect.center[1] > point[1]:
                        if self.rect.center[0] < point[0]:
                            angle += 180
                        else:
                            angle -= 180
                Bullet.BULLETS.add(Bullet_Phoenix((self.rect.center[0] + 10, self.rect.center[1] + 100), angle + 2))
                Bullet.BULLETS.add(Bullet_Phoenix((self.rect.center[0] - 10, self.rect.center[1] + 100), angle - 2))
            if self.shoot_interval.check_count(self.CARRIER_BULLET_NUMBER):
                self.attack2_flag = False
            self.shoot_interval.tick()

    @classmethod
    def LOAD(cls):
        cls.mainImage = [CARRIER_IMAGE["Body"]]
        cls.crashImage = [CARRIER_IMAGE["Body"]]
        cls.destroySound = SOUNDS["Explosion"][1]


class Enemy_Interceptor(EnemyII):
    INTERCEPTOR_MaxHealth = 1000
    INTERCEPTOR_MaxSpeed = 10.0
    INTERCEPTOR_Score = 500
    NUM = 0
    main_image = []
    crashImage = []

    def __init__(self, pos, path):
        EnemyII.__init__(self, pos, path)
        self.health = self.INTERCEPTOR_MaxHealth
        self.score = self.INTERCEPTOR_Score
        self.speed = [0.0, self.INTERCEPTOR_MaxSpeed]
        self.move_rad = 200
        self.move_interval = MYTIME(80)
        self.stay_interval = MYTIME(15)
        self.move_flag = True
        self.rotate_flag = False
        self.attack_flag = False
        self.stage1_flag = True
        Enemy_Interceptor.NUM += 1

    def update(self, point):
        self.change_image()
        self.action()
        self.shoot(point)

    def brake(self):
        self.speed[0] *= 0.8
        self.speed[1] *= 0.8

    def action(self):
        if self.stage1_flag:
            self.rect.move_ip(self.speed[0], self.speed[1])
            if self.rect.collidepoint(self.path[0]):
                self.stage1_flag = False
                self.current_path = 1
                self.move_flag = False
        else:
            if self.rotate_flag:
                x = random.randint(self.rect.center[0] - self.move_rad, self.rect.center[0] + self.move_rad)
                y = random.randint(self.rect.center[1] - self.move_rad, self.rect.center[1] + self.move_rad)
                self.path[1] = [x, y]
                self.rotate(self.path[self.current_path])
                self.rotate_flag = False
                self.move_flag = True

            if self.move_flag:
                self.move_interval.tick()
                if self.rect.collidepoint(self.path[self.current_path]):
                    self.move_interval.reset()
                    self.move_flag = False
                if self.move_interval.check():
                    self.move_flag = False
                self.rect.move_ip(self.speed[0], self.speed[1])
            else:
                if abs(self.speed[0]) > 0.1 or abs(self.speed[1]) > 0.1:
                    self.brake()
                    self.rect.move_ip(self.speed[0], self.speed[1])
                self.stay_interval.tick()
                if self.stay_interval.check():
                    self.rotate_flag = True
                    self.attack_flag = True

        if self.rect.top < 0 or self.rect.bottom > SCREEN.getH() - SCREEN.getH() / 3 or self.rect.left < 0 or self.rect.right > SCREEN.get_w():
            if self.rect.top < 0:
                self.rect.top = 0
                self.path[0][1] = -self.path[0][1]
            elif self.rect.bottom > SCREEN.getH() - SCREEN.getH() / 3:
                self.rect.bottom = SCREEN.getH() - SCREEN.getH() / 3
                self.path[0][1] = 2 * (SCREEN.getH() - SCREEN.getH() / 3) - self.path[0][1]
            if self.rect.left < 0:
                self.rect.left = 0
                self.path[0][0] = -self.path[0][0]
            elif self.rect.right > SCREEN.get_w():
                self.rect.right = SCREEN.get_w()
                self.path[0][0] = 2 * SCREEN.get_w() - self.path[0][0]
            self.rotate(self.path[0])

    def shoot(self, point):
        if self.attack_flag:
            if random.randint(0, 10) == 0:
                if self.rect.center[1] == point[1]:
                    if point[0] > self.rect.center[0]:
                        angle = 90
                    else:
                        angle = -90
                elif self.rect.center[0] == point[0]:
                    if point[1] > self.rect.center[1]:
                        angle = 0
                    else:
                        angle = 180
                else:
                    angle = math.atan((point[0] - self.rect.center[0]) / (point[1] - self.rect.center[1]))
                    angle = angle * 360 / 2 / math.pi
                    if self.rect.center[1] > point[1]:
                        if self.rect.center[0] < point[0]:
                            angle += 180
                        else:
                            angle -= 180
                Bullet.BULLETS.add(Bullet_Interceptor(self.rect.center, angle))
        self.attack_flag = False

    def rotate(self, point):
        if self.rect.center[1] == point[1]:
            if point[0] > self.rect.center[0]:
                angle = 90
            else:
                angle = -90
        elif self.rect.center[0] == point[0]:
            if point[1] > self.rect.center[1]:
                angle = 0
            else:
                angle = 180
        else:
            angle = math.atan((point[0] - self.rect.center[0]) / (point[1] - self.rect.center[1]))
            angle = angle * 360 / 2 / math.pi
            if self.rect.center[1] > point[1]:
                if self.rect.center[0] < point[0]:
                    angle += 180
                else:
                    angle -= 180
        self.angle = angle
        angle = angle * math.pi / 180
        self.speed = [float(self.INTERCEPTOR_MaxSpeed * math.sin(angle)),
                      float(self.INTERCEPTOR_MaxSpeed * math.cos(angle))]
        temp = self.rect.center
        self.image = pygame.transform.rotate(self.mainImage[self.image_switch], self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = temp

    def __del__(self):
        Enemy_Interceptor.NUM -= 1

    @classmethod
    def LOAD(cls):
        cls.mainImage = [INTERCEPTOR_IMAGE["Body"]]
        cls.crashImage = [INTERCEPTOR_IMAGE["Body"]]
        n = random.choice((0, 1))
        cls.destroySound = SOUNDS["Explosion"][n]


class Enemy_Scout(EnemyI):
    SCOUT_MaxHealth = 100
    SCOUT_MaxSpeed = 5
    SCOUT_Score = 100

    def __init__(self, pos):
        EnemyI.__init__(self, pos)
        self.health = self.SCOUT_MaxHealth
        self.speed = [0, self.SCOUT_MaxSpeed]
        self.score = self.SCOUT_Score

    @classmethod
    def LOAD(cls):
        cls.mainImage = PHOENIX_IMAGE["Normal"]
        cls.crashImage = PHOENIX_IMAGE["Destroy"]
        cls.destroySound = SOUNDS["Explosion"][0]


class Enemy_Phoenix(EnemyIII):
    PHOENIX_MaxHealth = 100
    PHOENIX_Score = 200

    def __init__(self, pos, side):
        EnemyIII.__init__(self, pos)
        self.health = Enemy_Phoenix.PHOENIX_MaxHealth
        self.score = Enemy_Phoenix.PHOENIX_Score
        self.side = side
        self.angle = 90 * side
        self.stay = 1000
        self.attack_interval = MYTIME(100)
        self.speed = [10, 1]
        self.accelerateX = 0.1
        self.stage1_flag = True
        self.stage2_flag = False
        self.stage3_flag = False
        self.shield = Shield()

    # 增加 Shield
    def hit(self, damage=100):
        if self.shield.active:
            self.shield.hit(damage)
        else:
            self.health -= damage
            if self.health <= 0:
                self.active = False

    def update(self, player_point):
        self.change_image()
        if self.entrance_flag:
            self.entrance()
        else:
            self.action(player_point)
            if self.stay_duration.tick() > 500:
                self.leave()
        self.shield.update(self.rect)


    def brake(self):
        self.speed[0] += -self.accelerateX

    def shoot(self):
        Bullet.BULLETS.add(Bullet_Phoenix(self.rect.center, self.angle))

    def entrance(self):
        if self.speed[0] > 0:
            self.brake()
            self.rect.right += self.speed[0] * self.side
        else:
            self.entrance_flag = False
            self.mainImage = PHOENIX_IMAGE["Stop"]

    @classmethod
    def LOAD(cls):
        cls.attackImage = PHOENIX_IMAGE["Attack"]
        cls.mainImage = PHOENIX_IMAGE["Normal"]
        cls.crashImage = PHOENIX_IMAGE["Destroy"]
        cls.attackSound = SOUNDS["Laser"]
        cls.destroySound = SOUNDS["Explosion"][1]


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


from pygame.locals import *


# Level1 类
class Level1():
    CREATE_Scout = USEREVENT + 3
    CREATE_Phoenix = USEREVENT + 4
    CREATE_Carrier = USEREVENT + 5
    enemy_Interceptor = pygame.sprite.Group()
    enemy_Scout = pygame.sprite.Group()
    enemy_Phoenix = pygame.sprite.Group()
    enemy_Carrier = pygame.sprite.GroupSingle()

    def __init__(self):
        LOAD_IMAGE_LEVER1()
        Enemy_Scout.LOAD()
        Enemy_Phoenix.LOAD()
        Enemy_Carrier.LOAD()
        Enemy_Interceptor.LOAD()
        Shield.LOAD()

        add_enemy_Scout(5)
        # 定时生成敌机
        pygame.time.set_timer(self.CREATE_Carrier, 30000)
        pygame.time.set_timer(self.CREATE_Phoenix, 20000)
        pygame.time.set_timer(self.CREATE_Scout, 500)

    def events(self, event):
        if event.type == self.CREATE_Scout:
            if len(self.enemy_Scout.sprites()) < 25:
                add_enemy_Scout(1)
                print("CREATE_Scout:")
            return True
        elif event.type == self.CREATE_Phoenix:
            add_enemy_Phoenix()
            print("CREATE_Phoenix:")
            return True
        elif event.type == self.CREATE_Carrier:
            pygame.time.set_timer(self.CREATE_Scout, 0)
            pygame.time.set_timer(self.CREATE_Phoenix, 0)
            pygame.time.set_timer(self.CREATE_Carrier, 0)
            pygame.time.set_timer(Game.CREATE_SUPPLY, 40000)
            add_enemy_Carrier()
            print("CREATE_Carrier:")
            return True
        return False

    def update(self, point):
        Level1.enemy_Interceptor.update(point)
        Level1.enemy_Scout.update()
        Level1.enemy_Phoenix.update(point)
        Level1.enemy_Carrier.update(point)

    def __del__(self):
        UNLOAD_IMAGE_LEVER1()


# 生成敌机
def add_enemy_Scout(num):
    for i in range(num):
        x = random.randint(50, SCREEN.get_w() - 50)
        y = random.randint(-0.5 * SCREEN.getH(), 0 - 100)

        scout = Enemy_Scout([x, y])
        Level1.enemy_Scout.add(scout)


def add_enemy_Phoenix():
    x1 = SCREEN.get_w() + 200
    x2 = - 200
    y = 200
    phoenix1 = Enemy_Phoenix((x1, y), -1)
    phoenix2 = Enemy_Phoenix((x2, y), 1)
    Level1.enemy_Phoenix.add([phoenix1, phoenix2])


def add_enemy_Interceptor(pos):
    path = [[pos[0], pos[1] + 300], [0, 0]]
    I = Enemy_Interceptor(pos, path)
    Level1.enemy_Interceptor.add(I)


def add_enemy_Carrier():
    carrier = Enemy_Carrier()
    Level1.enemy_Carrier.add(carrier)


import pygame
import traceback
from pygame.locals import *


def main():
    # 初始化Pygame
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN.change_screen_size(800, 800)
    screen = pygame.display.set_mode((SCREEN.get_w(), SCREEN.get_w()))
    # 加载图片音效
    LOAD_IMAGE_LEVER1()
    LOAD_SOUNDS()
    Enemy_Carrier.LOAD()
    Enemy_Interceptor.LOAD()
    Enemy_Phoenix.LOAD()
    Enemy_Scout.LOAD()
    # ----------------------------------------------------------
    # 创建 组
    # -- Scout
    S = Enemy_Scout((400, 200))
    Level1.enemy_Scout.add(S)
    # -- Phoenix
    P = Enemy_Phoenix((0, 100), 1)
    Level1.enemy_Phoenix.add(P)
    # -- Carrier
    # C = Enemy_Carrier()
    # Level1.enemy_Carrier.add(C)
    # -- Interceptor
    # I = Enemy_Interceptor([100, 100], [[100, 500], [0, 0]])
    # Level1.enemy_Interceptor.add(I)
    # ----------------------------------------------------------
    running = True
    while running:
        # ------------------------------------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        # ------------------------------------------------------
        clock.tick(60)
        # ------------------------------------------------------
        # 更新 Enemies 组
        Level1.enemy_Interceptor.update((500, 800))
        Level1.enemy_Scout.update()
        Level1.enemy_Phoenix.update((500, 800))
        Level1.enemy_Carrier.update((500, 800))
        # 更新 Bullet 组
        Bullet.BULLETS.update()
        # ------------------------------------------------------
        screen.fill(BLACK)
        # 渲染 组
        Bullet.BULLETS.draw(screen)
        Enemy.ENEMYS.draw(screen)
        Enemy.BOSS.draw(screen)
        # 显示
        pygame.display.flip()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
