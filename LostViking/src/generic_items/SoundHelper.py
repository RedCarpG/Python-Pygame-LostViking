import pygame
from abc import ABC, abstractmethod
import warnings


class SoundHelper(object):
    _SOUND = None
    _INIT_FLAG_SOUND = False

    def __init__(self):
        if not self._INIT_FLAG_SOUND:
            warnings.warn("!!! ERROR: _SOUND value is not set! {}".format(self.__name__))
            self._init_sound()

    @classmethod
    def _play_sound(cls, label):
        cls._SOUND[label].stop()
        cls._SOUND[label].play()

    @classmethod
    @abstractmethod
    def _init_sound(cls):
        """ """
        cls._SOUND = dict()
        cls._INIT_FLAG_SOUND = False
