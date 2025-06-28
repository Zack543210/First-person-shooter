import math
import pygame as pg


#game settings
ZOOM = 10 ## Zoom of the window
GLOOM = 12 ## Darkness
SPEED = 4 ## Player speed
PLAYER_POS = 4, 4 ## Player Position
SOLDIER_LIFE = 2 ## Gunshots to kill a soldier
CACAODEMON_LIFE = 3 ## Gunshots to kill a cacodemon
SOLDIER_ATTACK_DIST = 4 ## Max attack distance for a soldier
SIZE = 9 ## Player Size
GAME_LEVEL = 6

RES = WIDTH, HEIGHT = 16 * 10*ZOOM, 9 * 10*ZOOM
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

MOUSE_SENSITIVITY = 0.00015
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 10*ZOOM
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FLOOR_COLOR = (35, 35, 35)


PLAYER_ANGLE = 0
PLAYER_SPEED = SPEED / 1000 / 60 * FPS
PLAYER_ROT_SPEED = PLAYER_SPEED / 2
PLAYER_SIZE_SCALE = SIZE * ZOOM
PLAYER_MAX_HEALTH = 100

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 12

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2