from abc import ABC

from player_bullet import *
from LostViking.src.GLOBAL import *
from general_entity import *


class MyPlane(InertialEntity, pygame.sprite.Sprite):
    MAX_SPEED_X = 8
    MAX_SPEED_UP = 10
    MAX_SPEED_DOWN = 5
    ACC_X = 0.8
    ACC_UP = 1
    ACC_DOWN = 0.6

    Player_G = pygame.sprite.GroupSingle(None)

    # Player_Bullet_G = pygame.sprite.Group()

    def __init__(self, point=None, sort=1):
        InertialEntity.__init__(self, point)
        pygame.sprite.Sprite.__init__(self, self.Player_G)

        self.set_image_type("MoveNormal")

        ''' Init images from loaded image in self.IMAGE '''

        ''' Init States '''
        self.is_active = True
        self.is_invincible = False
        # self.invincible_reset = 0
        # self.crash_animation = 0

        ''' Init Weapon '''
        self.bullet_type = PlayerBulletType.Bullet1
        self.lever = 1

    """ Real-time methods """

    def update(self):
        if self.is_active:
            # Move if speed is not 0
            if self.speed_y != 0 or self.speed_x != 0:
                self._move()
                # Speed down if there's no movement command on X or Y
                self._inertial_deceleration()
        else:
            self.reset()
        self._switch_image()

    """
    def invincible(self, ticks, rate=60):
        if self.is_invincible:
            if self.current_time < ticks + rate:
                self.invincible_reset = (self.invincible_reset + 1) % 50
                if self.invincible_reset == 49:
                    self.is_invincible = False
    """

    """ -- Trigger-Movement-Commands (Instant trigger method called by events) -- """

    # Trigger Move Up 
    def trigger_move_up(self):
        # If it was not moving before, change image
        if not self._move_flag_y:
            self.set_image_type("MoveUp")
        # If not outside the screen
        if self.rect.top > 0:
            self.accelerate_up()
        else:
            self.speed_y = 0
            self.rect.top = 0

    # Trigger Move Down
    def trigger_move_back(self):
        # If it was not moving before, change image
        if not self._move_flag_y:
            self.set_image_type("MoveDown")
        # If not outside the screen
        if self.rect.bottom < SCREEN.get_h():
            self.accelerate_down()
        else:
            self.speed_y = 0
            self.rect.bottom = SCREEN.get_h()

    # Trigger Move Left
    def trigger_move_left(self):
        # If not outside the screen
        if self.rect.left > 0:
            self.accelerate_left()
        else:
            self.speed_x = 0
            self.rect.left = 0

    # Trigger Move Right
    def trigger_move_right(self):
        # If not outside the screen
        if self.rect.right < SCREEN.get_w():
            self.accelerate_right()
        else:
            self.speed_x = 0
            self.rect.right = SCREEN.get_w()

    # Trigger Brake y, only triggered when lease the button
    def trigger_stop_y(self):
        self._move_flag_y = False

    # Trigger Brake x
    def trigger_stop_x(self):
        self._move_flag_x = False

    ''' -- End of Trigger-Movement-Commands -- '''
    """
    def hit(self):
        if not self.is_invincible:
            self.is_active = False
            self.image_switch = 0
            self.mainImage = self.IMAGE["Explode"]
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
    
    # Set Bullet Type
    def set_bullet_type(self, bul_type):
        if self.bullet_type != bul_type:
            self.lever = 2
            self.bullet_type = bul_type
        elif self.lever < 3:
            self.lever += 1
    """


    # Reset
    def reset(self, point=None):
        self.is_active = True
        self._image_switch = 0
        self._set_pos(point)
        # self.is_invincible = True
        self.set_image_type("MoveNormal")
        self.bullet_type = PlayerBulletType.Bullet1
        self.lever = 1

    """ Class init methods"""

    @classmethod
    def _init_image(cls):
        cls.IMAGE["Base"] = [load_image_alpha("MyPlane/Viking_body.png")]
        cls.IMAGE.setdefault("Invincible", [load_image_alpha("MyPlane/MyPlane_Invincible.png")])
        cls.IMAGE.setdefault("MoveUp", [load_image_alpha("MyPlane/MyPlane_moveUp1.png"),
                                        load_image_alpha("MyPlane/MyPlane_moveUp2.png")])
        cls.IMAGE.setdefault("MoveDown", [load_image_alpha("MyPlane/MyPlane_moveDown1.png"),
                                          load_image_alpha("MyPlane/MyPlane_moveDown2.png")])
        cls.IMAGE.setdefault("MoveNormal", [load_image_alpha("MyPlane/MyPlane_moveNormal1.png"),
                                            load_image_alpha("MyPlane/MyPlane_moveNormal2.png")])
        cls.IMAGE.setdefault("Explode", [load_image_alpha("MyPlane/MyPlane_explode1.png"),
                                         load_image_alpha("MyPlane/MyPlane_explode2.png"),
                                         load_image_alpha("MyPlane/MyPlane_explode3.png"),
                                         load_image_alpha("MyPlane/MyPlane_explode4.png"),
                                         load_image_alpha("MyPlane/MyPlane_explode5.png"),
                                         load_image_alpha("MyPlane/MyPlane_explode6.png")])
        cls.INIT_FLAG = True

    @classmethod
    def _clear_image(cls):
        cls.IMAGE.clear()
        cls.INIT_FLAG = False


if __name__ == "__main__":
    import sys
    from LostViking.src.GLOBAL import *
    from pygame.locals import *

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN.WIDTH, SCREEN.HEIGHT))

    # Event
    # event_player_shoot = USEREVENT
    # event_nuc_launch = USEREVENT + 1

    # PlayerBullet1.init_player_bullet()
    """
    SOUNDS.setdefault("Player_Shoot", load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
    SOUNDS.setdefault("Player_Explo", load_sound("Player_Explo.wav", MAIN_VOLUME))
    SOUNDS.setdefault("NuclearLaunch_Detected", load_sound("NuclearLaunch_Detected.wav", MAIN_VOLUME - 0.1))
    SOUNDS.setdefault("NuclearMissle_Ready", load_sound("NuclearMissle_Ready.wav", MAIN_VOLUME - 0.1))
    """
    player = MyPlane()
    # player.set_bullet_type(PlayerBulletType.Bullet1)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                """
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
                """
            elif event.type == KEYUP:
                #if event.key == K_SPACE:
                    #pygame.time.set_timer(event_player_shoot, 0)
                if event.key == K_w:
                    player.trigger_stop_y()
                if event.key == K_s:
                    player.trigger_stop_y()
                if event.key == K_a:
                    player.trigger_stop_x()
                if event.key == K_d:
                    player.trigger_stop_x()
                if event.key == K_UP:
                    player.trigger_stop_y()
                if event.key == K_DOWN:
                    player.trigger_stop_y()
                if event.key == K_LEFT:
                    player.trigger_stop_x()
                if event.key == K_RIGHT:
                    player.trigger_stop_x()
            """
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
            """
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
        MyPlane.Player_G.update()
        MyPlane.Player_G.draw(screen)
        #b_g.update()
        #b_g.draw(screen)
        # 显示
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
