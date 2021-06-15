
import pygame

Player1_G = pygame.sprite.GroupSingle(None)
Player2_G = pygame.sprite.GroupSingle(None)

Player_NucBomb_G = pygame.sprite.GroupSingle(None)
NucBomb_Explosion_G = pygame.sprite.GroupSingle(None)

Enemy_G = pygame.sprite.Group()

BOSS_G = pygame.sprite.GroupSingle(None)

Bullet_G = pygame.sprite.Group()
Player_Bullet_G = pygame.sprite.Group()
Enemy_Bullet_G = pygame.sprite.Group()

Enemy_Destroyed_G = pygame.sprite.Group()

Shield_G = pygame.sprite.LayeredDirty()
