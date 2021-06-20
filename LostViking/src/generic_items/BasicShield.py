import warnings
from abc import abstractmethod
from pygame.sprite import DirtySprite
from ..groups import Shield_G


class BasicShield(DirtySprite):
    IMAGE = {"BASE": None,
             "IDLE": None}
    _IS_SET_IMAGE = False
    _IS_SET_ATTRS = False

    MAX_HEALTH = 1000

    def __init__(self, owner, **kwargs):
        # Check Initialization
        if not hasattr(self, "INIT_FLAG") or not self.INIT_FLAG:
            raise Exception("!!!ERROR: Class is not init! {}".format(self.__class__))
        if not self._IS_SET_IMAGE:
            raise Exception("!!!ERROR: Entity IMAGE is not set! {}".format(self.__class__))
        if not self._IS_SET_ATTRS:
            warnings.warn("!!!ERROR: Entity SPEED is not set! {}".format(self.__class__))
        DirtySprite.__init__(self, Shield_G)

        # Set Image properties
        self._main_image_type = self.IMAGE["BASE"]
        self._image_switch = 0
        self._image_switch_interval = 0
        self.image = self._main_image_type[self._image_switch]
        self._set_image_type("IDLE")
        # Set Rect
        self.rect = self.image.get_rect()

        # Set Attributes
        # Generic Attributes
        self.is_active = True
        self.dirty = 2
        self.visible = 0
        # Important Attributes
        self.health = self.MAX_HEALTH
        self.owner = owner

    def hit(self, damage, **kwargs):
        #self._play_sound('Shield')
        if self.health <= 0:
            self.is_active = False
            self.health = 0
        else:
            self.health -= damage
            self.visible = 1

    def _reposition(self):
        self.rect.center = self.owner.rect.center

    def update(self, *args, **kwargs):
        if self.visible:
            self._reposition()
            if self._switch_image():
                self.visible = 0

    @classmethod
    @abstractmethod
    def _init_attrs(cls):
        cls.MAX_HEALTH = 1000
        cls._IS_SET_ATTRS = False

    @classmethod
    @abstractmethod
    def _init_image(cls):
        cls.IMAGE = None
        cls._IS_SET_IMAGE = False

    # TODO Sound
    @classmethod
    def _init_sound(cls):
        cls._SOUND = dict()
        from ..generic_loader.sound_loader import load_sound
        from ..constants import MAIN_VOLUME
        cls._SOUND.setdefault("Shield", load_sound("Shield.wav", MAIN_VOLUME - 0.3))
        cls._INIT_FLAG_SOUND = True

    @classmethod
    def init(cls):
        if not hasattr(cls, "INIT_FLAG") or not cls.INIT_FLAG:
            cls._init_attrs()
            cls._init_image()
            cls.INIT_FLAG = True

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
