from pygame.locals import *


class KeyBinds:
    UP_PLAYER_1 = K_w
    DOWN_PLAYER_1 = K_s
    UP_PLAYER_2 = K_UP
    DOWN_PLAYER_2 = K_DOWN


class Config:
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500

    PLAYER_SIZE = (10, 200)
    PLAYER_COLOUR = (255, 128, 128)

    BALL_SIZE = (30, 30)
    BALL_COLOUR = (100, 100, 100)
    FPS = 60

    PLAYER_SPEED = 3
