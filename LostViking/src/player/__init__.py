from .player_event_handler import detect_player_event
from .player_interface import *


def init_player():
    # Init Player Plane
    from .player_plane import init_player_plane
    init_player_plane()
    from .player_bullet import init_player_bullet
    init_player_bullet()
    from .player_bomb import init_bomb
    init_bomb()


def create_player(player_num=1):
    from .player_plane import MyPlane
    if player_num == 1:
        return MyPlane()
    else:
        # TODO Point for P1, P2
        return MyPlane(point=None), MyPlane(point=None, p_id=2)

