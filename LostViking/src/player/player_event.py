import pygame.event
from pygame.locals import *
from LostViking.src.event_manager import EM
from LostViking.src.player.player_plane import MyPlane
from LostViking.src.player.player_bomb import PlayerNucBomb

EVENT_PLAYER1_SHOOT = EM.add_event("player1_shoot")
EVENT_PLAYER1_BOMB = EM.add_event("player1_boom")
EVENT_PLAYER2_SHOOT = EM.add_event("player2_shoot")
EVENT_PLAYER2_BOMB = EM.add_event("player2_boom")


def start_player_shoot_event(player: MyPlane, player_id: int) -> None:
    if player_id == 1:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER1_SHOOT, {}))
        pygame.time.set_timer(EVENT_PLAYER1_SHOOT, player.get_attack_speed())
    else:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER2_SHOOT, {}))
        pygame.time.set_timer(EVENT_PLAYER2_SHOOT, player.get_attack_speed())


def stop_player_shoot_event(player_id: int) -> None:
    if player_id == 1:
        pygame.time.set_timer(EVENT_PLAYER1_SHOOT, 0)
    else:
        pygame.time.set_timer(EVENT_PLAYER2_SHOOT, 0)
        

def handle_player_shoot_event(player: MyPlane):
    player.shoot()


def start_player_bomb_event(player_id: int):
    if player_id == 1:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER1_BOMB, {}))
    else:
        pygame.event.post(pygame.event.Event(EVENT_PLAYER2_BOMB, {}))


def handle_player_bomb_event(player: MyPlane):
    PlayerNucBomb.launch(player.get_position())


def detect_player_event(e: pygame.event.Event, player1: MyPlane, player2=None):
    if e.type == KEYDOWN:
        # Space Button
        if e.key == K_SPACE:
            start_player_shoot_event(player1, 1)
        # Q Button
        if e.key == K_q:
            start_player_bomb_event(1)
    # --------------- Key Up Events ---------------
    elif e.type == KEYUP:
        if e.key == K_SPACE:
            stop_player_shoot_event(1)
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
            stop_player_shoot_event(1)

    # ---------------Mouse Events ---------------
    elif e.type == MOUSEBUTTONDOWN:
        # Trigger PlayerShoot Event
        if e.button == 1:
            start_player_shoot_event(player1, 1)
    elif e.type == MOUSEBUTTONUP:
        # Stop Player Shoot Event
        if e.button == 1:
            stop_player_shoot_event(1)

    # --------------- Customized Events ---------------
    elif e.type == EVENT_PLAYER1_SHOOT:
        handle_player_shoot_event(player1)

    elif e.type == EVENT_PLAYER1_BOMB:
        handle_player_bomb_event(player1)

