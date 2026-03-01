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
    def hman(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuc(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


HEUR = {"Manhattan": hman, "Euclidean": heuc}
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def recon(cf, n):
    p = []
    while n is not None:
        p.append(n)
        n = cf[n]
    return p[::-1]


def astar(grid, R, C, s, g, h):
    gs  = {s: 0}
    cf  = {s: None}
    heap = [(h(s, g), 0, s)]
    vis  = set()
    ord_ = []
    front_at = {}
    ctr  = 0
    while heap:
        f, gc, n = heapq.heappop(heap)
        if n in vis:
            continue
        vis.add(n)
        ord_.append(n)
        front_at[n] = {x[2] for x in heap if x[2] not in vis}
        if n == g:
            return recon(cf, g), ord_, len(vis), front_at
        r, c = n
        for dr, dc in DIRS:
            nb = (r + dr, c + dc)
            if 0 <= nb[0] < R and 0 <= nb[1] < C and grid[nb[0]][nb[1]] != 1:
                ng = gc + 1
                if ng < gs.get(nb, 1e18):
                    gs[nb] = ng
                    cf[nb] = n
                    ctr += 1
                    heapq.heappush(heap, (ng + h(nb, g), ng, nb))
    return None, ord_, len(vis), front_at


def gbfs(grid, R, C, s, g, h):
    cf   = {s: None}
    heap = [(h(s, g), s)]
    vis  = set()
    ord_ = []
    front_at = {}
    ctr  = 0
    while heap:
        _, n = heapq.heappop(heap)
        if n in vis:
            continue
        vis.add(n)
        ord_.append(n)
        front_at[n] = {x[1] for x in heap if x[1] not in vis}
        if n == g:
            return recon(cf, g), ord_, len(vis), front_at
        r, c = n
        for dr, dc in DIRS:
            nb = (r + dr, c + dc)
            if 0 <= nb[0] < R and 0 <= nb[1] < C and grid[nb[0]][nb[1]] != 1 and nb not in vis:
                if nb not in cf:
                    cf[nb] = n
                ctr += 1
                heapq.heappush(heap, (h(nb, g), nb))
    return None, ord_, len(vis), front_at
class IBox:
    def __init__(self, lbl, default, mn, mx):
        self.lbl    = lbl
        self.val    = str(default)
        self.mn     = mn
        self.mx     = mx
        self.active = False
        self.rect   = pygame.Rect(0, 0, 52, 26)

    def get(self, fb):
        try:
            return max(self.mn, min(int(self.val), self.mx))
        except:
            return fb

    def key(self, ev):
        if not self.active:
            return
        if ev.key == pygame.K_BACKSPACE:
            self.val = self.val[:-1]
        elif ev.unicode.isdigit() and len(self.val) < 3:
            self.val += ev.unicode

    def draw(self, s, mx, my):
        hov = self.rect.collidepoint(mx, my)
        bc  = C_PURPLE if self.active else ((140, 110, 210) if hov else (165, 148, 215))
        rr(s, (238, 232, 255), self.rect, 4)
        rrb(s, bc, self.rect, 2 if self.active else 1, 4)
        cur = "_" if self.active and int(time.time() * 2) % 2 == 0 else ""
        tx(s, self.val + cur, self.rect.x + 5, self.rect.y + 5, C_BLACK, fm12)
        tx(s, self.lbl, self.rect.x, self.rect.y - 15, C_DARK, f10)
        class App:
    def __init__(self):
        self.W = 1100
        self.H = 720
        self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
        pygame.display.set_caption("Dynamic Pathfinding Agent — NUCES")
        self.clock = pygame.time.Clock()

        self.ROWS     = 18
        self.COLS     = 22
        self.density  = 0.25
        self.algo     = "A*"
        self.heur     = "Manhattan"
        self.dyn      = False
        self.dyn_prob = 0.04
        self.draw_mode = None

        self.ibR = IBox("Rows",  self.ROWS,             3, 40)
        self.ibC = IBox("Cols",  self.COLS,             3, 55)
        self.ibD = IBox("Dens%", int(self.density*100), 0, 80)
        self.ibs = [self.ibR, self.ibC, self.ibD]

        self.grid     = None
        self.start    = (0, 0)
        self.goal     = (self.ROWS - 1, self.COLS - 1)
        self.path     = []
        self.pset     = set()
        self.vis      = []
        self.vstep    = 0
        self.front_at = {}
        self.front    = set()
        self.apos     = None
        self.ai       = 0
        self.mode     = "idle"
        self.lt       = 0
        self.nv       = 0
        self.pc       = 0
        self.et       = 0.0
        self.nwalls   = set()
        self.rfsh     = 0
        self._u       = {}

        self.reset_grid()

    def reset_grid(self):
        self.grid = [[0] * self.COLS for _ in range(self.ROWS)]
        self.goal = (self.ROWS - 1, self.COLS - 1)
        self._clr()

    def _clr(self):
        self.path     = []
        self.pset     = set()
        self.vis      = []
        self.vstep    = 0
        self.front_at = {}
        self.front    = set()
        self.apos     = None
        self.ai       = 0
        self.mode     = "idle"
        self.nv       = 0
        self.pc       = 0
        self.et       = 0.0
        self.nwalls   = set()
        self.rfsh     = 0

    def gen_maze(self):
        self._clr()
        self.grid = [[0] * self.COLS for _ in range(self.ROWS)]
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if (r, c) not in (self.start, self.goal):
                    if random.random() < self.density:
                        self.grid[r][c] = 1

    @property
    def gx(self): return LEFT_W
    @property
    def gy(self): return TOP_H
    @property
    def gw(self): return self.W - LEFT_W
    @property
    def gh(self): return self.H - TOP_H
    @property
    def cs(self):
        return max(min(self.gw // self.COLS, self.gh // self.ROWS), 4)
    @property
    def ox(self): return self.gx + (self.gw - self.cs * self.COLS) // 2
    @property
    def oy(self): return self.gy + (self.gh - self.cs * self.ROWS) // 2

    def p2c(self, mx, my):
        cs = self.cs
        c  = (mx - self.ox) // cs
        r  = (my - self.oy) // cs
        if 0 <= r < self.ROWS and 0 <= c < self.COLS:
            return (r, c)
        return None

    def _apply_cfg(self):
        nr = self.ibR.get(self.ROWS)
        nc = self.ibC.get(self.COLS)
        nd = self.ibD.get(int(self.density * 100))
        self.density = nd / 100
        ch = (nr != self.ROWS or nc != self.COLS)
        self.ROWS = nr
        self.COLS = nc
        self.ibR.val = str(nr)
        self.ibC.val = str(nc)
        self.ibD.val = str(nd)
        if ch:
            self.start = (0, 0)
            self.goal  = (nr - 1, nc - 1)
            self.reset_grid()