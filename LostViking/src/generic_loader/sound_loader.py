import os
import pygame
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
sound_dir = os.path.join(main_dir, '../../data/sound')

_SOUND = {}


def play_sound(label):
    _SOUND[label].stop()
    _SOUND[label].play()


def load_sound(name, volume):
    class NoneSound:
        def play(self): print("-- No sound file")

    if not pygame.mixer or not pygame.mixer.get_init():
        print("-- Mixer hasn't initialized, failed loading sound！")
        return NoneSound()
    fullname = os.path.join(sound_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
        sound.set_volume(volume)
        print("-- Sound {} loaded successfully！".format(name))
    except pygame.error:
        print('!!-- Can not find audio file : {}'.format(fullname))
        raise SystemExit(str(geterror()))
    return sound


def load_music(name, volume):
    class NoneSound:
        def play(self): print("-- No music file")

    if not pygame.mixer or not pygame.mixer.get_init():
        print("-- Mixer hasn't initialized, failed loading music！")
        return NoneSound()
    if isinstance(name, list):
        fullname = []
        for each_name in name:
            fullname.append(os.path.join(sound_dir, each_name))
    else:
        fullname = os.path.join(sound_dir, name)
    try:
        if isinstance(name, list):
            pygame.mixer.music.load(fullname[0])
            print("-- Music {} loaded successfully！".format(name[0]))
            for each_name in fullname[1:]:
                pygame.mixer.music.queue(each_name)
        else:
            pygame.mixer.music.load(fullname)
            print("-- Music {} loaded successfully！".format(name))
        pygame.mixer.music.set_volume(volume)
    except pygame.error:
        print('!!-- Can not find audio file : {}'.format(fullname))
        raise SystemExit(str(geterror()))
