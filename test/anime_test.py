
import pygame
from pygame.locals import *
from pygame.display import set_caption
from pygame.sprite import Group

from src.helper.image import load_image
from src.setting import *
from src.util import *
from src.game.animation.AnimeSprite import AnimeSprite


def test_anime():
    # Init Environment
    pygame.init()
    set_caption("Animation Test")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    images = {
        "BASE": load_image("PlayerPlane/VikingBody.png", transparency=True),
        "IDLE": load_image("PlayerPlane/VikingIdle.png", transparency=True)
    }

    anime_sprites = Group()
    sprite = AnimeSprite(images)
    anime_sprites.add(sprite)
    sprite.rect.move_ip(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # --------------- Key Down Events ---------------
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.fill(BLACK)
        sprite.update()
        anime_sprites.draw(screen)
        # Display
        pygame.display.flip()

        clock.tick(60)
