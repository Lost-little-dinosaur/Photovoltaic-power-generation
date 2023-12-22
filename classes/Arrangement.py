from const.const import components


class Arrangement:
    def __init__(self, specification, component, width, length, type):
        self.specification = specification  # 排布的类型
        self.component = component  # 使用组件的类型
        self.type = type  # 排布的方式：基墩，膨胀常规，膨胀抬高
        self.width = width  # 排布的宽度（上下）
        self.length = length  # 排布的长度（左右）
        self.array_x = []  # 竖梁相对位置
        self.array_y = []  # 横梁相对位置
        self.start_x = 0  # 排布左上角坐标x
        self.start_y = 0  # 排布左上角坐标y

    def chooselayout(self):
        if self.specification == "竖二" and self.type == "基墩":
            array_x = [107, 1707, 3307]
            array_y = [459, 1859, 2706, 4135]

        elif self.specification == "竖四横一" and self.type == "基墩":
            array_x = [417, 2417, 4417, 6417, 6834]
            array_y = [458, 1858, 2725, 4143, 5016, 6428, 6849, 8007, 8465, 9865]
        else:
            layout = "Default Layout"

        return array_x, array_y
    def draw(self, x, y):
        self.start_x = x
        self.start_y = y




