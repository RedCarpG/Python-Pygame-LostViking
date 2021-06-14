import pygame
from abc import ABC, abstractmethod
import warnings


class SoundHelper(object):

    def __init__(self):
        if not hasattr(self, "_INIT_FLAG_SOUND") or not self._INIT_FLAG_SOUND:
            warnings.warn("!!! ERROR: _SOUND value is not set! {}".format(self.__name__))
            self._init_sound()

    @classmethod
    @abstractmethod
    def _init_sound(cls):
        """ """
        cls._SOUND = dict()
        cls._INIT_FLAG_SOUND = False
