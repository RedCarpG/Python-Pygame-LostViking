import os
import sys

import pygame
from pygame.compat import geterror

_sound_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '../../data/sound')

_SOUND = {}
_MUSIC = pygame.mixer.music


def play_sound(label):
    """ Play sound from _SOUND dictionary which is previously loaded
    :param label: Name tag of the sound effect
    """
    if label in _SOUND:
        _SOUND[label].stop()
        _SOUND[label].play()
    else:
        print("<WARNING> Sound [{}] not exist".format(label), file=sys.stderr)


def del_sound(label):
    """ Delete a key label from _SOUND which is not needed
    :param label: Name tag of the sound effect
    """
    _SOUND.pop(label, None)


def load_sound(filename, volume, label):
    """ Load a sound file from filename, and add label in the dictionary
    :param filename: Filename, in the sound_dir
    :param volume: Volume to be set for the sound effect
    :param label: Label tag in the dictionary
    """
    if not pygame.mixer or not pygame.mixer.get_init():
        class NoneSound:
            def __init__(self, sound_label):
                self.label = sound_label

            def play(self):
                print("-- No sound played for {}".format(self.label))

        print("<WARNING> Mixer hasn't initialized, failed loading sound！", file=sys.stderr)
        _SOUND[label] = NoneSound(label)

    full_path = os.path.join(_sound_dir, filename)

    try:
        sound = pygame.mixer.Sound(full_path)
        print("<SUCCESS> Sound {} loaded！".format(filename))
    except pygame.error:
        print('<ERROR> !!! Can not find audio file : {}'.format(full_path), file=sys.stderr)
        raise SystemExit(str(geterror()))

    sound.set_volume(volume)
    _SOUND[label] = sound


def load_music(filename, volume):
    """ Load a sound file from filename to be played as music
    :param filename: Filename, in the sound_dir
    :param volume: Volume to be set for the music
    """

    if not pygame.mixer or not pygame.mixer.get_init():
        class NoneMusic:
            @classmethod
            def play(cls):
                print("-- No music played to play")

        print("<WARNING> Mixer hasn't initialized, failed loading music！", file=sys.stderr)
        return NoneMusic()

    if isinstance(filename, (list, tuple)):
        try:
            _MUSIC.load(os.path.join(_sound_dir, filename[0]))
        except pygame.error:
            print('<ERROR> !!! Can not find audio file in: {}'.format(filename[0]), file=sys.stderr)
            raise SystemExit(str(geterror()))

        for each_filename in filename[1:]:
            each_path = os.path.join(_sound_dir, each_filename)
            try:
                _MUSIC.queue(os.path.join(_sound_dir, each_path))
            except pygame.error:
                print('<ERROR> !!! Can not find audio file in: {}'.format(each_path), file=sys.stderr)
                raise SystemExit(str(geterror()))
            print("<SUCCESS> Music {} loaded！".format(each_path))
    else:
        full_path = os.path.join(_sound_dir, filename)
        try:
            _MUSIC.load(full_path)
            print("<SUCCESS> Music {} loaded！".format(filename))
        except pygame.error:
            print('<ERROR> !!! Can not find audio file in: {}'.format(full_path), file=sys.stderr)
            raise SystemExit(str(geterror()))
    _MUSIC.set_volume(volume)
