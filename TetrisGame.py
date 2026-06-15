from PySide6.QtCore import QBasicTimer, Qt
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtWidgets import QMainWindow, QLabel
from casedata import  *
from Board import Board

class TetrisGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board = Board()
        self._init_ui()
        self.timer = QBasicTimer()
        self.timer.start(LEVEL_SPEED[self.board.level], self)

    def _init_ui(self):
        self.setWindowTitle("俄罗斯方块")
        self.setFixedSize(WINDOW_W, WINDOW_H)
        self.setStyleSheet("background-color: #1a1a2e;")
        font = QFont("Consolas", 12, QFont.Weight.Bold)#字体对象

        self.lbl_score = QLabel("分数: 0", self)
        self.lbl_score.setFont(font)
        self.lbl_score.setStyleSheet("color: white;")
        self.lbl_score.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN)

        self.lbl_lines = QLabel("行数: 0", self)
        self.lbl_lines.setFont(font)
        self.lbl_lines.setStyleSheet("color: #aaa;")
        self.lbl_lines.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 30)

        self.lbl_level = QLabel("等级: 0", self)
        self.lbl_level.setFont(font)
        self.lbl_level.setStyleSheet("color: #ffcc00;")
        self.lbl_level.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 60)

        self.lbl_next = QLabel("下一个:", self)
        self.lbl_next.setFont(font)
        self.lbl_next.setStyleSheet("color: white;")
        self.lbl_next.move(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 110)

        self.lbl_status = QLabel("", self)
        self.lbl_status.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        self.lbl_status.setStyleSheet("color: #ff4444;")
        self.lbl_status.setGeometry(BOARD_W * BLOCK_SIZE + MARGIN * 2, MARGIN + 300, 130, 60)
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        self._draw_board(p)
        self._draw_solidblocks(p)
        self._draw_ghost(p)
        self._draw_current(p)
        self._draw_next(p)
        self._draw_status(p)

    # ② 画棋盘格子
    def _draw_board(self, p):
        x, y = MARGIN, MARGIN
        w, h = BOARD_W * BLOCK_SIZE, BOARD_H * BLOCK_SIZE
        p.fillRect(x, y, w, h, BG_COLOR) #画一个实心矩形，用颜色 BG_COLOR 填满
        p.setPen(QPen(GRID_COLOR, 1))#设置画线条的笔，颜色 GRID_COLOR，粗细 1 像素，只影响后续的 drawLine() 画网格线
        for r in range(BOARD_H + 1):
            p.drawLine(x, y + r * BLOCK_SIZE, x + w, y + r * BLOCK_SIZE)
        for c in range(BOARD_W + 1):
            p.drawLine(x + c * BLOCK_SIZE, y, x + c * BLOCK_SIZE, y + h)

    # ③ 画当前方块的底部半透明投影（落点预览）
    def _draw_ghost(self, p):
        """半透明投影"""
        # if self.board.game_over or self.board.paused or not self.board.current:
        if self.board.game_over or not self.board.current:
            return
        ghost_row = self.board.current.row
        while not self.board._collides(self.board.current.shape, ghost_row + 1, self.board.current.col):
            ghost_row += 1
        shape = self.board.current.shape
        color = QColor(self.board.current.color)#复制一份本体颜色，单独改阴影的透明度
        # color = self.board.current.color   #直接拿了方块本体的颜色对象引用，setAlpha 改的是同一个对象，所以本体方块也变透明了。
        color.setAlpha(60)
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c]:
                    bx = MARGIN + (self.board.current.col + c) * BLOCK_SIZE
                    by = MARGIN + (ghost_row + r) * BLOCK_SIZE
                    p.fillRect(bx + 1, by + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2, color)

    #画物块
    def _draw_block(self, p, x, y, color, size=BLOCK_SIZE):
        p.fillRect(x + 1, y + 1, size - 2, size - 2, color)
        lighter = color.lighter(140)
        p.setPen(QPen(lighter, 1))
        p.drawLine(x + 1, y + 1, x + size - 2, y + 1)
        p.drawLine(x + 1, y + 1, x + 1, y + size - 2)

    #画棋盘底部已固定的方块
    def _draw_solidblocks(self, p):
        x, y = MARGIN, MARGIN
        for r in range(BOARD_H):
            for c in range(BOARD_W):
                color = self.board.grid[r][c]
                if color:
                    self._draw_block(p, x + c * BLOCK_SIZE, y + r * BLOCK_SIZE, color)

    # ④ 获取当前下落的方块，执行_draw_block画出来
    def _draw_current(self, p):
        if self.board.game_over or not self.board.current:
            return
        shape = self.board.current.shape
        color = self.board.current.color
        color.setAlpha(200)
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c]:
                    bx = MARGIN + (self.board.current.col + c) * BLOCK_SIZE
                    by = MARGIN + (self.board.current.row + r) * BLOCK_SIZE
                    self._draw_block(p, bx, by, color)

    # ⑤ 画右侧"下一个方块"预览
    def _draw_next(self, p):
        piece = self.board.next
        if not piece:
            return
        ox = BOARD_W * BLOCK_SIZE + MARGIN * 2 + 10
        oy = MARGIN + 140
        for r in range(len(piece.shape)):
            for c in range(len(piece.shape[0])):
                if piece.shape[r][c]:
                    self._draw_block(p, ox + c * PREVIEW_SIZE, oy + r * PREVIEW_SIZE,
                                     piece.color, PREVIEW_SIZE)

    # ⑥ 画状态文字（GAME OVER / 暂停中）
    def _draw_status(self, p):
        if self.board.game_over:
            self.lbl_status.setText("GAME OVER\n按 R 重开")
        elif self.board.paused:
            self.lbl_status.setText("暂停中\n按 P 继续")
        else:
            self.lbl_status.setText("")

    def _update_labels(self):
        self.lbl_score.setText(f"分数: {self.board.score}")
        self.lbl_lines.setText(f"行数: {self.board.lines}")
        self.lbl_level.setText(f"等级: {self.board.level}")
        self.timer.start(LEVEL_SPEED[self.board.level], self)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.board.move_down()
            self._update_labels()
            self.update()

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_P and not self.board.game_over:
            self.board.paused = not self.board.paused
            self.update()
            return
        if k == Qt.Key.Key_R and self.board.game_over:
            self.board = Board()
            self.timer.start(LEVEL_SPEED[0], self)
            self.update()
            return
        actions = {
            Qt.Key.Key_Left: self.board.move_left,
            Qt.Key.Key_Right: self.board.move_right,
            Qt.Key.Key_Down: lambda: self.board.move_down() or None,
            Qt.Key.Key_Up: self.board.rotate,
            Qt.Key.Key_Space: self.board.hard_drop,
        }
        act = actions.get(k)
        if act:
            act()
            self._update_labels()
            self.update()