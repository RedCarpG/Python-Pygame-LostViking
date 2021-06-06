from .player_plane import MyPlane
from .player_bullet import PlayerBullet1


class _PlayerProperty(object):
    NUC_BOMB_COUNT_MAX = 3
    Nuc_Bomb_Count = 0

    PLAYER_LIFE_MAX = 5
    Player_Life = 3


def set_player_bullet_type(player: MyPlane, bullet_type: int):
    if bullet_type == 1:
        player.change_bullet_type(PlayerBullet1)


def player_upgrade(player: MyPlane):
    player.level_up()


def get_level(player):
    return player.get_level()


def add_nuc_bomb():
    if _PlayerProperty.Nuc_Bomb_Count < _PlayerProperty.NUC_BOMB_COUNT_MAX:
        _PlayerProperty.Nuc_Bomb_Count += 1


def dec_nuc_bomb():
    _PlayerProperty.Nuc_Bomb_Count -= 1


def get_nuc_count():
    return _PlayerProperty.Nuc_Bomb_Count


def get_life_count():
    return _PlayerProperty.Player_Life


def add_life():
    if _PlayerProperty.Player_Life < _PlayerProperty.Player_Life:
        _PlayerProperty.Player_Life += 1


def dec_life():
    _PlayerProperty.Player_Life -= 1

