
from LostViking.src.groups import *

from pygame.locals import *
from LostViking.src.generic_loader.color import *
from LostViking.src.level1 import *
from LostViking.src.constants import SCREEN
import time


def test_enemy():
    # Init Environment
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN.get_s())

    level1_init()

    pygame.time.set_timer(EVENT_CREATE_SCOUT, 1000)
    pygame.time.set_timer(EVENT_CREATE_PHOENIX, 15000)

    from LostViking.src.player import create_player, init_player
    init_player()
    create_player(1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # --------------- Key Down Events ---------------
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            level1_events_handler(event=event)

        screen.fill(BLACK)
        Player1_G.update()
        Player1_G.draw(screen)
        Bullet_G.update()
        Bullet_G.draw(screen)
        Enemy_G.update()
        Enemy_G.draw(screen)

        # Display
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    test_enemy()

    pygame.quit()
    import sys

    sys.exit()
