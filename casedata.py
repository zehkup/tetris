# ── 常量 ────────────────────────────────────────────
from PySide6.QtGui import QColor

BOARD_W = 10          # 列数
BOARD_H = 20          # 行数
BLOCK_SIZE = 30      # 像素
PREVIEW_SIZE = 22
SIDE_PANEL = 150      # 右侧面板宽度
MARGIN = 10
WINDOW_W = BOARD_W * BLOCK_SIZE + SIDE_PANEL + MARGIN * 3
WINDOW_H = BOARD_H * BLOCK_SIZE + MARGIN * 2
SCORE_TABLE = [0, 100, 300, 500, 800]
LEVEL_SPEED = [800, 720, 630, 550, 470, 380, 300, 220, 140, 100]


# ── 七种方块 ────────────────────────────────────────
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
}

COLORS = {
    'I': QColor(0, 240, 240),
    'O': QColor(240, 240, 0),
    'T': QColor(160, 0, 240),
    'S': QColor(0, 240, 0),
    'Z': QColor(240, 0, 0),
    'J': QColor(0, 0, 240),
    'L': QColor(240, 160, 0),
}
GRID_COLOR = QColor(50, 50, 50)
BG_COLOR = QColor(15, 15, 35)