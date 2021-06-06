from LostViking.src.player import *
from LostViking.src.groups import *

if __name__ == "__main__":
    import sys
    from LostViking.src.constants import *
    from pygame.locals import *
    from LostViking.src.generic_loader.color import *

    # Init Environment
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN.WIDTH, SCREEN.HEIGHT))

    # Init Player
    init_player_image()
    init_player_sound()
    player1 = create_player()
    set_player_bullet_type(player1, 1)
    player_upgrade(player1)
    player_upgrade(player1)
    add_nuc_bomb()
    add_nuc_bomb()
    add_nuc_bomb()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # --------------- Key Down Events ---------------
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            detect_player_event(event, player1=player1)

        # If Key Pressed
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player1.trigger_move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player1.trigger_move_back()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player1.trigger_move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player1.trigger_move_right()

        screen.fill(BLACK)
        Player_NucBomb_G.update()
        Player_Bullet_G.update()
        Player1_G.update()
        NucBomb_Explosion_G.update()
        Player_Bullet_G.draw(screen)
        Player_NucBomb_G.draw(screen)
        Player1_G.draw(screen)
        NucBomb_Explosion_G.draw(screen)
        # Display
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()
