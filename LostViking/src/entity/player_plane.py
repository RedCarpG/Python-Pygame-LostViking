from LostViking.src.GLOBAL import *
from LostViking.src.generic.image import *
from bullet import *
from player_bullet import PlayerBulletType


class MyPlane(pygame.sprite.Sprite):
    PLAYER_SPEED_X = 8
    PLAYER_SPEED_UP = 10
    PLAYER_SPEED_DOWN = 5

    Player_G = pygame.sprite.GroupSingle(None)
    Player_Bullet_G = pygame.sprite.Group()

    def __init__(self, pos=None, sort=1):
        pygame.sprite.Sprite.__init__(self)

        self.rect = VIKING_IMAGE["Body"].get_rect()
        self.image_up = VIKING_IMAGE["MoveUp"]
        self.downImage = VIKING_IMAGE["MoveDown"]
        self.normalImage = VIKING_IMAGE["MoveNormal"]
        self.mainImage = self.normalImage
        self.crashImage = VIKING_IMAGE["Explode"]
        self.invincibleImage = VIKING_IMAGE["Invincible"]
        self.image = self.mainImage[0]

        self.image_switch = 0
        self.set_pos(pos)

        self.speed = [0, 0]
        self.accelerate = [0.8, 1, 0.6]
        self.direction = [0, 0]
        self.move_flag = [False, False]

        self.current_time = 0
        self.active = True
        self.invincible_flag = False
        self.invincible_reset = 0
        self.crash_animation = 0
        self.bullet_type = PlayerBulletType.Bullet1
        self.lever = 1

    def set_pos(self, point=None):
        if point is None:
            self.rect.center = (int(SCREEN.getW() // 2), int(SCREEN.getH() - self.rect.height // 2 - 30))
        else:
            self.rect.center = point

    def change_image(self, ticks, rate=60):
        if self.active:
            if self.direction[1] == -1:
                self.mainImage = self.image_up
            elif self.direction[1] == 1:
                self.mainImage = self.downImage
            else:
                self.mainImage = self.normalImage
        if ticks > self.current_time + rate:
            self.current_time = ticks
            self.image_switch = (self.image_switch + 1) % len(self.mainImage)
            self.image = self.mainImage[self.image_switch]
        elif self.invincible_flag:
            self.image = self.invincibleImage

    def update(self, ticks):
        self.invincible(ticks)
        if self.active:
            self.rect.move_ip(self.speed)
            self.brake()
        elif self.image_switch == len(self.mainImage) - 1:
            self.invincible_flag = True
            self.reset()
        self.change_image(ticks)

    def move_up(self):
        self.direction[1] = -1
        self.move_flag[1] = True
        if self.rect.top > 0:
            if self.speed[1] > -self.PLAYER_SPEED_UP:
                self.speed[1] += -self.accelerate[1]
        else:
            self.speed[1] = 0
            self.rect.top = 0

    def move_back(self):
        self.direction[1] = 1
        self.move_flag[1] = True
        if self.rect.bottom < SCREEN.getH():
            if self.speed[1] < self.PLAYER_SPEED_DOWN:
                self.speed[1] += self.accelerate[2]
        else:
            self.speed[1] = 0
            self.rect.bottom = SCREEN.getH()

    def move_left(self):
        self.direction[0] = -1
        self.move_flag[0] = True
        if self.rect.left > 0:
            if self.speed[0] > -self.PLAYER_SPEED_X:
                self.speed[0] += -self.accelerate[0]
        else:
            self.speed[0] = 0
            self.rect.left = 0

    def move_right(self):
        self.direction[0] = 1
        self.move_flag[0] = True
        if self.rect.right < SCREEN.getW():
            if self.speed[0] < self.PLAYER_SPEED_X:
                self.speed[0] += self.accelerate[0]
        else:
            self.speed[0] = 0
            self.rect.right = SCREEN.getW()

    def brake(self):
        if self.speed == [0, 0]:
            return
        if not self.move_flag[0]:
            if self.speed[0] > 0:
                self.speed[0] += -self.accelerate[0]
                if self.speed[0] <= 0:
                    self.speed[0] = 0
                    self.direction[0] = 0
            elif self.speed[0] < 0:
                self.speed[0] += self.accelerate[0]
                if self.speed[0] >= 0:
                    self.speed[0] = 0
                    self.direction[0] = 0
        if not self.move_flag[1]:
            if self.speed[1] > 0:
                self.direction[1] = 0
                self.speed[1] += -self.accelerate[1]
                if self.speed[1] <= 0:
                    self.speed[1] = 0
                    self.direction[1] = 0
            elif self.speed[1] < 0:
                self.direction[1] = 1
                self.speed[1] += self.accelerate[2]
                if self.speed[1] >= 0:
                    self.speed[1] = 0
                    self.direction[1] = 0

    def hit(self):
        if not self.invincible_flag:
            self.active = False
            self.image_switch = 0
            self.mainImage = self.crashImage
            SOUNDS["Player_Explo"].play()
            return True
        else:
            return False

    def shoot(self):
        b = []
        position1 = self.rect.center[0] - 10, self.rect.center[1]
        position2 = self.rect.center[0] + 10, self.rect.center[1]
        if self.bullet_type == PlayerBulletType.Bullet1:
            if self.lever == 1:
                b1 = PlayerBullet1(position1, -1)
                b2 = PlayerBullet1(position2, 1)
                b = [b1, b2]
            elif self.lever == 2:
                b1 = PlayerBullet1(position1, -1)
                b2 = PlayerBullet1(position2, 1)
                b3 = PlayerBullet1(position1, -2)
                b4 = PlayerBullet1(position2, 2)
                b = [b1, b2, b3, b4]
            elif self.lever == 3:
                b1 = PlayerBullet1(position1, -1)
                b2 = PlayerBullet1(position2, 1)
                b3 = PlayerBullet1(position1, -2)
                b4 = PlayerBullet1(position2, 2)
                b5 = PlayerBullet1(position1, -3)
                b6 = PlayerBullet1(position2, 3)
                b = [b1, b2, b3, b4, b5, b6]
            MyPlane.Player_Bullet_G.add(b)

    def invincible(self, ticks, rate=60):
        if self.invincible_flag:
            if self.current_time < ticks + rate:
                self.invincible_reset = (self.invincible_reset + 1) % 50
                if self.invincible_reset == 49:
                    self.invincible_flag = False

    def reset(self, pos=None):
        self.active = True
        self.image_switch = 0
        self.invincible_flag = True
        self.mainImage = self.normalImage
        self.bullet_type = PlayerBulletType.Bullet1
        self.lever = 1
        if not pos:
            pos = int(SCREEN.getW() // 2), \
                  int(SCREEN.getH() - self.rect.height // 2 - 60)
        self.rect.center = pos
        self.direction = [0, 0]

    def set_bullet(self, bul_type):
        if self.bullet_type != bul_type:
            self.lever = 2
            self.bullet_type = bul_type
        elif self.lever < 3:
            self.lever += 1



if __name__ == "__main__":
    import pygame, sys
    from pygame.locals import *

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 1000))

    # Event
    event_player_shoot = USEREVENT
    event_nuc_launch = USEREVENT + 1

    BULLET_IMAGE.setdefault("Viking_Bullet", load_image_alpha("MyPlane/bullet.png"))

    VIKING_IMAGE.setdefault("Invincible", load_image_alpha("MyPlane\Myplane_Invincible.png"))
    VIKING_IMAGE.setdefault("Body", load_image_alpha("MyPlane\Viking_body.png"))
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
    SOUNDS.setdefault("Player_Shoot", load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
    SOUNDS.setdefault("Player_Explo", load_sound("Player_Explo.wav", MAIN_VOLUME))
    SOUNDS.setdefault("NuclearLaunch_Detected", load_sound("NuclearLaunch_Detected.wav", MAIN_VOLUME - 0.1))
    SOUNDS.setdefault("NuclearMissle_Ready", load_sound("NuclearMissle_Ready.wav", MAIN_VOLUME - 0.1))

    player = MyPlane()
    player.set_bullet(PlayerBulletType.Bullet1)
    player.set_bullet(PlayerBulletType.Bullet1)
    p_g = pygame.sprite.Group()
    p_g.add(player)
    b_g = MyPlane.Player_Bullet_G
    # 延时
    running = True
    while running:

        clock.tick(60)
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                # 空格键射�?
                if event.key == K_SPACE:
                    pygame.event.post(pygame.event.Event(event_player_shoot, {}))
                    pygame.time.set_timer(event_player_shoot, 200)
                    # Q键投掷核�?
                if event.key == K_q:
                    if nuclear_bomb > 0 and NB.active == False:
                        nuclear_bomb -= 1
                        bomb_text.change_text("Bomb: " + str(nuclear_bomb))
                        SOUNDS["NuclearLaunch_Detected"].stop()
                        SOUNDS["NuclearLaunch_Detected"].play()
                        pygame.event.post(pygame.event.Event(event_nuc_launch, {}))
                    else:
                        SOUNDS["Error"].stop()
                        SOUNDS["Error"].play()

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    pygame.time.set_timer(event_player_shoot, 0)
                if event.key == K_w:
                    player.move_flag[1] = False
                if event.key == K_s:
                    player.move_flag[1] = False
                if event.key == K_a:
                    player.move_flag[0] = False
                if event.key == K_d:
                    player.move_flag[0] = False
                if event.key == K_UP:
                    player.move_flag[1] = False
                if event.key == K_DOWN:
                    player.move_flag[1] = False
                if event.key == K_LEFT:
                    player.move_flag[0] = False
                if event.key == K_RIGHT:
                    player.move_flag[0] = False

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.event.post(pygame.event.Event(event_player_shoot, {}))
                    pygame.time.set_timer(event_player_shoot, 200)

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    pygame.time.set_timer(event_player_shoot, 0)

            elif event.type == event_player_shoot:
                SOUNDS["Player_Shoot"].stop()
                SOUNDS["Player_Shoot"].play()
                player.shoot()

            elif event.type == event_nuc_launch:
                NB.active = True
                NB.rect.center = player.rect.midtop

        # 检测用户键盘操�?
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.move_back()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.move_right()

        screen.fill(BLACK)
        p_g.update(ticks)
        p_g.draw(screen)
        b_g.update()
        b_g.draw(screen)
        # 显示
        pygame.display.flip()
    pygame.quit()
    sys.exit()
