from pygame.sprite import GroupSingle, Group, LayeredDirty

G_Player1 = GroupSingle(None)
G_Player2 = GroupSingle(None)

G_Bomb = GroupSingle(None)

G_Enemy = Group()

G_BOSS = GroupSingle(None)

G_Bullet = Group()
G_Player_Bullet = Group()
G_Enemy_Bullet = Group()

G_Plane = Group()
G_Destroyed_Plane = Group()

G_Shield = LayeredDirty()


G_Supply = Group()

G_Effect = Group()
