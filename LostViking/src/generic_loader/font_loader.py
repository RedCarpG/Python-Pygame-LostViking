import pygame
import os
from .color import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
font_dir = os.path.join(main_dir, '../../data/font')


def load_font(name, size):
    """ Load from a font file ".ttf" to a Font object
    :param name [Name of the file, from a default directory "font_dir"]
    :param size
    :return pygame.font.Font object"""
    class NoneFont:
        def render(self):
            print("--无字体")
            return pygame.Surface((0, 0))

    if not pygame.font or not pygame.font.get_init():
        print("--Font未启动,%s加载失败！" % name)
        return NoneFont()
    fullname = os.path.join(font_dir, name)
    try:
        font = pygame.font.Font(fullname, size)
        print('--字体%s加载成功！' % name)
    except pygame.error:
        print('！！--找不到字体: %s' % fullname)
        raise SystemExit(str(geterror()))
    return font


class PGFont:
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

    def move_center(self, center_positon):
        self.rect.center = center_positon

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
