from abc import abstractmethod


class SingleImageHelper(object):
    """ Abstract Class, which manage with image """
    # A Dictionary of lists of images
    _IMAGE = None
    # Flag is set to True once the _IMAGE is initialized
    _INIT_FLAG = False

    def __init__(self):
        if not self._INIT_FLAG:
            self.init_image()
        self.image = self._IMAGE

    @classmethod
    @abstractmethod
    def init_image(cls):
        pass


class LoopImageHelper(object):
    """
    A Helper for drawing Entities by looping in its image list
    """
    # A Dictionary of lists of images
    _IMAGE = {"Base": [None]}
    # Flag is set to True once the _IMAGE is initialized
    _INIT_FLAG = False

    def __init__(self):
        if not self._INIT_FLAG:
            self.init_image()
        self._image_switch = 0
        self._image_switch_count = 0
        self._main_image_type = self._IMAGE["Base"]
        self.image = self._main_image_type[self._image_switch]

    # Switch image
    def _switch_image(self, switch_rate=5):
        """ Switch image function should be called """
        if self._image_switch_count >= switch_rate:
            self._image_switch = (self._image_switch + 1) % len(self._main_image_type)
            self.image = self._main_image_type[self._image_switch]
            self._image_switch_count = 0
        else:
            self._image_switch_count += 1

    def _set_image_type(self, image_type):
        self._main_image_type = self._IMAGE[image_type]

    @classmethod
    @abstractmethod
    def init_image(cls):
        pass
