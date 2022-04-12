import pygame
from src.game.Game import Game


def main():

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption("Lost Viking")

    game = Game()
    game.run()

    pygame.font.quit()
    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()

    import sys
    sys.exit()
