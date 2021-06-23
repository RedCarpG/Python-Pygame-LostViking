


class Supply_Bullet1(Supply):
    def __init__(self, position=[-1, -1]):
        Supply.__init__(self, position)
        self.type = SupplyType.Bullet1

    def setImage(self):
        self.image = SUPPLY_IMAGE["Bullet"]

    def catched(self, player):
        player.set_bullet_type(PlayerBulletType.Bullet1)
        self.kill()


class Supply_Bomb(Supply):
    def __init__(self, position=[-1, -1]):
        Supply.__init__(self, position)
        self.type = SupplyType.Bomb

    def setImage(self):
        self.image = SUPPLY_IMAGE["Bomb"]

    def catched(self, player):
        if G.BOMB < 5:
            G.BOMB += 1
        self.kill()

