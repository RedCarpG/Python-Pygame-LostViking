from player_bullet import *
from LostViking.src.GLOBAL import *


class MyPlane(pygame.sprite.Sprite):
    PLAYER_MAX_SPEED_X = 8
    PLAYER_MAX_SPEED_UP = 10
    PLAYER_MAX_SPEED_DOWN = 5
    PLAYER_ACC_X = 0.8
    PLAYER_ACC_UP = 1
    PLAYER_ACC_DOWN = 0.6

    INIT_FLAG = False

    Player_G = pygame.sprite.GroupSingle(None)
    Player_Bullet_G = pygame.sprite.Group()

    def __init__(self, pos=None, sort=1):
        pygame.sprite.Sprite.__init__(self)

        ''' Init images from loaded image in PLAYER_IMAGE '''
        # If not initialized yet
        if not MyPlane.INIT_FLAG:
            MyPlane.init_player_plane_image()
        # Main image list
        self.mainImage = PLAYER_IMAGE["MoveNormal"]
        # Current image
        self.image_switch = 0
        self.image = self.mainImage[self.image_switch]

        ''' Init Rect '''
        self.rect = PLAYER_IMAGE["Body"].get_rect()

        ''' Init Position '''
        self.set_pos(pos)

        ''' Init Movement properties '''
        self.speed_x = 0
        self.speed_y = 0
        self.direction_x = 0
        self.direction_y = 0
        self.move_flag_x = False
        self.move_flag_y = False

        ''' Init States '''
        self.is_active = True
        self.is_invincible = False
        # self.invincible_reset = 0
        # self.crash_animation = 0

        self.current_time = 0
        self.lever = 1

        ''' Init Weapon '''
        self.bullet_type = PlayerBulletType.Bullet1

    """ Real-time methods """
    def update(self, ticks):
        #self.invincible(ticks)
        if self.is_active:
            # Move if speed is not 0
            if self.move_flag_y or self.move_flag_x:
                self.rect.move_ip(self.speed_x, self.speed_y)
            # Speed down if there's no movement command on X or Y
            self.brake()
        elif self.image_switch == len(self.mainImage) - 1:
            self.is_invincible = True
            self.reset()
        self.switch_image(ticks)

    def invincible(self, ticks, rate=60):
        if self.is_invincible:
            if self.current_time < ticks + rate:
                self.invincible_reset = (self.invincible_reset + 1) % 50
                if self.invincible_reset == 49:
                    self.is_invincible = False

    # Switch image
    def switch_image(self, ticks, rate=60):
        if ticks > self.current_time + rate:
            self.current_time = ticks
            self.image_switch = (self.image_switch + 1) % len(self.mainImage)
            self.image = self.mainImage[self.image_switch]
        elif self.is_invincible:
            self.image = PLAYER_IMAGE["Invincible"]

    # Speed down the plane when there's no movement commands on a X or Y direction
    def brake(self):
        # If no speed
        if self.speed_x == 0 and self.speed_y == 0:
            return
        else:
            # If no move X command but speed_x != 0
            if not self.move_flag_x:
                if self.speed_x > 0:            # If it is moving right
                    self.speed_x -= self.PLAYER_ACC_X
                    if self.speed_x <= 0:
                        self.speed_x = 0
                elif self.speed_x < 0:          # If it is moving left
                    self.speed_x += self.PLAYER_ACC_X
                    if self.speed_x >= 0:
                        self.speed_x = 0
            # If no move Y command but speed_y != 0
            if not self.move_flag_y:
                if self.speed_y > 0:            # If it is moving down
                    self.speed_y -= self.PLAYER_ACC_UP
                    if self.speed_y <= 0:
                        self.speed_y = 0
                        self.mainImage = PLAYER_IMAGE["MoveNormal"]
                elif self.speed_y < 0:          # If it is moving up
                    self.speed_y += self.PLAYER_ACC_DOWN
                    if self.speed_y >= 0:
                        self.speed_y = 0
                        self.mainImage = PLAYER_IMAGE["MoveNormal"]

    """ -- Trigger-Movement-Commands (Instant trigger method called by events) -- """

    # Trigger Move Up 
    def trigger_move_up(self):
        # If it was not moving before, change image
        if not self.move_flag_y:
            self.move_flag_y = True
            self.mainImage = PLAYER_IMAGE["MoveUp"]
        # If not outside the screen
        if self.rect.top > 0:
            # If speed doesn't reach limit
            if self.speed_y > -self.PLAYER_MAX_SPEED_UP:
                self.speed_y += -self.PLAYER_ACC_UP
        else:
            self.speed_y = 0
            self.rect.top = 0

    # Trigger Move Down
    def trigger_move_back(self):
        # If it was not moving before, change image
        if not self.move_flag_y:
            self.move_flag_y = True
            self.mainImage = PLAYER_IMAGE["MoveDown"]
        # If not outside the screen
        if self.rect.bottom < SCREEN.get_h():
            # If speed doesn't reach limit
            if self.speed_y < self.PLAYER_MAX_SPEED_DOWN:
                self.speed_y += self.PLAYER_ACC_DOWN
        else:
            self.speed_y = 0
            self.rect.bottom = SCREEN.get_h()

    # Trigger Move Left
    def trigger_move_left(self):
        self.move_flag_x = True
        # If not outside the screen
        if self.rect.left > 0:
            # If speed doesn't reach limit
            if self.speed_x > -self.PLAYER_MAX_SPEED_X:
                self.speed_x += -self.PLAYER_ACC_X
        else:
            self.speed_x = 0
            self.rect.left = 0

    # Trigger Move Right
    def trigger_move_right(self):
        self.move_flag_x = True
        # If not outside the screen
        if self.rect.right < SCREEN.get_w():
            # If speed doesn't reach limit
            if self.speed_x < self.PLAYER_MAX_SPEED_X:
                self.speed_x += self.PLAYER_ACC_X
        else:
            self.speed_x = 0
            self.rect.right = SCREEN.get_w()

    # Trigger Brake y, only triggered when lease the button
    def trigger_brake_y(self):
        self.move_flag_y = False

    # Trigger Brake x
    def trigger_brake_x(self):
        self.move_flag_x = False
    ''' -- End of Trigger-Movement-Commands -- '''

    def hit(self):
        if not self.is_invincible:
            self.is_active = False
            self.image_switch = 0
            self.mainImage = PLAYER_IMAGE["Explode"]
            RESOURCES.SOUNDS["Player_Explo"].play()
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

    # Set position
    def set_pos(self, point=None):
        if point is None:
            self.rect.center = (int(SCREEN.get_w() // 2), int(SCREEN.get_h() - self.rect.height // 2 - 30))
        else:
            self.rect.center = point

    # Reset
    def reset(self, pos=None):
        self.is_active = True
        self.image_switch = 0
        self.is_invincible = True
        self.mainImage = PLAYER_IMAGE["MoveNormal"]
        self.bullet_type = PlayerBulletType.Bullet1
        self.lever = 1
        if not pos:
            pos = int(SCREEN.get_w() // 2), \
                  int(SCREEN.get_h() - self.rect.height // 2 - 60)
        self.rect.center = pos
        self.direction = [0, 0]

    # Set Bullet Type
    def set_bullet_type(self, bul_type):
        if self.bullet_type != bul_type:
            self.lever = 2
            self.bullet_type = bul_type
        elif self.lever < 3:
            self.lever += 1

    """ Class init methods"""
    @classmethod
    def init_player_plane_image(cls):
        PLAYER_IMAGE.setdefault("Body", load_image_alpha("MyPlane/Viking_body.png"))
        PLAYER_IMAGE.setdefault("Invincible", load_image_alpha("MyPlane/MyPlane_Invincible.png"))
        PLAYER_IMAGE.setdefault("MoveUp", [load_image_alpha("MyPlane/MyPlane_moveUp1.png"),
                                           load_image_alpha("MyPlane/MyPlane_moveUp2.png")])
        PLAYER_IMAGE.setdefault("MoveDown", [load_image_alpha("MyPlane/MyPlane_moveDown1.png"),
                                             load_image_alpha("MyPlane/MyPlane_moveDown2.png")])
        PLAYER_IMAGE.setdefault("MoveNormal", [load_image_alpha("MyPlane/MyPlane_moveNormal1.png"),
                                               load_image_alpha("MyPlane/MyPlane_moveNormal2.png")])
        PLAYER_IMAGE.setdefault("Explode", [load_image_alpha("MyPlane/MyPlane_explode1.png"),
                                            load_image_alpha("MyPlane/MyPlane_explode2.png"),
                                            load_image_alpha("MyPlane/MyPlane_explode3.png"),
                                            load_image_alpha("MyPlane/MyPlane_explode4.png"),
                                            load_image_alpha("MyPlane/MyPlane_explode5.png"),
                                            load_image_alpha("MyPlane/MyPlane_explode6.png")])
        cls.INIT_FLAG = True

    @classmethod
    def clear_player_plane_image(cls):
        PLAYER_IMAGE.clear()
        cls.INIT_FLAG = False


if __name__ == "__main__":
    import pygame
    import sys
    from LostViking.src.GLOBAL import *
    from pygame.locals import *

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 1000))

    # Event
    event_player_shoot = USEREVENT
    event_nuc_launch = USEREVENT + 1

    MyPlane.init_player_plane_image()
    PlayerBullet1.init_player_bullet()
    """
    SOUNDS.setdefault("Player_Shoot", load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
    SOUNDS.setdefault("Player_Explo", load_sound("Player_Explo.wav", MAIN_VOLUME))
    SOUNDS.setdefault("NuclearLaunch_Detected", load_sound("NuclearLaunch_Detected.wav", MAIN_VOLUME - 0.1))
    SOUNDS.setdefault("NuclearMissle_Ready", load_sound("NuclearMissle_Ready.wav", MAIN_VOLUME - 0.1))
    """
    player = MyPlane()
    player.set_bullet_type(PlayerBulletType.Bullet1)
    player.set_bullet_type(PlayerBulletType.Bullet1)
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
                # Space Button
                if event.key == K_SPACE:
                    pygame.event.post(pygame.event.Event(event_player_shoot, {}))
                    pygame.time.set_timer(event_player_shoot, 200)
                # Q Button
                if event.key == K_q:
                    if nuclear_bomb > 0 and NB.is_active == False:
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
                    player.trigger_brake_y()
                if event.key == K_s:
                    player.trigger_brake_y()
                if event.key == K_a:
                    player.trigger_brake_x()
                if event.key == K_d:
                    player.trigger_brake_x()
                if event.key == K_UP:
                    player.trigger_brake_y()
                if event.key == K_DOWN:
                    player.trigger_brake_y()
                if event.key == K_LEFT:
                    player.trigger_brake_x()
                if event.key == K_RIGHT:
                    player.trigger_brake_x()

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
                NB.is_active = True
                NB.rect.center = player.rect.midtop

        # If Key Pressed?
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.trigger_move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.trigger_move_back()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.trigger_move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.trigger_move_right()

        screen.fill(BLACK)
        p_g.update(ticks)
        p_g.draw(screen)
        b_g.update()
        b_g.draw(screen)
        # 显示
        pygame.display.flip()
    pygame.quit()
    sys.exit()
