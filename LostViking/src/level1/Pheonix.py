



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