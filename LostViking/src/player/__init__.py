from .player_event_handler import detect_player_event
from .player_interface import *


def init_player():
    # Init Player Plane
    from .PlayerPlane import PlayerPlane
    PlayerPlane.init_player()
    from .PlayerBullet import init_player_bullet
    init_player_bullet()
    from .PlayerBomb import init_bomb
    init_bomb()


def create_player(player_num=1):
    from .PlayerPlane import PlayerPlane
    if player_num == 1:
        return PlayerPlane()
    else:
        # TODO Point for P1, P2
        return PlayerPlane(point=None), PlayerPlane(point=None, p_id=2)

