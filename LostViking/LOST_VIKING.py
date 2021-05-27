import pygame, sys
from pygame.locals import *
import traceback

if not pygame.font: print("Warning, fonts disabled!")
if not pygame.mixer: print("Warning, sounds disabled!")

from myPlane import *
from GLOBAL import *
from sound import *
from LostViking.src.generic.font import *
from supply import *
from Lever1 import *


def col(a, b):
    if pygame.sprite.collide_rect(a, b):
        if pygame.sprite.collide_rect_ratio(0.5)(a, b):
            return True
    return False


class Enter:

    def enter(self, screen, clock):
        # 加载播放 enter界面音乐
        Main.MUSIC = ['bgm.ogg', 'bgm2.ogg']
        load_music(Main.MUSIC, MAIN_VOLUME - 0.7)
        # enter音乐播放
        pygame.mixer.music.play(0)
        # 加载 enter界面背景
        Main.BACKGROUND = load_image("Space.png")
        # enter界面字体
        begin_font = load_font("arialbd.ttf", 50)
        title_font = load_font("arialbd.ttf", 120)
        begin_text = myFont(screen, begin_font, "Press Space To Begin", (0, 0), color=WHITE)
        title_text = myFont(screen, title_font, "LOST VIKING", (0, 0), color=WHITE)
        title_text.move_center((screen.get_width() // 2, screen.get_height() // 2))
        begin_text.move_center((screen.get_width() // 2, 3 * screen.get_height() // 5))
        UI1 = load_sound("UI1.wav", MAIN_VOLUME - 0.2)
        # enter入场等待
        enter = True
        delay = 100
        while enter:
            # 绘制背景，文本
            screen.fill(BLACK)
            title_text.blit()
            if delay % 5:
                begin_text.blit()
            pygame.display.flip()
            # 全部事件
            for event in pygame.event.get():
                # 退出事件
                if event.type == QUIT:
                    pygame.font.quit()
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
                # 按键事件
                elif event.type == KEYDOWN:
                    # 按ESCAPE退出
                    if event.key == K_ESCAPE:
                        pygame.font.quit()
                        pygame.mixer.quit()
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_SPACE or event.key == K_RETURN:
                        UI1.play()
                        begin = False
                        enter = False
            delay = (delay - 1) % 100
            # 帧数设置
            clock.tick(10)


class Game:
    # 定义事件
    PLAYER_SHOOT = USEREVENT
    NUCLEAR_LAUNCH = USEREVENT + 1
    CREATE_SUPPLY = USEREVENT + 2

    def __init__(self, screen):
        #  ---------------------- 初始化 ---------------------- #
        self.screen = screen  # 初始化 屏幕
        # -* 初始化 字体样式 *-
        self.score_font = load_font("arialbd.ttf", 30)  # 分数 字体
        # self.life_font = load_font("arialbd.ttf", 30)   # 生命 字体
        # -* 初始化 组 *-
        # · 功能道具 组
        self.supplies = pygame.sprite.Group()
        self.bomb = pygame.sprite.GroupSingle()
        self.shields = Shield.SHIELDS
        # · 敌方飞机组，存储所有敌方飞机
        self.enemies = Enemy.ENEMYS
        self.enemy_bullets = Bullet.BULLETS
        self.enemies_hit = Enemy.ENEMYS_HIT
        self.enemies_die = Enemy.ENEMYS_DIE
        self.boss = Enemy.BOSS
        self.players = pygame.sprite.GroupSingle()
        self.player_bullets = MyPlane.PLAYER_Bullets
        # -* 设置时钟 *-
        pygame.time.set_timer(self.CREATE_SUPPLY, 10000)
        # -* 定义退出游戏条件 *-
        self.running = True
        # -* 加载音乐 *-
        # Main.MUSIC = ['bgm2.ogg', 'bgm.ogg']
        # load_music(Main.MUSIC, MAIN_VOLUME)
        pygame.mixer.music.play(1)
        # -* 加载背景 *-
        Main.BACKGROUND = load_image("Space.png")

        # -* 加载图片和音频
        LOAD_IMAGE()
        LOAD_SOUNDS()
        # · 显示分数和道具 文字
        self.score_text = myFont(self.screen, self.score_font, ("Score: " + str(G.SCORE)), (0, 30), color=WHITE)
        self.life_text = myFont(self.screen, self.score_font, ("Life: " + str(G.LIFE)), (0, 60), color=WHITE)
        self.bomb_text = myFont(self.screen, self.score_font, ("Bomb: " + str(G.BOMB)), (0, 90), color=WHITE)
        # 生成我方飞机
        self.player_number = 1
        if self.player_number == 1:
            self.player = MyPlane()
        self.players.add(self.player)
        # 加载关卡
        self.Lever = Level1()

    def play(self, clock):
        # 主循�?
        while self.running:
            clock.tick(60)
            ticks = pygame.time.get_ticks()

            self.Events()
            self.Collide()
            self.Blit()
            # 更新
            self.Update(ticks)

        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()

    def Events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                # 空格键射�?
                if event.key == K_SPACE:
                    pygame.event.post(pygame.event.Event(self.PLAYER_SHOOT, {}))
                    pygame.time.set_timer(self.PLAYER_SHOOT, 200)
                    # Q键投掷核�?
                if event.key == K_q:
                    if G.BOMB > 0:
                        if len(self.bomb) == 0:
                            G.BOMB -= 1
                            self.bomb_text.change_text("Bomb: " + str(G.BOMB))
                            SOUNDS["NuclearLaunch_Detected"].stop()
                            SOUNDS["NuclearLaunch_Detected"].play()
                            nuclear_bomb = Nuclear_Bomb(self.player.rect.center)
                            self.bomb.add(nuclear_bomb)
                    else:
                        SOUNDS["Error"].stop()
                        SOUNDS["Error"].play()

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    pygame.time.set_timer(self.PLAYER_SHOOT, 0)
                if event.key == K_w:
                    self.player.move_flag[1] = False
                if event.key == K_s:
                    self.player.move_flag[1] = False
                if event.key == K_a:
                    self.player.move_flag[0] = False
                if event.key == K_d:
                    self.player.move_flag[0] = False
                if event.key == K_UP:
                    self.player.move_flag[1] = False
                if event.key == K_DOWN:
                    self.player.move_flag[1] = False
                if event.key == K_LEFT:
                    self.player.move_flag[0] = False
                if event.key == K_RIGHT:
                    self.player.move_flag[0] = False

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.event.post(pygame.event.Event(self.PLAYER_SHOOT, {}))
                    pygame.time.set_timer(self.PLAYER_SHOOT, 400)

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    pygame.time.set_timer(self.PLAYER_SHOOT, 0)

            elif event.type == self.PLAYER_SHOOT:
                SOUNDS["Player_Shoot"].stop()
                SOUNDS["Player_Shoot"].play()
                self.player.shoot()

            elif self.Lever.events(event):
                pass

            elif event.type == self.CREATE_SUPPLY:
                n = random.randint(1, 10)
                if n < 3:
                    self.supplies.add(Supply.create(SUPPLY_TYPE(0)))
                elif n > 8:
                    self.supplies.add(Supply.create(SUPPLY_TYPE(2)))
                else:
                    self.supplies.add(Supply.create(SUPPLY_TYPE(1)))

        # 检测用户键盘操�?
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            self.player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.player.moveBack()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.player.moveRight()

    def Collide(self):
        supply_get = pygame.sprite.spritecollideany(self.player, self.supplies)
        if supply_get != None:
            if pygame.sprite.collide_circle_ratio(0.65)(self.player, supply_get):
                supply_get.catched(self.player)
                G.SCORE += supply_get.score
                if supply_get.type == SUPPLY_TYPE.Bomb:
                    self.bomb_text.change_text("Bomb: " + str(G.BOMB))
                elif supply_get.type == SUPPLY_TYPE.Life:
                    self.life_text.change_text("Life: " + str(G.LIFE))

        if self.player.active and not self.player.invicible_flag:
            bullet_hit = pygame.sprite.spritecollideany(self.player, self.enemy_bullets)
            if bullet_hit != None:
                if pygame.sprite.collide_rect_ratio(0.65)(self.player, bullet_hit):
                    if self.player.hit():
                        bullet_hit.kill()
                        G.LIFE -= 1
            enemy_hit = pygame.sprite.spritecollideany(self.player, self.enemies)
            if enemy_hit != None:
                if pygame.sprite.collide_rect_ratio(0.65)(self.player, enemy_hit):
                    if enemy_hit.active:
                        if self.player.hit():
                            if enemy_hit not in self.boss:
                                enemy_hit.active = False
                                enemy_hit.destroy()
                                enemy_hit.kill()
                                self.enemies_die.add(enemy_hit)
                            G.LIFE -= 1

        self.enemies_hit.add(pygame.sprite.groupcollide(self.enemies, self.player_bullets, False, True, col))
        if len(self.enemies_hit) > 0:
            for each in self.enemies_hit:
                each.hit()
                if not each.active:
                    G.SCORE += each.score
                    each.destroy()
                    each.kill()
                    self.enemies_die.add(each)
                self.enemies_hit.remove(each)

        if len(self.bomb) > 0:
            if self.bomb.sprite.active and self.bomb.sprite.explode_flag:
                self.bomb.sprite.active = False
                for each in self.enemies:
                    if each.rect.bottom > 0 and each.active:
                        each.hit(800)
                        if not each.active:
                            G.SCORE += each.score
                            each.destroy()
                            each.kill()
                            self.enemies_die.add(each)
                self.enemy_bullets.empty()

        self.life_text.change_text("Life: " + str(G.LIFE))
        self.score_text.change_text("Score: " + str(G.SCORE))

    def Blit(self):
        # 星空背景
        self.screen.fill(BLACK)
        self.screen.blit(Main.BACKGROUND, (0, 0))
        if self.boss.sprite:
            pygame.draw.rect(self.screen, (100, 200, 100, 180), Rect(0, 0, SCREEN.getW(), 25), 3)
            pygame.draw.rect(self.screen, (100, 200, 100, 180),
                             Rect(0, 0, SCREEN.getW() * self.boss.sprite.health / self.boss.sprite.maxHealth, 25))

        # 绘制字体
        self.score_text.blit()
        self.life_text.blit()
        self.bomb_text.blit()
        #
        self.supplies.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.bomb.draw(self.screen)
        self.players.draw(self.screen)
        self.boss.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemies_die.draw(self.screen)
        self.shields.draw(self.screen)
        #

    def Update(self, ticks):
        self.supplies.update()
        self.player.update(ticks)
        self.enemy_bullets.update()
        self.player_bullets.update()
        self.Lever.update(self.player.rect.center)
        self.bomb.update()

        for each in self.enemies_die:
            if each.image_switch == len(each.mainImage) - 1:
                each.kill()
            each.change_image()
        # 显示
        pygame.display.flip()


class Main:
    MUSIC = ['bgm2.ogg', 'bgm.ogg']
    BACKGROUND = None

    # 初始化游戏
    def __init__(self):
        # 初始化ppygame
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        # 窗口标题
        pygame.display.set_caption("LOST VIKING")
        # 加载音乐
        load_music(Main.MUSIC, MAIN_VOLUME)

        self.screen = pygame.display.set_mode(SCREEN.SIZE, DOUBLEBUF)
        self.clock = pygame.time.Clock()  # 初始化 时钟

    def begin_animation(self):

        # 生成背景
        BG = load_image_alpha("BackGround.png")
        BG2 = load_image_alpha("BackGround2.png")
        BG_rect = BG.get_rect()
        BG2_rect = BG2.get_rect()
        BG_rect.bottom = SCREEN.getH()
        BG2_rect.bottom = SCREEN.getH()
        accelerate = 0
        DELAY = 100
        lift_flag1 = 0
        lift_flag2 = 0
        init_speed = 0
        end_flag = -1
        SOUNDS["Liftoff2"].play()

        while begin:
            self.screen.blit(BACKGROUND, (0, 0))

            if BG2 is not None:
                self.screen.blit(BG2, BG2_rect)
            if BG is not None:
                self.screen.blit(BG, BG_rect)
            # 绘制我方飞机   
            self.player.blit()

            if init_speed < BG_SPEED:
                accelerate += 0.005
                init_speed += accelerate

            if BG2_rect.top >= screen.get_height():
                if end_flag == -1:
                    end_flag = 50
                self.player.direction[1] = 0
            elif BG_rect.top >= screen.get_height() // 2:
                if lift_flag2 == 0:
                    lift_flag2 = 1
                    SOUNDS["Liftoff2"].play()

            if self.player.rect.bottom > 2 * screen.get_height() // 3:
                if init_speed > 2:
                    self.player.direction[1] = -1
                    if lift_flag1 == 0:
                        lift_flag1 = 1
                        SOUNDS["Liftoff1"].play()
                        # BG_rect1.top += init_speed
                self.player.rect.top -= init_speed
            else:
                BG_rect.top += init_speed
                BG2_rect.top += 1 * init_speed // 6
            if end_flag > 0:
                end_flag -= 1
            elif end_flag == 0:
                begin = False
            DELAY = (DELAY - 1) % 100
            # 显示
            pygame.display.flip()
            # 帧数设置
            self.clock.tick(60)

    def game(self):
        e = Enter()
        e.enter(self.screen, self.clock)
        # self.begin_animation()
        g = Game(self.screen)
        g.play(self.clock)


def main():
    m = Main()
    m.game()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
