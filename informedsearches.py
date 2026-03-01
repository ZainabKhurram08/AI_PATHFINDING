import pygame
import heapq
import random
import time
import math
import sys

pygame.init()

TOP_H  = 70
LEFT_W = 215

BG_APP   = (200, 215, 245)
BG_TOP   = (180, 195, 235)
BG_LEFT  = (195, 175, 235)
BG_GRID  = (220, 228, 248)

C_EMPTY    = (250, 252, 255)
C_WALL     = (170, 178, 205)
C_WALL_TXT = (108, 116, 148)
C_FRONTIER = (255, 225,  55)
C_VISITED  = (100, 205, 225)
C_PATH     = (145, 220, 148)
C_START_BG = (200, 155, 220)
C_GOAL_BG  = (255, 140, 140)
C_START_TXT= ( 85,  18, 128)
C_GOAL_TXT = (138,  18,  18)
C_AGENT    = (255, 145,   0)
C_DYNWALL  = (255,  90, 160)

BORD_LT  = (205, 218, 240)

C_BLACK  = ( 25,  30,  45)
C_DARK   = ( 45,  55,  85)
C_MED    = ( 90, 105, 150)
C_WHITE  = (255, 255, 255)
C_PURPLE = (100,  55, 190)

M_COLS = [(115, 60, 205), (30, 150, 60), (190, 120, 18)]

BTN_BG   = (210, 200, 240)
BTN_HOV  = (195, 182, 230)
BTN_ACT  = ( 90, 118, 225)
BTN_TXT  = ( 55,  35, 120)
BTN_TXTA = (255, 255, 255)