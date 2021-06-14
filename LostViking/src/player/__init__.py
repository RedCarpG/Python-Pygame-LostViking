from .player_event_handler import detect_player_event, detect_key_pressed
from .player_interface import *


def init_player():
    # Init Player Plane
    from .PlayerPlane import Player1
    Player1.init()
    from .PlayerBullet import PlayerBullet1
    PlayerBullet1.init()
    from .PlayerBomb import PlayerNucBomb, Explosion
    PlayerNucBomb.init()
    Explosion.init()


def create_player(player_num=1):
    from .PlayerPlane import Player1
    if player_num == 1:
        return Player1()
    else:
        # TODO Point for P1, P2
        #return PlayerPlane(point=None), PlayerPlane(point=None, p_id=2)
        return None
