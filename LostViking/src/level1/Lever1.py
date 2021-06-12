from GLOBAL import *
from LostViking.LostViking import *
from LostViking.src.enemy.enemyPlane import *
from LostViking.src.generic_items.BasicBullet import *
from LostViking.src.generic_loader.mytime import *





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
