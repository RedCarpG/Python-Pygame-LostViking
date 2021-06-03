import pygame
import os
from pygame.compat import geterror
from pygame.locals import RLEACCEL

main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, '../../data/image')


def _load_image(name, color_key=None, alpha=None, scale=None):
    fullname = os.path.join(image_dir, name)
    try:
        image = pygame.image.load(fullname)
        print('-- Success: Image load {}'.format(name))
    except pygame.error:
        print('!!! Error: Can not find image {}'.format(fullname))
        raise SystemExit(str(geterror()))
    image = image.convert()
    if scale is not None:
        image = pygame.transform.smoothscale(image,
                                             (int(image.get_height() * scale[0]), int(image.get_width() * scale[1])))
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)
    if alpha is not None:
        image.set_alpha(alpha, pygame.RLEACCEL)
    return image


def _load_image_alpha(name, color_key=None, alpha=None, scale=None):
    fullname = os.path.join(image_dir, name)
    try:
        image = pygame.image.load(fullname)
        print('-- Success: Alpha image load {}'.format(name))
    except pygame.error:
        print('!!! Error: Can not find image {}'.format(fullname))
        raise SystemExit(str(geterror()))
    image = image.convert_alpha()
    if scale is not None:
        image = pygame.transform.smoothscale(image,
                                             (int(image.get_height() * scale[0]), int(image.get_width() * scale[1])))
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, RLEACCEL)
    if alpha is not None:
        image.set_alpha(alpha, pygame.RLEACCEL)
    return image
