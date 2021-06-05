from player_bullet import PlayerBullet1, Player_Bullet_G
from player_plane import MyPlane, Player1_G
from player_bomb import PlayerNucBomb, Player_NucBomb_G
from player_event import detect_player_event


def init_player_image():
    MyPlane.init_image()
    PlayerBullet1.init_image()
    PlayerNucBomb.init_image()


def init_player_sound():
    MyPlane.init_sound()
    PlayerNucBomb.init_sound()


def create_player(player_num=1):
    if player_num == 1:
        return MyPlane()
    else:
        # TODO Point for P1, P2
        return MyPlane(point=None), MyPlane(point=None, p_id=2)

