import os
import sys
import pygame
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

_font_dir = os.path.join(os.path.split(
    os.path.abspath(__file__))[0], '../../asset/font')


class NoneFont:
    @classmethod
    def render(cls):
        logging.warning("-- No font")
        return pygame.Surface((0, 0))


class _FontBuffer(object):

    BUFFER = {}

    def __getitem__(self, key):
        if key not in self.BUFFER:
            logging.warning(
                f"<WARNING> Font [{key}] not loaded")
            return NoneFont()
        return self.BUFFER[key]

    def __setitem__(self, key, item):
        self.BUFFER[key] = item

    def __delitem__(self, key):
        del self.BUFFER[key]


_FONT = _FontBuffer()


def load_font(filename, size, label):
    """ Load from a font file ".ttf" to a Font object
    :param filename [Name of the file, from a default directory "_font_dir"]
    :param size
    :return pygame.font.Font object
    """

    if not pygame.font or not pygame.font.get_init():
        logging.warning("<WARNING> pygame.font not inited")
        return NoneFont()
    fullname = os.path.join(_font_dir, filename)
    try:
        font = pygame.font.Font(fullname, size)
        logging.info(f"<SUCCESS> Font [{filename}] loaded !")
    except pygame.error:
        logging.error(f"<ERROR> Font [{filename}] not found")
        raise SystemExit(str(pygame.get_error()))
    _FONT[label] = font
    return font


def get_font(label):
    return _FONT[label]


def del_font(label):
    del _FONT[label]
