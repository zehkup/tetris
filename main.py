"""
俄罗斯方块 — PySide6 实现
操作：← → 移动，↑ 旋转，↓ 加速下落，Space 直接落底，P 暂停，R 重开

功能一览：
标准 10×20 面板，七种方块（I/O/T/S/Z/J/L）
← → 左右移动，↑ 旋转，↓ 加速下落
Space 一键落底，P 暂停/继续，R 游戏结束后重开
右侧显示分数、消行数、等级、下一块预览
半透明落点投影辅助定位
每消 2 行升一级，下落速度递增（共 10 档）
"""


"""
俄罗斯方块/
├── main.py              # 程序入口（启动游戏）
├── constants.py         # 常量（BOARD_W, SHAPES, COLORS...）
├── tetromino.py         # Tetromino 类（方块形状、旋转）
├── board.py             # Board 类（碰撞、消行、计分）
├── game.py              # TetrisGame 类（界面绘制、按键）
└── .gitignore           # 忽略 __pycache__/
"""
import sys
import random
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtCore import Qt, QBasicTimer
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from 俄罗斯方块.TetrisGame import TetrisGame

# # ── 常量 ────────────────────────────────────────────
# BOARD_W = 10          # 列数
# BOARD_H = 20          # 行数
# BLOCK_SIZE = 30      # 像素
# PREVIEW_SIZE = 22
# SIDE_PANEL = 150      # 右侧面板宽度
# MARGIN = 10
# WINDOW_W = BOARD_W * BLOCK_SIZE + SIDE_PANEL + MARGIN * 3
# WINDOW_H = BOARD_H * BLOCK_SIZE + MARGIN * 2
# SCORE_TABLE = [0, 100, 300, 500, 800]
# LEVEL_SPEED = [800, 720, 630, 550, 470, 380, 300, 220, 140, 100]
#
#
# # ── 七种方块 ────────────────────────────────────────
# SHAPES = {
#     'I': [[1, 1, 1, 1]],
#     'O': [[1, 1],
#           [1, 1]],
#     'T': [[0, 1, 0],
#           [1, 1, 1]],
#     'S': [[0, 1, 1],
#           [1, 1, 0]],
#     'Z': [[1, 1, 0],
#           [0, 1, 1]],
#     'J': [[1, 0, 0],
#           [1, 1, 1]],
#     'L': [[0, 0, 1],
#           [1, 1, 1]],
# }
#
# COLORS = {
#     'I': QColor(0, 240, 240),
#     'O': QColor(240, 240, 0),
#     'T': QColor(160, 0, 240),
#     'S': QColor(0, 240, 0),
#     'Z': QColor(240, 0, 0),
#     'J': QColor(0, 0, 240),
#     'L': QColor(240, 160, 0),
# }
# GRID_COLOR = QColor(50, 50, 50)
# BG_COLOR = QColor(15, 15, 35)


# # ── 方块 ────────────────────────────────────────────
# class Tetromino:
#     def __init__(self, name):
#         self.name = name
#         self.shape = SHAPES[name]
#         self.color = COLORS[name]
#         self.row = 0
#         self.col = BOARD_W // 2 - len(self.shape[0]) // 2
#
#     # rotated()返回顺时针旋转90° 后的新形状（矩阵转置 + 行反转）
#     def rotated(self):
#         rows = len(self.shape)
#         cols = len(self.shape[0])
#         return [[self.shape[rows - 1 - c][r] for c in range(rows)]
#                 for r in range(cols)]


# # ── 游戏逻辑 ────────────────────────────────────────
# class Board:
#     def __init__(self):
#         self.grid = [[None] * BOARD_W for _ in range(BOARD_H)]
#         self.current = None
#         self.next = None
#         self.score = 0
#         self.lines = 0
#         self.level = 0
#         self.game_over = False
#         self.paused = False
#         self._new_piece()
#
#     # 生成新方块时调用：生成新方块，判断游戏结束
#     def _new_piece(self):
#         self.current = self.next if self.next else Tetromino(random.choice(list(SHAPES)))
#         self.next = Tetromino(random.choice(list(SHAPES)))
#         # self.current.row = 0
#         # self.current.col = BOARD_W // 2 - len(self.current.shape[0]) // 2  和61行重复
#         if self._collides(self.current.shape, self.current.row, self.current.col):
#             self.game_over = True
#
#     # 判断游戏结束，碰撞检测
#     def _collides(self, shape, row, col):
#         for r in range(len(shape)):
#             for c in range(len(shape[0])):
#                 if shape[r][c]:
#                     br, bc = row + r, col + c
#                     if br < 0 or br >= BOARD_H or bc < 0 or bc >= BOARD_W:
#                         return True
#                     if self.grid[br][bc]:
#                         return True
#         return False
#
#     #画布填充颜色，相当于移动俄罗斯方块
#     def _merge(self):
#         shape = self.current.shape
#         for r in range(len(shape)):
#             for c in range(len(shape[0])):
#                 if shape[r][c]:
#                     br = self.current.row + r
#                     bc = self.current.col + c
#                     if 0 <= br < BOARD_H and 0 <= bc < BOARD_W:
#                         self.grid[br][bc] = self.current.color
#         self._clear_lines()
#         self._new_piece()
#
#     #行满消除加分
#     def _clear_lines(self):
#         self.grid = [r for r in self.grid if any(c is None for c in r)]
#         n = BOARD_H - len(self.grid)#
#         for _ in range(n):
#             self.grid.insert(0, [None] * BOARD_W)
#         if n:
#             self.lines += n
#             self.score += SCORE_TABLE[n] * (self.level + 1)
#             self.level = min(self.lines // 2, 9)
#
#     def move_left(self):
#         if not self.game_over and not self.paused:
#             if not self._collides(self.current.shape, self.current.row, self.current.col - 1):
#                 self.current.col -= 1
#
#     def move_right(self):
#         if not self.game_over and not self.paused:
#             if not self._collides(self.current.shape, self.current.row, self.current.col + 1):
#                 self.current.col += 1
#
#     def move_down(self):
#         if not self.game_over and not self.paused:
#             if not self._collides(self.current.shape, self.current.row + 1, self.current.col):
#                 self.current.row += 1
#                 return True
#             self._merge()
#         return False
#
#     def hard_drop(self):
#         if not self.game_over and not self.paused:
#             while not self._collides(self.current.shape, self.current.row + 1, self.current.col):
#                 self.current.row += 1
#             self._merge()
#
#     def rotate(self):
#         if not self.game_over and not self.paused:
#             r = self.current.rotated()
#             if not self._collides(r, self.current.row, self.current.col):
#                 self.current.shape = r


# ── 主窗口 ──────────────────────────────────────────
# class TetrisGame(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.board = Board()
#         self._init_ui()
#         self.timer = QBasicTimer()
#         self.timer.start(LEVEL_SPEED[self.board.level], self)
#
#     def _init_ui(self):
#         self.setWindowTitle("俄罗斯方块")
#         self.setFixedSize(WINDOW_W, WINDOW_H)
#         self.setStyleSheet("background-color: #1a1a2e;")
#         font = QFont("Consolas", 12, QFont.Bold)#字体对象
#
#         self.lbl_score = QLabel("分数: 0", self)
#         self.lbl_score.setFont(font)
#         self.lbl_score.setStyleSheet("color: white;")
#         self.lbl_score.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN)
#
#         self.lbl_lines = QLabel("行数: 0", self)
#         self.lbl_lines.setFont(font)
#         self.lbl_lines.setStyleSheet("color: #aaa;")
#         self.lbl_lines.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 30)
#
#         self.lbl_level = QLabel("等级: 0", self)
#         self.lbl_level.setFont(font)
#         self.lbl_level.setStyleSheet("color: #ffcc00;")
#         self.lbl_level.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 60)
#
#         self.lbl_next = QLabel("下一个:", self)
#         self.lbl_next.setFont(font)
#         self.lbl_next.setStyleSheet("color: white;")
#         self.lbl_next.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 110)
#
#         self.lbl_status = QLabel("", self)
#         self.lbl_status.setFont(QFont("Consolas", 14, QFont.Bold))
#         self.lbl_status.setStyleSheet("color: #ff4444;")
#         self.lbl_status.setGeometry(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 300, 130, 60)
#         self.lbl_status.setAlignment(Qt.AlignCenter)
#
#         # self.show()
#
#     def paintEvent(self, event):
#         p = QPainter(self)
#         self._draw_board(p)
#         self._draw_ghost(p)
#         self._draw_current(p)
#         self._draw_next(p)
#         self._draw_status(p)
#
#     # ② 画棋盘格子、已固定的方块
#     def _draw_board(self, p):
#         x, y = MARGIN, MARGIN
#         w, h = BOARD_W * BLOCK_SIZE, BOARD_H * BLOCK_SIZE
#         p.fillRect(x, y, w, h, BG_COLOR) #画一个实心矩形，用颜色 BG_COLOR 填满
#         p.setPen(QPen(GRID_COLOR, 1))#设置画线条的笔，颜色 GRID_COLOR，粗细 1 像素，只影响后续的 drawLine() 画网格线
#         for r in range(BOARD_H + 1):
#             p.drawLine(x, y + r * BLOCK_SIZE, x + w, y + r * BLOCK_SIZE)
#         for c in range(BOARD_W + 1):
#             p.drawLine(x + c * BLOCK_SIZE, y, x + c * BLOCK_SIZE, y + h)
#         for r in range(BOARD_H):
#             for c in range(BOARD_W):
#                 color = self.board.grid[r][c]
#                 if color:
#                     self._draw_block(p, x + c * BLOCK_SIZE, y + r * BLOCK_SIZE, color)
#
#     # ③ 画半透明投影（落点预览）
#     def _draw_ghost(self, p):
#         """半透明投影"""
#         # if self.board.game_over or self.board.paused or not self.board.current:
#         if self.board.game_over or not self.board.current:
#             return
#         ghost_row = self.board.current.row
#         while not self.board._collides(self.board.current.shape, ghost_row + 1, self.board.current.col):
#             ghost_row += 1
#         shape = self.board.current.shape
#         color = QColor(self.board.current.color)#复制一份本体颜色，单独改阴影的透明度
#         # color = self.board.current.color   #直接拿了方块本体的颜色对象引用，setAlpha 改的是同一个对象，所以本体方块也变透明了。
#         color.setAlpha(60)
#         for r in range(len(shape)):
#             for c in range(len(shape[0])):
#                 if shape[r][c]:
#                     bx = MARGIN + (self.board.current.col + c) * BLOCK_SIZE
#                     by = MARGIN + (ghost_row + r) * BLOCK_SIZE
#                     p.fillRect(bx + 1, by + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2, color)
#
#     # ④ 画当前下落的方块
#     def _draw_current(self, p):
#         if self.board.game_over or self.board.paused or not self.board.current:
#             return
#         shape = self.board.current.shape
#         color = self.board.current.color
#         color.setAlpha(200)
#         for r in range(len(shape)):
#             for c in range(len(shape[0])):
#                 if shape[r][c]:
#                     bx = MARGIN + (self.board.current.col + c) * BLOCK_SIZE
#                     by = MARGIN + (self.board.current.row + r) * BLOCK_SIZE
#                     self._draw_block(p, bx, by, color)
#
#     def _draw_block(self, p, x, y, color, size=BLOCK_SIZE):
#         p.fillRect(x + 1, y + 1, size - 2, size - 2, color)
#         lighter = color.lighter(140)
#         p.setPen(QPen(lighter, 1))
#         p.drawLine(x + 1, y + 1, x + size - 2, y + 1)
#         p.drawLine(x + 1, y + 1, x + 1, y + size - 2)
#
#     # ⑤ 画右侧"下一个方块"预览
#     def _draw_next(self, p):
#         piece = self.board.next
#         if not piece:
#             return
#         ox = BOARD_W * BLOCK_SIZE + MARGIN * 2 + 10
#         oy = MARGIN + 140
#         for r in range(len(piece.shape)):
#             for c in range(len(piece.shape[0])):
#                 if piece.shape[r][c]:
#                     self._draw_block(p, ox + c * PREVIEW_SIZE, oy + r * PREVIEW_SIZE,
#                                      piece.color, PREVIEW_SIZE)
#
#     # ⑥ 画状态文字（GAME OVER / 暂停中）
#     def _draw_status(self, p):
#         if self.board.game_over:
#             self.lbl_status.setText("GAME OVER\n按 R 重开")
#         elif self.board.paused:
#             self.lbl_status.setText("暂停中\n按 P 继续")
#         else:
#             self.lbl_status.setText("")
#
#     def timerEvent(self, event):
#         if event.timerId() == self.timer.timerId():
#             self.board.move_down()
#             self._update_labels()
#             self.update()
#
#     def _update_labels(self):
#         self.lbl_score.setText(f"分数: {self.board.score}")
#         self.lbl_lines.setText(f"行数: {self.board.lines}")
#         self.lbl_level.setText(f"等级: {self.board.level}")
#         self.timer.start(LEVEL_SPEED[self.board.level], self)
#
#     def keyPressEvent(self, event):
#         k = event.key()
#         if k == Qt.Key_P and not self.board.game_over:
#             self.board.paused = not self.board.paused
#             self.update()
#             return
#         if k == Qt.Key_R and self.board.game_over:
#             self.board = Board()
#             self.timer.start(LEVEL_SPEED[0], self)
#             self.update()
#             return
#         actions = {
#             Qt.Key_Left: self.board.move_left,
#             Qt.Key_Right: self.board.move_right,
#             Qt.Key_Down: lambda: self.board.move_down() or None,
#             Qt.Key_Up: self.board.rotate,
#             Qt.Key_Space: self.board.hard_drop,
#         }
#         act = actions.get(k)
#         if act:
#             act()
#             self._update_labels()
#             self.update()


# ── 启动 ────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = TetrisGame()
    game.show()
    sys.exit(app.exec())
