import pygame.event
from pygame.locals import *

from src.helper.sound.sound_loader import play_sound
from .PLAYER_EVENT_TYPE import *
from .PlayerPlane import PlayerPlane
from .PlayerBomb import PlayerNucBomb


def _start_player_shoot_event(player: PlayerPlane, player_id: int) -> None:
    if player_id == 1:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER1_SHOOT, {}))
        pygame.time.set_timer(EVENT_PLAYER1_SHOOT, player.attack_speed)
    else:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER2_SHOOT, {}))
        pygame.time.set_timer(EVENT_PLAYER2_SHOOT, player.attack_speed)


def _stop_player_shoot_event(player_id: int) -> None:
    if player_id == 1:
        pygame.time.set_timer(EVENT_PLAYER1_SHOOT, 0)
    else:
        pygame.time.set_timer(EVENT_PLAYER2_SHOOT, 0)


def _handle_player_shoot_event(player: PlayerPlane):
    player.attack()


def _start_player_bomb_launch_event(player_id: int):
    if player_id == 1:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER1_BOMB, {}))
    else:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER2_BOMB, {}))


def _handle_player_bomb_launch_event(player: PlayerPlane):
    if player.bomb_count > 0:
        player.dec_nuc_bomb()
        PlayerNucBomb.launch(player.pos)
    else:
        play_sound("NUC_ERROR")


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
            _start_player_shoot_event(player1, 1)
        # Q Button
        if e.key == K_q:
            _start_player_bomb_launch_event(1)
    # --------------- Key Up Events ---------------
    elif e.type == KEYUP:
        if e.key == K_SPACE:
            _stop_player_shoot_event(1)
        if e.key == K_w:
            player1.trigger_stop_y()
        if e.key == K_s:
            player1.trigger_stop_y()
        if e.key == K_a:
            player1.trigger_stop_x()
        if e.key == K_d:
            player1.trigger_stop_x()
        if e.key == K_UP:
            player1.trigger_stop_y()
        if e.key == K_DOWN:
            player1.trigger_stop_y()
        if e.key == K_LEFT:
            player1.trigger_stop_x()
        if e.key == K_RIGHT:
            player1.trigger_stop_x()
        # Space Button
        if e.key == K_SPACE:
            _stop_player_shoot_event(1)

    # ---------------Mouse Events ---------------
    elif e.type == MOUSEBUTTONDOWN:
        # Trigger PlayerShoot Event
        if e.button == 1:
            _start_player_shoot_event(player1, 1)
    elif e.type == MOUSEBUTTONUP:
        # Stop Player Shoot Event
        if e.button == 1:
            _stop_player_shoot_event(1)

    # --------------- Customized Events ---------------
    elif e.type == EVENT_PLAYER1_SHOOT:
        _handle_player_shoot_event(player1)

    elif e.type == EVENT_PLAYER1_BOMB:
        _handle_player_bomb_launch_event(player1)

    elif e.type == EVENT_BOMB_EXPLODE:
        print(e.__dict__)
