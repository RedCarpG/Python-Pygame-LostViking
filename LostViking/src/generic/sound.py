import pygame, os
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
sound_dir = os.path.join(main_dir, 'sound')


def load_sound(name, volume):
    class NoneSound:
        def play(self): print("--无音频")

    if not pygame.mixer or not pygame.mixer.get_init():
        print("--Mixer未启动,%s加载失败！" % name)
        return NoneSound()
    fullname = os.path.join(sound_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
        sound.set_volume(volume)
        print("--音频%s加载成功！" % name)
    except pygame.error:
        print('！！--找不到音乐: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


def load_music(name, volume):
    class NoneSound:
        def play(self): print("--无音乐")

    if not pygame.mixer or not pygame.mixer.get_init():
        print("--Mixer未启动,音乐加载失败！")
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
            print("--音乐%s加载成功！" % name[0])
            for each_name in fullname[1:]:
                pygame.mixer.music.queue(each_name)
        else:
            pygame.mixer.music.load(fullname)
            print("--音乐%s加载成功！" % name)
        pygame.mixer.music.set_volume(volume)
    except pygame.error:
        print('!!--找不到音效: %s' % fullname)
        raise SystemExit(str(geterror()))
