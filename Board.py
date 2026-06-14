from  casedata import *
import random

from 俄罗斯方块.Tetromino import Tetromino


# ── 游戏逻辑 ────────────────────────────────────────
class Board:
    def __init__(self):
        self.grid = [[None] * BOARD_W for _ in range(BOARD_H)]
        self.current = None
        self.next = None
        self.score = 0
        self.lines = 0
        self.level = 0
        self.game_over = False
        self.paused = False
        self._new_piece()

    # 生成新方块时调用：生成新方块，判断游戏结束
    def _new_piece(self):
        self.current = self.next if self.next else Tetromino(random.choice(list(SHAPES)))
        self.next = Tetromino(random.choice(list(SHAPES)))
        # self.current.row = 0
        # self.current.col = BOARD_W // 2 - len(self.current.shape[0]) // 2  和61行重复
        if self._collides(self.current.shape, self.current.row, self.current.col):
            self.game_over = True

    # 判断游戏结束，碰撞检测
    def _collides(self, shape, row, col):
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c]:
                    br, bc = row + r, col + c
                    if br < 0 or br >= BOARD_H or bc < 0 or bc >= BOARD_W:
                        return True
                    if self.grid[br][bc]:
                        return True
        return False

    #画布填充颜色，相当于移动俄罗斯方块
    def _merge(self):
        shape = self.current.shape
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c]:
                    br = self.current.row + r
                    bc = self.current.col + c
                    if 0 <= br < BOARD_H and 0 <= bc < BOARD_W:
                        self.grid[br][bc] = self.current.color
        self._clear_lines()
        self._new_piece()

    #行满消除加分
    def _clear_lines(self):
        self.grid = [r for r in self.grid if any(c is None for c in r)]
        n = BOARD_H - len(self.grid)#
        for _ in range(n):
            self.grid.insert(0, [None] * BOARD_W)
        if n:
            self.lines += n
            self.score += SCORE_TABLE[n] * (self.level + 1)
            self.level = min(self.lines // 2, 9)

    def move_left(self):
        if not self.game_over and not self.paused:
            if not self._collides(self.current.shape, self.current.row, self.current.col - 1):
                self.current.col -= 1

    def move_right(self):
        if not self.game_over and not self.paused:
            if not self._collides(self.current.shape, self.current.row, self.current.col + 1):
                self.current.col += 1

    def move_down(self):
        if not self.game_over and not self.paused:
            if not self._collides(self.current.shape, self.current.row + 1, self.current.col):
                self.current.row += 1
                return True
            self._merge()
        return False

    def hard_drop(self):
        if not self.game_over and not self.paused:
            while not self._collides(self.current.shape, self.current.row + 1, self.current.col):
                self.current.row += 1
            self._merge()

    def rotate(self):
        if not self.game_over and not self.paused:
            r = self.current.rotated()
            if not self._collides(r, self.current.row, self.current.col):
                self.current.shape = r
