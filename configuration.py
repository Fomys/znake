# coding: utf8
#
# Configuration for snake game

from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT

#### Game configuration  ####

WINDOW_SIZE = (750, 750)
CASE_SIZE = (50, 50)
MAP_SIZE = (15, 15)

#### Image configuration ####

IMAGE_FOLDER = "images"

HEAD_IMG = "head.png"
BODY_STRAIGHT_IMG = "bodyStraight.png"
TAIL_IMG = "tail.png"
TURN_IMG = "bodyTurn.png"
GAME_OVER = "gameOver.png"
FRUITS_IMG = ["fruit1.png",
              "fruit2.png"]

#### KEYBINDING ####

KEYS = [K_UP, # TOP
        K_RIGHT, # RIGHT
        K_DOWN, #DOWN
        K_LEFT, #LEFT
        ]
