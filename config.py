from pygame.locals import *


class KeyBinds:
    UP_PLAYER_1 = K_w
    DOWN_PLAYER_1 = K_s
    UP_PLAYER_2 = K_UP
    DOWN_PLAYER_2 = K_DOWN


class Config:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500

    PLAYER_SIZE = (30, 125)
    PLAYER_COLOUR = (255, 128, 128)
    PLAYER_SPEED = 10
    PLAYER_SCORE_FOR_BOUNCE = 1

    BALL_SIZE = (30, 30)
    BALL_COLOUR = (100, 100, 100)
    BALL_SPEED = 5
    COLLISION_STRENGTH = 10
    FPS = 60


