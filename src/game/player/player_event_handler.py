import pygame.event
from pygame.locals import *
from src.game.groups import G_Enemys

from src.helper.sound.sound_loader import play_sound
from .PLAYER_EVENT_TYPE import *
from .PlayerPlane import PlayerPlane
from .PlayerBomb import PlayerNucBomb


def trigger_player_shoot_event(player: PlayerPlane, id: int) -> None:
    if id == 1:
        pygame.event.post(pygame.event.Event(
            EVENT_PLAYER1_SHOOT, {"player": player}))
        pygame.time.set_timer(pygame.event.Event(
            EVENT_PLAYER1_SHOOT, {"player": player}), player.attack_speed)
    else:
        pygame.event.post(pygame.event.Event(
            EVENT_PLAYER2_SHOOT, {"player": player}))
        pygame.time.set_timer(pygame.event.Event(
            EVENT_PLAYER2_SHOOT, {"player": player}), player.attack_speed)


def _stop_player_shoot_event(player: PlayerPlane, id: int) -> None:
    if id == 1:
        pygame.time.set_timer(pygame.event.Event(
            EVENT_PLAYER1_SHOOT, {"player": player}), 0)
    else:
        pygame.time.set_timer(pygame.event.Event(
            EVENT_PLAYER2_SHOOT, {"player": player}), 0)


def _handle_player_shoot_event(player: PlayerPlane):
    player.attack()


def trigger_player_bomb_launch_event(player: PlayerPlane):
    pygame.event.post(pygame.event.Event(
        EVENT_PLAYER_BOMB, {"player": player}))


def _handle_player_bomb_launch_event(player: PlayerPlane):
    if player.bomb_count > 0:
        player.dec_bomb()
        PlayerNucBomb.launch(player.pos, player)
        pygame.event.set_blocked(EVENT_PLAYER_BOMB)
    else:
        play_sound("BOMB_ERROR")


def _handle_player_bomb_explode_event(player: PlayerPlane):
    from src.game.groups import G_Enemys, G_Enemy_Bullets
    for each in G_Enemys:
        if each.is_active:
            each.hit(1000)
            if not each.is_active:
                player.add_score(each.score)

    for each in G_Enemy_Bullets:
        each.hit()

    pygame.event.set_allowed(EVENT_PLAYER_BOMB)


def detect_key_pressed(player1: PlayerPlane, player2=None):
    # If Key Pressed
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w] or key_pressed[K_UP]:
        player1.trigger_move_up()
    elif key_pressed[K_s] or key_pressed[K_DOWN]:
        player1.trigger_move_back()
    elif key_pressed[K_a] or key_pressed[K_LEFT]:
        player1.trigger_move_left()
    elif key_pressed[K_d] or key_pressed[K_RIGHT]:
        player1.trigger_move_right()


def detect_player_event(e: pygame.event.Event, player1: PlayerPlane, player2=None):
    if e.type == KEYDOWN:
        # Space Button
        if e.key == K_SPACE:
            trigger_player_shoot_event(player1, 1)
        # Q Button
        elif e.key == K_q:
            trigger_player_bomb_launch_event(player1)
        else:
            return False
    # --------------- Key Up Events ---------------
    elif e.type == KEYUP:
        if e.key == K_SPACE:
            _stop_player_shoot_event(player1, 1)
        elif e.key == K_w:
            player1.trigger_stop_y()
        elif e.key == K_s:
            player1.trigger_stop_y()
        elif e.key == K_a:
            player1.trigger_stop_x()
        elif e.key == K_d:
            player1.trigger_stop_x()
        elif e.key == K_UP:
            player1.trigger_stop_y()
        elif e.key == K_DOWN:
            player1.trigger_stop_y()
        elif e.key == K_LEFT:
            player1.trigger_stop_x()
        elif e.key == K_RIGHT:
            player1.trigger_stop_x()
        else:
            return False

    # ---------------Mouse Events ---------------
    elif e.type == MOUSEBUTTONDOWN:
        # Trigger PlayerShoot Event
        if e.button == 1:
            trigger_player_shoot_event(player1, 1)
        else:
            return False
    elif e.type == MOUSEBUTTONUP:
        # Stop Player Shoot Event
        if e.button == 1:
            _stop_player_shoot_event(player1, 1)
        else:
            return False

    # --------------- Customized Events ---------------
    elif e.type == EVENT_PLAYER1_SHOOT or e.type == EVENT_PLAYER2_SHOOT:
        _handle_player_shoot_event(e.player)

    elif e.type == EVENT_PLAYER_BOMB:
        _handle_player_bomb_launch_event(e.player)
    elif e.type == EVENT_BOMB_EXPLODE:
        _handle_player_bomb_explode_event(e.player)
    else:
        return False
    return True
