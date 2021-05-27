import pygame, os
from pygame.compat import geterror
from GLOBAL import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, 'image')

#functions to create our resources
def load_image(name, colorkey=None, alpha=None, scale=None):
    fullname = os.path.join(image_dir, name)
    try:
        image = pygame.image.load(fullname) 
        print ('--图片%s加载成功！' % name)
    except pygame.error:
        print ('！！--找不到图片:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if scale is not None:
        image = pygame.transform.smoothscale(image, (int(image.get_height()*scale[0]), int(image.get_width()*scale[1])))
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    if alpha is not None:
        image.set_alpha(alpha, pygame.RLEACCEL)
    return image

def load_image_alpha(name, colorkey=None, alpha=None, scale=None):
    fullname = os.path.join(image_dir, name)
    try:
        image = pygame.image.load(fullname) 
        print ('--图片%s加载成功！' % name)
    except pygame.error:
        print ('！！--找不到图片:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert_alpha()
    if scale is not None:
        image = pygame.transform.smoothscale(image, (int(image.get_height()*scale[0]), int(image.get_width()*scale[1])))
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    if alpha is not None:
        image.set_alpha(alpha, pygame.RLEACCEL)
    return image