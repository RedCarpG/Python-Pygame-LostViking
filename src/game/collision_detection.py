from pygame.sprite import spritecollideany, collide_rect_ratio, groupcollide, collide_rect
from .groups import *


def _collide_test(a, b):
    if collide_rect(a, b):
        if collide_rect_ratio(0.5)(a, b):
            return True
    return False


def collide_detection(player):
    """
    supply_get = pygame.sprite.spritecollideany(self.player, self.group_supply)
    if supply_get != None:
        if pygame.sprite.collide_circle_ratio(0.65)(self.player, supply_get):
            supply_get.catched(self.player)
            G.SCORE += supply_get.score
            if supply_get.type == SupplyType.Bomb:
                self.bomb_text.change_text("Bomb: " + str(G.BOMB))
            elif supply_get.type == SupplyType.Life:
                self.life_text.change_text("Life: " + str(G.LIFE))
    """
    if player.is_active and not player.is_invincible:
        bullet_hit = spritecollideany(player, Enemy_Bullet_G)
        if bullet_hit is not None:
            if collide_rect_ratio(0.65)(player, bullet_hit):
                if player.hit(100):
                    bullet_hit.hit()
                    # G.LIFE -= 1
        enemy_hit = spritecollideany(player, Enemy_G)
        if enemy_hit is not None:
            if collide_rect_ratio(0.65)(player, enemy_hit):
                if enemy_hit.is_active:
                    if player.hit(100):
                        if enemy_hit not in BOSS_G:
                            enemy_hit.hit(1000)
                        # G.LIFE -= 1

    enemy_hit = groupcollide(Enemy_G, G_Player_Bullet,
                             False, True, _collide_test)
    if len(enemy_hit) > 0:
        for enemy, bullets in enemy_hit.items():
            for each_bullets in bullets:
                enemy.hit(each_bullets.damage)
                each_bullets.hit()
    """
    if len(self.bomb) > 0:
        if self.bomb.sprite.is_active and self.bomb.sprite.explode_flag:
            self.bomb.sprite.is_active = False
            for each in self.enemies:
                if each.rect.bottom > 0 and each.is_active:
                    each.hit(800)
                    if not each.is_active:
                        G.SCORE += each.score
                        each.destroy()
                        each.kill()
                        self.enemies_die.add(each)
            self.enemy_bullets.empty()

    self.life_text.change_text("Life: " + str(G.LIFE))
    self.score_text.change_text("Score: " + str(G.SCORE))
    """
