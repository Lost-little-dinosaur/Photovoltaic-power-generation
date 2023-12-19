from const.const import PhotovoltaicPanelCrossMargin, PhotovoltaicPanelVerticalDiffMargin


class Rectangle:
    def __init__(self, startY, startX, endY, endX, direction, row, marginRight, marginBottom):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.direction = direction  # 1表示纵向，2表示横向
        self.row = row
        self.marginRight = marginRight  # 该矩形右边的间距（只记录每个矩形下边的间距和右边的间距）
        self.marginBottom = marginBottom  # 该矩形下边的间距（只记录每个矩形下边的间距和右边的间距）
