""" Contains functions to load image to a pygame.surface.Surface object.
Some methods to modify a Surface:
    Surface.set_colorkey() -> None
    Surface.set_alpha() -> None
    pygame.transform.smoothscale(Surface) -> Surface
"""
import os
from pygame.compat import geterror
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, '../..', 'data', 'image')


def load_image(name: str,
               transparency=True,
               color_key=None,
               alpha=None,
               scale=None) -> pygame.surface.Surface:
    """ Load an image file to a Surface object.
    :param transparency: If a file has transparent pixels
    :param name: File name, from a default directory "image_dir"
    :param color_key: A color value which make certain color transparent if not None
    :param alpha: A value from 0-255 which controls full image alpha(transparency) if not None
    :param scale: Transform the image with scale if not None
    :return pygame.surface.Surface object
    """
    fullname = os.path.join(image_dir, name)
    try:
        # Try load from file
        image = pygame.image.load(fullname)
        print('-- Success: Image load {}'.format(name))
    except pygame.error:
        # If error occurs
        print('!!! Error: Can not find image {}'.format(fullname))
        raise SystemExit(str(geterror()))
    # Convert the Surface for better performance(convert_alpha() if with transparent pixels)
    image = image.convert_alpha() if transparency else image.convert()
    # Transform with scale if needed
    if scale is not None:
        image = pygame.transform.smoothscale(image,
                                             (int(image.get_height() * scale[0]),
                                              int(image.get_width() * scale[1])))
    # Set transparent color_key if needed
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)
    # Set full image alpha value if needed
    if alpha is not None:
        from pygame.locals import RLEACCEL
        image.set_alpha(alpha, pygame.RLEACCEL)
    return image
