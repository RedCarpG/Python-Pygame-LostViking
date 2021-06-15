import pygame
from abc import ABC, abstractmethod
import warnings


class SoundHelper(object):
    _SOUND = None

    def __init__(self):
        if not hasattr(self, "_INIT_FLAG_SOUND") or not self._INIT_FLAG_SOUND:
            warnings.warn("!!! ERROR: _SOUND value is not set! {}".format(self.__name__))
            self._init_sound()

    def _play_sound(self, label):
        self._SOUND[label].stop()
        self._SOUND[label].play()

    @classmethod
    @abstractmethod
    def _init_sound(cls):
        """ """
        cls._SOUND = dict()
        cls._INIT_FLAG_SOUND = False
