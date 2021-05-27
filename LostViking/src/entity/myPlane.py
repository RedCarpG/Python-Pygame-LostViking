
from GLOBAL import *
from LostViking.src.generic.image import *
from bullet import *

class MyPlane(pygame.sprite.Sprite):
    PLAYER_xSpeed = 8
    PLAYER_UpSpeed = 10
    PLAYER_BackSpeed = 5
    PLAYER_Bullets = pygame.sprite.Group()

    def __init__(self, pos=None, sort=1):
        pygame.sprite.Sprite.__init__(self)
        self.setImage(sort)
        self.image_switch = 0
        self.setPos(pos)

        self.speed = [0, 0]
        self.accelerate = [0.8, 1, 0.6]
        self.direction = [0, 0]
        self.move_flag = [False, False]

        self.current_time = 0
        self.active = True
        self.invicible_flag = False
        self.reset_invincible = 0
        self.crash_animation = 0
        self.bullet_type = PLAYER_BULLET.Bullet1
        self.lever = 1

    def setPos(self,point=None):        
        if point == None:
            self.rect.center = ( int(SCREEN.getW() // 2), int(SCREEN.getH() - self.rect.height // 2 - 30 ))
        else:
            self.rect.center = point

    def change_image(self,ticks,rate=60):
        if self.active:
            if self.direction[1] == -1:
                self.mainImage = self.upImage
            elif self.direction[1] == 1 :
                self.mainImage = self.downImage
            else:
                self.mainImage = self.normalImage
        if ticks > self.current_time + rate:
            self.current_time = ticks
            self.image_switch = (self.image_switch+1)%len(self.mainImage)
            self.image = self.mainImage[self.image_switch]
        elif self.invicible_flag:
            self.image = self.invincibleImage

    def setImage(self,sort):
        self.rect = VIKING_IMAGE["Body"].get_rect()
        self.upImage = VIKING_IMAGE["MoveUp"]
        self.downImage = VIKING_IMAGE["MoveDown"]
        self.normalImage = VIKING_IMAGE["MoveNormal"]
        self.mainImage = self.normalImage
        self.crashImage = VIKING_IMAGE["Explode"]
        self.invincibleImage = VIKING_IMAGE["Invincible"]
        self.image = self.mainImage[0]

    def update(self, ticks):
        self.Invincible(ticks)
        if self.active:
            self.rect.move_ip(self.speed)
            self.brake()
        elif self.image_switch == len(self.mainImage)-1:
            self.invicible_flag = True
            self.reset()
        self.change_image(ticks)

    def moveUp(self):
        self.direction[1] = -1
        self.move_flag[1] = True
        if self.rect.top > 0 :
            if self.speed[1] > -self.PLAYER_UpSpeed:
                self.speed[1] += -self.accelerate[1]
        else :
            self.speed[1] = 0
            self.rect.top = 0
    def moveBack(self):
        self.direction[1] = 1
        self.move_flag[1] = True
        if self.rect.bottom < SCREEN.getH():
            if self.speed[1] < self.PLAYER_BackSpeed:
                self.speed[1] += self.accelerate[2]
        else:
            self.speed[1] = 0
            self.rect.bottom = SCREEN.getH()
    def moveLeft(self):
        self.direction[0] = -1
        self.move_flag[0] = True
        if self.rect.left > 0 :
            if self.speed[0] > -self.PLAYER_xSpeed :
                self.speed[0] += -self.accelerate[0]
        else:
            self.speed[0] = 0
            self.rect.left = 0  
    def moveRight(self):
        self.direction[0] = 1
        self.move_flag[0] = True
        if self.rect.right < SCREEN.getW() :
            if self.speed[0] < self.PLAYER_xSpeed:
                self.speed[0] += self.accelerate[0]
        else:
            self.speed[0] = 0
            self.rect.right = SCREEN.getW()
    def brake(self):
        if self.speed == [0, 0]:
            return
        if not self.move_flag[0]:
            if self.speed[0] > 0 :
                self.speed[0] += -self.accelerate[0]
                if self.speed[0] <= 0 :
                    self.speed[0] = 0
                    self.direction[0] = 0
            elif self.speed[0] < 0:
                self.speed[0] += self.accelerate[0]
                if self.speed[0] >= 0 :
                    self.speed[0] = 0
                    self.direction[0] = 0
        if not self.move_flag[1]:
            if self.speed[1] > 0:
                self.direction[1] = 0
                self.speed[1] += -self.accelerate[1]
                if self.speed[1] <= 0 :
                    self.speed[1] = 0
                    self.direction[1] = 0
            elif self.speed[1] < 0:
                self.direction[1] = 1
                self.speed[1] += self.accelerate[2]
                if self.speed[1] >= 0 :
                    self.speed[1] = 0
                    self.direction[1] = 0

    def hit(self):
        if not self.invicible_flag:
            self.active = False
            self.image_switch = 0
            self.mainImage = self.crashImage
            SOUNDS["Player_Explo"].play()
            return True
        else:
            return False

    def shoot(self):
        b = []
        position1 = self.rect.center[0]-10,self.rect.center[1]
        position2 = self.rect.center[0]+10,self.rect.center[1]
        if self.bullet_type == PLAYER_BULLET.Bullet1:
            if self.lever == 1:
                b1 = Player_Bullet1(position1, -1)
                b2 = Player_Bullet1(position2, 1)
                b = [b1,b2]
            elif self.lever == 2:
                b1 = Player_Bullet1(position1, -1)
                b2 = Player_Bullet1(position2, 1)
                b3 = Player_Bullet1(position1, -2)
                b4 = Player_Bullet1(position2, 2)
                b = [b1,b2,b3,b4]
            elif self.lever == 3:
                b1 = Player_Bullet1(position1, -1)
                b2 = Player_Bullet1(position2, 1)
                b3 = Player_Bullet1(position1, -2)
                b4 = Player_Bullet1(position2, 2)
                b5 = Player_Bullet1(position1, -3)
                b6 = Player_Bullet1(position2, 3)
                b = [b1,b2,b3,b4,b5,b6]
            MyPlane.PLAYER_Bullets.add(b)

    def Invincible(self,ticks, rate=60):
        if self.invicible_flag:
            if self.current_time < ticks + rate :
                self.reset_invincible = (self.reset_invincible + 1) % 50
                if self.reset_invincible == 49:
                    self.invicible_flag = False

    def reset(self, pos=None):
        self.active = True 
        self.image_switch = 0       
        self.invicible_flag = True
        self.mainImage = self.normalImage
        self.bullet_type = PLAYER_BULLET.Bullet1
        self.lever = 1
        if not pos:
            pos = int(SCREEN.getW() // 2), \
                    int(SCREEN.getH() - self.rect.height // 2 - 60 )
        self.rect.center = pos
        self.direction = [0, 0]

    def setBullet(self,bul_type):
        if self.bullet_type != bul_type:
            self.lever = 2
            self.bullet_type = bul_type
        elif self.lever < 3:
                self.lever += 1

class PLAYER_BULLET(Enum):
    Bullet1 = 0
    Bullet2 = 1

class Player_Bullet1(pygame.sprite.Sprite):
    PLAYER_BulletSPEED = 17
    def __init__(self, pos, lever):
        pygame.sprite.Sprite.__init__(self)
        self.damage = 150
        self.image = BULLET_IMAGE["Viking_Bullet"]
        self.MaxSpeed = self.PLAYER_BulletSPEED
        if lever == 1:
            self.speed = [0.5,-17]
        if lever == -1:
            self.speed = [-0.5,-17]
        elif lever == 2:
            self.speed = [5.8,-16]        
            self.image = pygame.transform.rotate(self.image, -20)
        elif lever == -2:
            self.speed = [-5.8,-16]
            self.image = pygame.transform.rotate(self.image, 20)
        elif lever == 3:
            self.speed = [6,-15.8]
            self.image = pygame.transform.rotate(self.image, -21)
        elif lever == -3:
            self.speed = [-6,-15.8]
            self.image = pygame.transform.rotate(self.image, 21)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        if self.whenkill():
            self.kill()
        else :
            self.move()
    def move(self):
        self.rect.move_ip(self.speed[0], self.speed[1])

    def whenkill(self):
        if self.rect.top > SCREEN.getH() \
            or self.rect.bottom < 50 or self.rect.right < 0 \
            or self.rect.left > SCREEN.getW():
            return True
        return False
        

class Nuclear_Bomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = BULLET_IMAGE["Viking_Bullet"]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.accelerate = 0.2
        self.speed = -2
        self.explode_flag = False
        self.active = True

    def update(self):
        if self.active:
            if self.rect.bottom > SCREEN.getH() // 3:
                self.move()
            else:
                self.explode_flag = True
        else :
            self.kill()

    def move(self):
        self.rect.top -= self.speed
        self.speed += self.accelerate


def main():
    pygame.init()
    clock = pygame.time.Clock()   
    screen = pygame.display.set_mode((1000,1000))
    # 事件
    PLAYER_SHOOT = USEREVENT
    NUCLEAR_LAUNCH = USEREVENT+1

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
    player.setBullet(PLAYER_BULLET.Bullet1)
    player.setBullet(PLAYER_BULLET.Bullet1)
    p_g = pygame.sprite.Group()
    p_g.add(player)
    b_g = MyPlane.PLAYER_Bullets
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
                    pygame.event.post(pygame.event.Event(PLAYER_SHOOT, {}))
                    pygame.time.set_timer(PLAYER_SHOOT, 200)  
                # Q键投掷核�?
                if event.key == K_q:
                    if nuclear_bomb > 0 and NB.active == False:    
                        nuclear_bomb -= 1          
                        bomb_text.change_text("Bomb: " + str(nuclear_bomb))
                        SOUNDS["NuclearLaunch_Detected"].stop() 
                        SOUNDS["NuclearLaunch_Detected"].play()      
                        pygame.event.post(pygame.event.Event(NUCLEAR_LAUNCH, {}))
                    else:
                        SOUNDS["Error"].stop()
                        SOUNDS["Error"].play()

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    pygame.time.set_timer(PLAYER_SHOOT, 0) 
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
                    pygame.event.post(pygame.event.Event(PLAYER_SHOOT, {}))
                    pygame.time.set_timer(PLAYER_SHOOT, 200)

            elif event.type == MOUSEBUTTONUP:  
                if event.button == 1:
                    pygame.time.set_timer(PLAYER_SHOOT, 0) 

            elif event.type == PLAYER_SHOOT:
                SOUNDS["Player_Shoot"].stop()
                SOUNDS["Player_Shoot"].play()
                player.shoot()

            elif event.type == NUCLEAR_LAUNCH:
                NB.active = True
                NB.rect.center = player.rect.midtop

        # 检测用户键盘操�?
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveBack()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

        screen.fill(BLACK)
        p_g.update(ticks)
        p_g.draw(screen)
        b_g.update()
        b_g.draw(screen)
        # 显示
        pygame.display.flip()
    pygame.quit() 
    sys.exit()

if __name__ == "__main__":
    import pygame, sys
    from pygame.locals import *    
    main()