from .player_event_handler import detect_player_event
from .player_interface import *


def init_player_image():
    from .player_plane import MyPlane
    MyPlane.init_image()
    from .player_bullet import PlayerBullet1
    PlayerBullet1.init_image()
    from .player_bomb import PlayerNucBomb, Explosion
    PlayerNucBomb.init_image()
    Explosion.init_image()


def init_player_sound():
    from .player_plane import MyPlane
    MyPlane.init_sound()
    from .player_bomb import PlayerNucBomb
    PlayerNucBomb.init_sound()


def create_player(player_num=1):
    from .player_plane import MyPlane
    if player_num == 1:
        return MyPlane()
    else:
        # TODO Point for P1, P2
        return MyPlane(point=None), MyPlane(point=None, p_id=2)

