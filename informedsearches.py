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

    def _run(self, sov=None):
        s  = sov or self.start
        h  = HEUR[self.heur]
        t0 = time.time()
        fn = astar if self.algo == "A*" else gbfs
        path, vis, nv, front_at = fn(self.grid, self.ROWS, self.COLS, s, self.goal, h)
        self.et       = (time.time() - t0) * 1000
        self.vis      = vis
        self.nv       = nv
        self.front_at = front_at
        if path:
            self.path  = path
            self.pset  = set(path)
            self.pc    = len(path) - 1
            if sov is None:
                self.vstep = 0
                self.mode  = "searching"
            else:
                self.vstep = len(vis)
                self.mode  = "running"
                self.ai    = 0
                self.apos  = path[0]
        else:
            self.path = []
            self.pset = set()
            self.mode = "no_path"
        self.lt = time.time()
        return path is not None

    def _step(self):
        if time.time() - self.lt < 0.04:
            return
        self.lt = time.time()
        if self.mode == "searching":
            self.vstep = min(self.vstep + 1, len(self.vis))
            if self.vstep < len(self.vis):
                node = self.vis[self.vstep]
                self.front = self.front_at.get(node, set())
            else:
                self.front = set()
            if self.vstep >= len(self.vis):
                if self.path:
                    self.mode = "running"
                    self.ai   = 0
                    self.apos = self.path[0]
                else:
                    self.mode = "no_path"
        elif self.mode == "running":
            self.ai += 1
            if self.ai >= len(self.path):
                self.mode = "done"
                self.apos = self.goal
            else:
                self.apos = self.path[self.ai]
                if self.dyn:
                    self._spawn()
            if self.rfsh > 0:
                self.rfsh -= 1

    def _spawn(self):
        if random.random() > self.dyn_prob:
            return
        r    = random.randint(0, self.ROWS - 1)
        c    = random.randint(0, self.COLS - 1)
        cell = (r, c)
        if cell in (self.start, self.goal, self.apos):
            return
        if self.grid[r][c] == 1:
            return
        self.grid[r][c] = 1
        self.nwalls.add(cell)
        if cell in set(self.path[self.ai:]):
            sv = self.apos
            self._run(sov=sv)
            self.rfsh = 20

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

    def draw(self):
        self.screen.fill(BG_APP)
        self._draw_top()
        self._draw_left()
        self._draw_grid()
        pygame.display.flip()

    def _draw_top(self):
        pygame.draw.rect(self.screen, BG_TOP, pygame.Rect(0, 0, self.W, TOP_H))
        pygame.draw.line(self.screen, (155, 172, 218), (0, TOP_H), (self.W, TOP_H), 2)

        labels = ["Nodes Visited", "Path Cost", "Exec Time"]
        vals   = [str(self.nv), str(self.pc), f"{self.et:.1f} ms"]
        cw     = 160
        gap    = 14
        total  = cw * 3 + gap * 2
        sx     = self.W // 2 - total // 2
        for i in range(3):
            rx   = sx + i * (cw + gap)
            ry   = 8
            card = pygame.Rect(rx, ry, cw, TOP_H - 16)
            rr(self.screen, (255, 255, 255), card, 8)
            rrb(self.screen, M_COLS[i], card, 2, 8)
            pygame.draw.rect(self.screen, M_COLS[i],
                pygame.Rect(rx, ry, 5, TOP_H - 16),
                border_top_left_radius=8, border_bottom_left_radius=8)
            tx(self.screen, labels[i], rx + 12, ry + 6,  C_MED,     f10)
            tx(self.screen, vals[i],   rx + 12, ry + 24, M_COLS[i], f18)

    def _draw_left(self):
        pygame.draw.rect(self.screen, BG_LEFT, pygame.Rect(0, TOP_H, LEFT_W, self.H - TOP_H))
        vln(self.screen, LEFT_W, TOP_H, self.H)

        mx, my = pygame.mouse.get_pos()
        lx = 8
        y  = TOP_H + 12
        W2 = LEFT_W - 16
        sp = 6

        sec_hdr(self.screen, "GRID CONFIG", lx, y)
        y += 22
        iw = 50
        self.ibR.rect = pygame.Rect(lx,       y + 18, iw, 26)
        self.ibC.rect = pygame.Rect(lx + 56,  y + 18, iw, 26)
        self.ibD.rect = pygame.Rect(lx + 112, y + 18, iw, 26)
        for ib in self.ibs:
            ib.draw(self.screen, mx, my)
        y += 54

        bw = (W2 - sp) // 2
        b1 = pygame.Rect(lx,           y, bw, 27)
        b2 = pygame.Rect(lx + bw + sp, y, bw, 27)
        draw_btn(self.screen, "▶ Apply",    b1, hover=b1.collidepoint(mx, my), act=(40, 140, 68))
        draw_btn(self.screen, "⚙ Gen Maze", b2, hover=b2.collidepoint(mx, my), act=(105, 50, 190))
        self._u["b1"] = b1
        self._u["b2"] = b2
        y += 38

        sec_hdr(self.screen, "ALGORITHM", lx, y)
        y += 22
        bw = (W2 - sp) // 2
        a1 = pygame.Rect(lx,           y, bw, 28)
        a2 = pygame.Rect(lx + bw + sp, y, bw, 28)
        draw_btn(self.screen, "A* Search", a1, active=self.algo == "A*",   hover=a1.collidepoint(mx, my))
        draw_btn(self.screen, "GBFS",      a2, active=self.algo == "GBFS", hover=a2.collidepoint(mx, my), act=(105, 50, 190))
        self._u["a1"] = a1
        self._u["a2"] = a2
        y += 40

        sec_hdr(self.screen, "HEURISTIC", lx, y)
        y += 22
        hw = (W2 - sp) // 2
        self._u["rH"] = []
        for i, n in enumerate(HEUR):
            r = pygame.Rect(lx + i * (hw + sp), y, hw, 26)
            draw_btn(self.screen, n, r, active=self.heur == n, hover=r.collidepoint(mx, my), fn=f11)
            self._u["rH"].append((n, r))
        y += 40

        sec_hdr(self.screen, "EDIT MODE", lx, y)
        y += 22
        em = [
            ("Wall",  "wall",  (185,  48,  48)),
            ("Erase", "erase", ( 38, 148,  68)),
            ("Start", "start", (120,  48, 180)),
            ("Goal",  "goal",  (180,  60,  60)),
        ]
        ew = (W2 - sp * 3) // 4
        self._u["rE"] = []
        for i, (lb, md, ac) in enumerate(em):
            r = pygame.Rect(lx + i * (ew + sp), y, ew, 26)
            draw_btn(self.screen, lb, r, active=self.draw_mode == md, hover=r.collidepoint(mx, my), fn=f10, act=ac)
            self._u["rE"].append((md, r))
        y += 40

        sec_hdr(self.screen, "ACTIONS", lx, y)
        y += 22
        bw = (W2 - sp) // 2
        s1 = pygame.Rect(lx,           y, bw, 30)
        s2 = pygame.Rect(lx + bw + sp, y, bw, 30)
        draw_btn(self.screen, "▶ START", s1, hover=s1.collidepoint(mx, my), act=(40, 140, 68))
        draw_btn(self.screen, "Reset",   s2, hover=s2.collidepoint(mx, my), act=(168, 38, 38))
        self._u["s1"] = s1
        self._u["s2"] = s2
        y += 40

        sec_hdr(self.screen, "DYNAMIC MODE", lx, y)
        y += 22
        rd = pygame.Rect(lx, y, W2, 28)
        dl = "⚡ Dynamic: ON" if self.dyn else "  Dynamic: OFF"
        draw_btn(self.screen, dl, rd, active=self.dyn, hover=rd.collidepoint(mx, my),
                 act=(155, 30, 110), fn=f11)
        self._u["rd"] = rd

    def _draw_grid(self):
        pygame.draw.rect(self.screen, BG_GRID,
                         pygame.Rect(self.gx, self.gy, self.gw, self.gh))

        cs   = self.cs
        ox   = self.ox
        oy   = self.oy
        vset = set(self.vis[:self.vstep])

        for r in range(self.ROWS):
            for c in range(self.COLS):
                cell  = (r, c)
                px    = ox + c * cs
                py    = oy + r * cs
                inner = pygame.Rect(px + 1, py + 1, cs - 2, cs - 2)
                rad   = max(2, min(cs // 7, 5))

                if self.grid[r][c] == 1:
                    bg = C_DYNWALL if cell in self.nwalls else C_WALL
                    rr(self.screen, bg, inner, rad)
                    if cs >= 20:
                        tx(self.screen, "-1", px + cs // 2, py + cs // 2, C_WALL_TXT, f10, cx=True, cy=True)
                elif cell == self.start:
                    rr(self.screen, C_START_BG, inner, rad)
                    if cs >= 14:
                        tx(self.screen, "S", px + cs // 2, py + cs // 2, C_START_TXT, f14, cx=True, cy=True)
                elif cell == self.goal:
                    rr(self.screen, C_GOAL_BG, inner, rad)
                    if cs >= 14:
                        tx(self.screen, "G", px + cs // 2, py + cs // 2, C_GOAL_TXT, f14, cx=True, cy=True)
                elif self.mode in ("running", "done") and cell in self.pset:
                    rr(self.screen, C_PATH, inner, rad)
                elif cell in self.front:
                    rr(self.screen, C_FRONTIER, inner, rad)
                elif cell in vset:
                    rr(self.screen, C_VISITED, inner, rad)
                else:
                    rr(self.screen, C_EMPTY, inner, rad)

                pygame.draw.rect(self.screen, BORD_LT, pygame.Rect(px, py, cs, cs), 1)

        if self.apos and self.mode in ("running", "done"):
            r,  c  = self.apos
            cx = ox + c * cs + cs // 2
            cy = oy + r * cs + cs // 2
            ar = max(cs // 3, 4)
            pygame.draw.circle(self.screen, (255, 225, 170), (cx, cy), ar + 3)
            pygame.draw.circle(self.screen, C_AGENT,         (cx, cy), ar)
            pygame.draw.circle(self.screen, C_WHITE,         (cx, cy), ar, 2)

        gw2 = cs * self.COLS
        gh2 = cs * self.ROWS
        pygame.draw.rect(self.screen, (115, 138, 205),
                         pygame.Rect(ox - 1, oy - 1, gw2 + 2, gh2 + 2), 2)

        if cs >= 22:
            if oy - self.gy >= 16:
                for c in range(self.COLS):
                    tx(self.screen, str(c), ox + c * cs + cs // 2, oy - 15, C_MED, f9, cx=True)
            if ox - self.gx >= 16:
                for r in range(self.ROWS):
                    lbl_y = oy + r * cs + cs // 2
                    if self.gy <= lbl_y <= self.gy + self.gh:
                        tx(self.screen, str(r), ox - 14, lbl_y, C_MED, f9, cy=True)

        if self.rfsh > 0:
            a  = min(self.rfsh * 10, 100)
            sf = pygame.Surface((self.gw, self.gh), pygame.SRCALPHA)
            sf.fill((205, 75, 160, a))
            self.screen.blit(sf, (self.gx, self.gy))
            tx(self.screen, "⚡ RE-PLANNING",
               self.gx + self.gw // 2, self.gy + self.gh // 2,
               (160, 20, 100), f16, cx=True, cy=True)

        if self.mode == "no_path":
            cx  = self.gx + self.gw // 2
            cy  = self.gy + self.gh // 2
            bw  = 320
            bh  = 72
            box = pygame.Rect(cx - bw // 2, cy - bh // 2, bw, bh)
            rr(self.screen,  (255, 255, 255), box, 10)
            rrb(self.screen, (190,  40,  40), box, 2, 10)
            tx(self.screen, "✘  Path Not Found",
               cx, cy - 14, (190, 35, 35), f16, cx=True, cy=True)
            tx(self.screen, "No route exists between Start and Goal",
               cx, cy + 16, (130, 60, 60), f11, cx=True, cy=True)

    def run(self):
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.VIDEORESIZE:
                    self.W = max(ev.w, 700)
                    self.H = max(ev.h, 480)
                    self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
                elif ev.type == pygame.KEYDOWN:
                    for ib in self.ibs:
                        ib.key(ev)
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self._click(ev.pos)
                elif ev.type == pygame.MOUSEMOTION and ev.buttons[0]:
                    self._drag(ev.pos)

            if self.mode in ("searching", "running"):
                self._step()
            if self.mode != "running":
                self.nwalls.clear()
            self.draw()
            self.clock.tick(60)

    def _click(self, pos):
        mx, my = pos
        any_ = False
        for ib in self.ibs:
            if ib.rect.collidepoint(mx, my):
                ib.active = True
                any_ = True
            else:
                ib.active = False
        if any_:
            return
        for ib in self.ibs:
            ib.active = False

        u = self._u

        def ck(k):
            return k in u and u[k].collidepoint(mx, my)

        if ck("b1"):
            self._apply_cfg()
            return
        if ck("b2"):
            self._apply_cfg()
            self.gen_maze()
            return
        if ck("a1"):
            self.algo = "A*"
            return
        if ck("a2"):
            self.algo = "GBFS"
            return
        for n, r in u.get("rH", []):
            if r.collidepoint(mx, my):
                self.heur = n
                return
        for md, r in u.get("rE", []):
            if r.collidepoint(mx, my):
                self.draw_mode = None if self.draw_mode == md else md
                return
        if ck("s1"):
            self._clr()
            self._run()
            return
        if ck("s2"):
            self.reset_grid()
            return
        if ck("rd"):
            self.dyn = not self.dyn
            return

        if self.gx <= mx < self.gx + self.gw and self.gy <= my < self.gy + self.gh:
            cell = self.p2c(mx, my)
            if cell:
                self._edit(cell)

    def _drag(self, pos):
        mx, my = pos
        if self.gx <= mx < self.gx + self.gw and self.gy <= my < self.gy + self.gh:
            if self.draw_mode in ("wall", "erase"):
                cell = self.p2c(mx, my)
                if cell:
                    self._edit(cell)

    def _edit(self, cell):
        r, c = cell
        if self.draw_mode == "wall":
            if cell not in (self.start, self.goal):
                self.grid[r][c] = 1
                self._clr()
        elif self.draw_mode == "erase":
            self.grid[r][c] = 0
            self._clr()
        elif self.draw_mode == "start":
            self.grid[r][c] = 0
            self.start = cell
            self._clr()
        elif self.draw_mode == "goal":
            self.grid[r][c] = 0
            self.goal = cell
            self._clr()


if __name__ == "__main__":
    App().run()