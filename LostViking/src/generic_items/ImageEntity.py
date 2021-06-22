from abc import abstractmethod

from pygame.sprite import Sprite


class SingleImageEntity(Sprite):
    IMAGE = None
    _IS_SET_IMAGE = False

    def __init__(self):
        # Check Initialization
        if not self._IS_SET_IMAGE:
            raise Exception("!!!ERROR: Entity IMAGE is not set! {}".format(self.__class__))

        # Init Sprite
        Sprite.__init__(self)

        # Set Image properties
        self.image = self.IMAGE
        # Set Rect
        self.rect = self.image.get_rect()

    @classmethod
    @abstractmethod
    def _init_image(cls):
        cls.IMAGE = None
        cls._IS_SET_IMAGE = False


class LoopImageEntity(Sprite):
    IMAGE = {"BASE": None,
             "IDLE": None,
             "EXPLODE": None}
    _IS_SET_IMAGE = False

    def __init__(self):
        # Check Initialization
        if not self._IS_SET_IMAGE:
            raise Exception("!!!ERROR: Entity IMAGE is not set! {}".format(self.__class__))

        # Init Sprite
        Sprite.__init__(self)

        # Set Image properties
        self._main_image_type = self.IMAGE["BASE"]
        self._image_switch = 0
        self._image_switch_interval = 0
        self.image = self._main_image_type[self._image_switch]
        self._set_image_type("IDLE")
        # Set Rect
        self.rect = self.image.get_rect()

    # --------------- Image blit helper --------------- #
    def _switch_image(self, switch_rate=5) -> bool:
        """
        Switch image function should be called per frame
        :param switch_rate: switch rate between each change
        :return: True if loop finished, False if loop not finished
        """
        if self._image_switch_interval >= switch_rate:
            self._image_switch = (self._image_switch + 1) % len(self._main_image_type)
            self.image = self._main_image_type[self._image_switch]
            self._image_switch_interval = 0
            if self._image_switch == 0:
                return True
        else:
            self._image_switch_interval += 1
        return False

    def _set_image_type(self, image_type) -> None:
        """
        Change main loop image
        :param image_type: Name of the type of image to put into loop
        """
        self._main_image_type = self.IMAGE[image_type]
        self._image_switch = 0
        self._image_switch_interval = 0

    @classmethod
    @abstractmethod
    def _init_image(cls) -> None:
        """ Override this method to load images """
        cls.IMAGE = dict()
        cls.IMAGE["BASE"] = []
        cls.IMAGE["IDLE"] = []
        cls.IMAGE["EXPLODE"] = []
        cls._IS_SET_IMAGE = False

