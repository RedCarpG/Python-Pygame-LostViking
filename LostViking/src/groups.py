from pygame.sprite import GroupSingle, Group, LayeredDirty

Player1_G = GroupSingle(None)
Player2_G = GroupSingle(None)

Player_NucBomb_G = GroupSingle(None)
Explosion_G = GroupSingle(None)

Enemy_G = Group()

BOSS_G = GroupSingle(None)

Bullet_G = Group()
Player_Bullet_G = Group()
Enemy_Bullet_G = Group()

Plane_G = Group()
Destroyed_Plane_G = Group()

Shield_G = LayeredDirty()


Supply_G = Group()
