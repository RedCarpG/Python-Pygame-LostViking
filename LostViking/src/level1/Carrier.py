
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
