import os
import sys
import pygame
from ..constants import WHITE
from pygame.compat import geterror

_font_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '../../data/font')


def load_font(filename, size):
    """ Load from a font file ".ttf" to a Font object
    :param filename [Name of the file, from a default directory "_font_dir"]
    :param size
    :return pygame.font.Font object
    """
    class NoneFont:
        @classmethod
        def render(cls):
            print("-- No font")
            return pygame.Surface((0, 0))

    if not pygame.font or not pygame.font.get_init():
        print("<WARNING> pygame.font not inited", file=sys.stderr)
        return NoneFont()
    fullname = os.path.join(_font_dir, filename)
    try:
        font = pygame.font.Font(fullname, size)
        print("<SUCCESS> Font [{}] loaded !".format(filename))
    except pygame.error:
        print("<ERROR> Font [{}] not found".format(filename), file=sys.stderr)
        raise SystemExit(str(geterror()))
    return font


class FontEntity:
    def __init__(self, screen, font, text='', position=(0, 0), antialias=True, color=WHITE, background=None):
        self.font = font
        self.antialias = antialias
        self.color = color
        self.background = background
        self.text = text
        self.screen = screen
        self.render = self.font.render(self.text, self.antialias, self.color, self.background)
        self.rect = self.render.get_rect()
        self.rect.move_ip(position)

    def blit(self):
        self.screen.blit(self.render, (self.rect[0], self.rect[1]))

    def move_center(self, center_position):
        self.rect.center = center_position

    def move(self, position):
        self.rect.move_ip(position)

    def change_text(self, text):
        self.text = text
        self.rendering()

    def change_font(self, font):
        self.font = font
        self.rendering()

    def change_color(self, color):
        self.color = color
        self.rendering()

    def rendering(self):
        self.render = self.font.render(self.text, self.antialias, self.color, self.background)
