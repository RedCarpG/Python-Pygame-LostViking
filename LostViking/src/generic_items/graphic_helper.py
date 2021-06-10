""" This file contains Helpers
which works with pygame.sprite.Sprite

They handle with :
    -> image loading with init_image()
    -> loop through a image list with _switch_image() for drawing.
            which should be called in customized update() from Sprite
"""
from abc import abstractmethod, ABC


class BasicImageHelper(object):
    """ Helper which deal with image loading and drawing by it's own
    Interface class for Basic Image Helper,
    Implemented by SingleImageHelper and LoopImageHelper

    Attributes:
        cls._IMAGE: A Surface or a list of Surface entity
            which are loaded from images
        cls._INIT_FLAG_IMAGE: A flag which will be set True
            when init_image() is called
     """
    # A Dictionary of lists of images
    _IMAGE = None
    # Flag is set to True once the _IMAGE is initialized
    _INIT_FLAG_IMAGE = False

    def __init__(self):
        if not self._INIT_FLAG_IMAGE:
            print("!!! WARNING: {} image value not initialized", self.__name__)
            self.init_image()

    @classmethod
    @abstractmethod
    def init_image(cls):
        """ It should load image(s) to cls._IMAGE
        and set cls._INIT_FLAG_IMAGE to true when it's done """
        pass


class SingleImageHelper(BasicImageHelper, ABC):
    """ A Helper for object which only needs a single image
    It's an abstract Class which implements from BasicImageHelper
    """
    def __init__(self):
        BasicImageHelper.__init__(self)
        self.image = self._IMAGE


class LoopImageHelper(BasicImageHelper, ABC):
    """ A Helper for drawing Entities by looping in its image list
    It's an abstract Class which implements from BasicImageHelper
    """
    # A Dictionary of lists of images
    _IMAGE = {"Base": None}

    def __init__(self):
        BasicImageHelper.__init__(self)
        if self._IMAGE["Base"] is None:
            raise Exception("ERROR: _IMAGE[\"Base\"] value is not set! {}".format(self))
        self._main_image_type = self._IMAGE["Base"]
        self._image_switch = 0
        self._image_switch_interval = 0
        self.image = self._main_image_type[self._image_switch]

    # Switch image
    def _switch_image(self, switch_rate=5):
        """ Switch image function should be called """
        if self._image_switch_interval >= switch_rate:
            self._image_switch = (self._image_switch + 1) % len(self._main_image_type)
            self.image = self._main_image_type[self._image_switch]
            self._image_switch_interval = 0
        else:
            self._image_switch_interval += 1

    def _set_image_type(self, image_type):
        self._main_image_type = self._IMAGE[image_type]
