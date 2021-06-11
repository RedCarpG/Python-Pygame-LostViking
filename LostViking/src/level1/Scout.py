

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