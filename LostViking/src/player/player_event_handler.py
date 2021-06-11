import pygame.event
from pygame.locals import *
from .PlayerPlane import PlayerPlane
from .PlayerBomb import PlayerNucBomb
from .player_event_type import *


def _start_player_shoot_event(player: PlayerPlane, player_id: int) -> None:
    if player_id == 1:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER1_SHOOT, {}))
        pygame.time.set_timer(EVENT_PLAYER1_SHOOT, player.get_attack_speed())
    else:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER2_SHOOT, {}))
        pygame.time.set_timer(EVENT_PLAYER2_SHOOT, player.get_attack_speed())


def _stop_player_shoot_event(player_id: int) -> None:
    if player_id == 1:
        pygame.time.set_timer(EVENT_PLAYER1_SHOOT, 0)
    else:
        pygame.time.set_timer(EVENT_PLAYER2_SHOOT, 0)


def _handle_player_shoot_event(player: PlayerPlane):
    player.shoot()


def _start_player_bomb_launch_event(player_id: int):
    if player_id == 1:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER1_BOMB, {}))
    else:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER2_BOMB, {}))


def _handle_player_bomb_launch_event(player: PlayerPlane):
    PlayerNucBomb.launch(player.get_position())


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

