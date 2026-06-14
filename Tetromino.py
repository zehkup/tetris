import casedata

# ── 方块 ────────────────────────────────────────────
class Tetromino:
    def __init__(self, name):
        self.name = name
        self.shape = casedata.SHAPES[name]
        self.color = casedata.COLORS[name]
        self.row = 0
        self.col = casedata.BOARD_W // 2 - len(self.shape[0]) // 2

    # rotated()返回顺时针旋转90° 后的新形状（矩阵转置 + 行反转）
    def rotated(self):
        rows = len(self.shape)
        cols = len(self.shape[0])
        return [[self.shape[rows - 1 - c][r] for c in range(rows)]
                for r in range(cols)]