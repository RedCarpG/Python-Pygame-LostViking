from enum import Enum


from pygame.locals import *


class PLAYER1_CONTROL(Enum):
    MOVE_UP = K_w
    MOVE_DOWN = K_s
    MOVE_LEFT = K_a
    MOVE_RIGHT = K_d
    SHOOT = K_SPACE
    BOMB = K_q


class PLAYER2_CONTROL(Enum):
    MOVE_UP = K_UP
    MOVE_DOWN = K_DOWN
    MOVE_LEFT = K_LEFT
    MOVE_RIGHT = K_RIGHT
    SHOOT = K_SPACE
    BOMB = K_q
