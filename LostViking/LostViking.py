import traceback
import pygame
from pygame.sprite import spritecollideany, collide_rect_ratio, groupcollide
from pygame.locals import *
import sys
from src.constants import *
from src.generic_loader.sound_loader import load_music, load_sound, play_sound
from src.generic_loader.image_loader import load_image
from src.generic_loader.font_loader import load_font, PGFont
from src.player import *
from src.groups import *

if not pygame.font:
    print("Warning, fonts disabled!")
if not pygame.mixer:
    print("Warning, sounds disabled!")

# TODO collide test separate file
def collide_test(a, b):
    if pygame.sprite.collide_rect(a, b):
        if pygame.sprite.collide_rect_ratio(0.5)(a, b):
            return True
    return False

# TODO enter UI
""" 
def enter(Screen, clock):
    # Load music
    load_music(['bgm.ogg', 'bgm2.ogg'], MAIN_VOLUME - 0.7)
    # Play music
    pygame.mixer.music.play(0)

    # Load bg image
    bg_surface = load_image("Space.png")

    # enter font
    begin_font = load_font("arialbd.ttf", 50)
    title_font = load_font("arialbd.ttf", 120)
    begin_text = PGFont(Screen, begin_font, "Press Space To Begin", (0, 0), color=WHITE)
    title_text = PGFont(Screen, title_font, "LOST VIKING", (0, 0), color=WHITE)
    title_text.move_center((Screen.get_width() // 2, Screen.get_height() // 2))
    begin_text.move_center((Screen.get_width() // 2, 3 * Screen.get_height() // 5))
    ui1 = load_sound("ui1.wav", MAIN_VOLUME - 0.2)

    # enter loop
    delay = 100
    while True:
        # 绘制背景，文本
        Screen.fill(BLACK)
        title_text.blit()
        if delay % 5:
            begin_text.blit()
        pygame.display.flip()
        # 全部事件
        for event in pygame.event.get():
            # 退出事件
            if event.type == QUIT:
                pygame.font.quit()
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()
            # 按键事件
            elif event.type == KEYDOWN:
                # 按ESCAPE退出
                if event.key == K_ESCAPE:
                    pygame.font.quit()
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE or event.key == K_RETURN:
                    ui1.play()
                    return
        delay = (delay - 1) % 100
        # Frame rate
        clock.tick(10)
"""

class LostViking(object):

    #  ---------------------- Init ---------------------- #
    def __init__(self):
        # Init Pygame
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption("LOST VIKING")

        # Init screen surface
        self.screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
        # Init clock
        self.clock = pygame.time.Clock()

        # Init Music
        music = ['bgm2.ogg', 'bgm.ogg']
        load_music(music, MAIN_VOLUME)
        pygame.mixer.music.play(1)

        # Load BG
        self.background_image = load_image("Space.png")

        # TODO Text
        """
        # · Text Groups
        fonts = {"score_font": load_font("arialbd.ttf", 30),
                 "life_font": load_font("arialbd.ttf", 30)}
        self.Text_G = {
            'score_text': PGFont(self.screen, fonts["score_font"],
                                 ("Score: " + str(G.SCORE)), (0, 30), color=WHITE),
            'life_text': PGFont(self.screen, fonts["score_font"],
                                ("Life: " + str(G.LIFE)), (0, 60), color=WHITE),
            'bomb_text': PGFont(self.screen, fonts["score_font"],
                                ("Bomb: " + str(G.BOMB)), (0, 90), color=WHITE)
        }
        """
        # TODO Supply Event
        # pygame.time.set_timer(self.CREATE_SUPPLY, 10000)

        # create player
        init_player()
        self.player1, _ = create_player(player_num=1)

        self.level = None

        self.running = True

    # TODO begin animation
    """
    def begin_animation(self):

        # 生成背景
        bg1_image = load_image("BackGround.png")
        bg2_image = load_image("BackGround2.png")
        bg1_rect = bg1_image.get_rect()
        bg2_rect = bg2_image.get_rect()
        bg1_rect.bottom = SCREEN.get_h()
        bg2_rect.bottom = SCREEN.get_h()

        accelerate = 0
        delay = 100
        lift_flag1 = 0
        lift_flag2 = 0
        init_speed = 0
        end_flag = -1
        play_sound("Liftoff2")

        while True:
            self.screen.blit(self.background_image, (0, 0))

            if bg2_image is not None:
                self.screen.blit(bg2_image, bg2_rect)
            if bg1_image is not None:
                self.screen.blit(bg1_image, bg1_rect)
            # 绘制我方飞机
            self.player.blit()

            if init_speed < BG_SPEED:
                accelerate += 0.005
                init_speed += accelerate

            if bg2_rect.top >= self.screen.get_height():
                if end_flag == -1:
                    end_flag = 50
                self.player.direction[1] = 0
            elif bg1_rect.top >= SCREEN.get_height() // 2:
                if lift_flag2 == 0:
                    lift_flag2 = 1
                    SOUNDS["Liftoff2"].play()

            if self.player.rect.bottom > 2 * SCREEN.get_height() // 3:
                if init_speed > 2:
                    self.player.direction[1] = -1
                    if lift_flag1 == 0:
                        lift_flag1 = 1
                        SOUNDS["Liftoff1"].play()
                        # BG_rect1.top += init_speed
                self.player.rect.top -= init_speed
            else:
                bg1_rect.top += init_speed
                bg2_rect.top += 1 * init_speed // 6
            if end_flag > 0:
                end_flag -= 1
            elif end_flag == 0:
                begin = False
            delay = (delay - 1) % 100
            # Display
            pygame.display.flip()
            # Frame rate
            self.clock.tick(60)
    """
    def load_level(self, level):
        if self.level:
            self.level.end_level()
        self.level = level
        self.level.level_event_config()
        level.init_level()

    def play(self):
        import src.level1 as level1
        self.load_level(level=level1)

        # Main loop
        while self.running:
            self.clock.tick(60)

            self._events_handler()
            self._collide_detection()
            self._blit_all()
            self._update_all()

    def _events_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            detect_player_event(event, self.player1)
            self.level.level_events_handler(event)
        detect_key_pressed(self.player1)

    def _collide_detection(self):
        """
        supply_get = pygame.sprite.spritecollideany(self.player, self.group_supply)
        if supply_get != None:
            if pygame.sprite.collide_circle_ratio(0.65)(self.player, supply_get):
                supply_get.catched(self.player)
                G.SCORE += supply_get.score
                if supply_get.type == SUPPLY_TYPE.Bomb:
                    self.bomb_text.change_text("Bomb: " + str(G.BOMB))
                elif supply_get.type == SUPPLY_TYPE.Life:
                    self.life_text.change_text("Life: " + str(G.LIFE))
        """
        if self.player1.is_active and not self.player1.is_invincible:
            bullet_hit = spritecollideany(self.player1, Enemy_Bullet_G)
            if bullet_hit is not None:
                if collide_rect_ratio(0.65)(self.player1, bullet_hit):
                    if self.player1.hit(100):
                        bullet_hit.hit()
                        # G.LIFE -= 1
            enemy_hit = spritecollideany(self.player1, Enemy_G)
            if enemy_hit is not None:
                if collide_rect_ratio(0.65)(self.player1, enemy_hit):
                    if enemy_hit.is_active:
                        if self.player1.hit(100):
                            if enemy_hit not in BOSS_G:
                                enemy_hit.hit(1000)
                            # G.LIFE -= 1

        enemy_hit = groupcollide(Enemy_G, Player_Bullet_G, False, True, collide_test)
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

    @classmethod
    def _update_all(cls, *args, **kwargs):
        # Destroyed plane
        Destroyed_Plane_G.update()
        # Enemies
        BOSS_G.update()
        Enemy_G.update()
        # Player
        Player1_G.update()
        # Bullets
        Enemy_Bullet_G.update()
        Player_Bullet_G.update()
        # Other entities
        Shield_G.update()
        Player_NucBomb_G.update()
        # Flip all
        pygame.display.flip()

    def _blit_all(self):
        # BG
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (0, 0))
        if BOSS_G.sprite:
            pygame.draw.rect(self.screen, (100, 200, 100, 180), Rect(0, 0, SCREEN_WIDTH, 25), 3)
            pygame.draw.rect(self.screen, (100, 200, 100, 180),
                             Rect(0, 0, SCREEN_WIDTH * BOSS_G.sprite.get_health() / BOSS_G.sprite.MAX_HEALTH, 25))
        """
        # Fonts
        self.score_text.blit()
        self.life_text.blit()
        self.bomb_text.blit()
        """
        # Groups
        Destroyed_Plane_G.draw(self.screen)
        Enemy_G.draw(self.screen)
        Shield_G.draw(self.screen)
        BOSS_G.draw(self.screen)
        Bullet_G.draw(self.screen)
        Player_NucBomb_G.draw(self.screen)
        Player1_G.draw(self.screen)

    def __del__(self):
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()


if __name__ == "__main__":
    try:
        game = LostViking()
        game.play()
    except SystemExit:
        pass
    except (ValueError, Exception):
        print(traceback.format_exc())
        traceback.print_exc()
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()
        input()
        sys.exit()
