from LostViking.src.player import *
from LostViking.src.ingame_items import *
from LostViking.src.ingame_items.SupplyLife import *
from LostViking.src.groups import *

from LostViking.src.constants import *
from pygame.locals import *
import pygame


def test_player():
    # Init Environment
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Init Player
    init_player()
    init_supply()
    player1, _ = create_player()
    set_player_bullet_type(player1, 1)
    player_upgrade(player1)
    add_nuc_bomb()

    s = SupplyLife(position=(500, 500))

    def test_key_event():
        if event.key == K_x:
            player1.hit(100)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # --------------- Key Down Events ---------------
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                test_key_event()
            detect_player_event(event, player1=player1)

        detect_key_pressed(player1)

        screen.fill(BLACK)
        Supply_G.update()
        Player_NucBomb_G.update()
        Player_Bullet_G.update()
        Player1_G.update()
        Player_NucBomb_G.update()
        Supply_G.draw(screen)
        Player_Bullet_G.draw(screen)
        Player_NucBomb_G.draw(screen)
        Player1_G.draw(screen)
        Player_NucBomb_G.draw(screen)
        # Display
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    test_player()

    pygame.quit()
    import sys

    sys.exit()
