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
def F(sz, b=False):
    for n in ["Segoe UI", "Arial", "Helvetica"]:
        try:
            f = pygame.font.SysFont(n, sz, b)
            if f:
                return f
        except:
            pass
    return pygame.font.SysFont(None, sz, b)


def M(sz, b=False):
    for n in ["Consolas", "Courier New"]:
        try:
            f = pygame.font.SysFont(n, sz, b)
            if f:
                return f
        except:
            pass
    return pygame.font.SysFont(None, sz, b)


f9   = F(9);  f10 = F(10); f11 = F(11); f12 = F(12); f13 = F(13)
f14  = F(14, True); f16 = F(16, True); f18 = F(18, True)
fm12 = M(12, True)


def rr(s, c, r, rad=5):
    pygame.draw.rect(s, c, r, border_radius=rad)


def rrb(s, c, r, w=1, rad=5):
    pygame.draw.rect(s, c, r, width=w, border_radius=rad)


def tx(s, text, x, y, col=C_DARK, f=None, cx=False, cy=False):
    if f is None:
        f = f12
    sur = f.render(str(text), True, col)
    bx  = x - sur.get_width()  // 2 if cx else x
    by  = y - sur.get_height() // 2 if cy else y
    s.blit(sur, (bx, by))


def vln(s, x, y1, y2, c=(150, 165, 210)):
    pygame.draw.line(s, c, (x, y1), (x, y2), 1)


def draw_btn(s, label, rect, active=False, hover=False, fn=None,
             act=BTN_ACT, base=BTN_BG):
    if fn is None:
        fn = f12
    bg = act if active else (BTN_HOV if hover else base)
    rr(s, bg, rect, 5)
    rrb(s, (130, 110, 210) if not active else (55, 85, 190), rect, 1, 5)
    tx(s, label, rect.centerx, rect.centery, BTN_TXTA if active else BTN_TXT, fn, cx=True, cy=True)


def sec_hdr(s, lbl, x, y):
    tx(s, lbl, x, y, C_PURPLE, f13)