from classes.component import Component, components


class Arrangement:
    def __init__(self, verticalCount, crossCount, num, component, width, length, type):
        # self.specification = specification  # 排布的类型
        self.verticalCount = verticalCount  # 竖排布数量
        self.crossCount = crossCount  # 横排布数量
        self.num = num  # 列数
        self.component = component  # 使用组件的类型
        self.componentArray = []  # 组合排布中组件的详细信息
        self.type = type  # 排布的方式：基墩，膨胀常规，膨胀抬高
        self.width = width  # 排布的宽度（上下）
        self.length = length  # 排布的长度（左右）
        self.arrayX = []  # 竖梁相对位置
        self.arrayY = []  # 横梁相对位置
        self.startX = 0  # 排布左上角坐标x
        self.startY = 0  # 排布左上角坐标y

    def calculateComponentArray(self, startX, startY):
        # 通过输入的startX, startY和Arrangement本就有的信息计算出组件的排布坐标，添加到self.componentArray里
        x = startX
        y = startY
        if self.verticalCount == 2 and self.crossCount == 0:  # 竖二
            for i in range(2):
                for j in range(self.num):
                    self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
                                                         x, y, x + 1.134, y + 2.279, 1, i))
                    x = x + self.component.width + 0.006
            x = x - (self.component.width + 0.006) * self.num
            y = y + self.component.length + 0.012
        if self.verticalCount == 4 and self.crossCount == 1:  # 竖四横一
            for i in range(3):
                for j in range(self.num):
                    self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
                                                         x, y, x + 1.134, y + 2.279, 1, i))
                    x = x + self.component.width + 0.006
            x = x - (self.component.width + 0.006) * self.num
            y = y + self.component.length + 0.012
            for j in range(3):
                self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
                                                     x, y, x + 2.279, y + 1.134, 2, 4))
                x = x + self.component.length + 0.006
            x = x - (self.component.length + 0.006) * 3
            for i in range(3):
                for j in range(self.num):
                    self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
                                                         x, y, x + 1.134, y + 2.279, 1, i))
                    x = x + self.component.width + 0.006
            x = x - (self.component.width + 0.006) * self.num
            y = y + self.component.length + 0.012
        return self.componentArray

    # def chooseLayout(self):
    #     if self.specification == "竖二" and self.type == "基墩":
    #         array_x = [107, 1707, 3307]
    #         array_y = [459, 1859, 2706, 4135]
    #
    #     elif self.specification == "竖四横一" and self.type == "基墩":
    #         array_x = [417, 2417, 4417, 6417, 6834]
    #         array_y = [458, 1858, 2725, 4143, 5016, 6428, 6849, 8007, 8465, 9865]
    #     else:
    #         layout = "Default Layout"
    #
    #     return array_x, array_y

# 组件排布的规格
arrangement1 = Arrangement(2, 0, 3, components[0], 3.414, 4.570, "基墩")
arrangement2 = Arrangement(4, 1, 6, components[0], 6.834, 10.289, "基墩")

arrangements = [arrangement1, arrangement2]