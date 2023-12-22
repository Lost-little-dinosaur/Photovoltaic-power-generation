from classes.component import Component

class Arrangement:
    def __init__(self, verticalCount, crossCount, component, width, length, type):
        # self.specification = specification  # 排布的类型
        self.verticalCount = verticalCount  # 竖排布数量
        self.crossCount = crossCount  # 横排布数量
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
        self.componentArray = []
        pass

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

    # def draw(self, x, y):
    #     self.start_x = x
    #     self.start_y = y


# 组件排布的规格
arrangement1 = Arrangement(2, 0, Component, 3.307, 4.135, "基墩")
arrangement2 = Arrangement(4, 1, Component, 6.834, 9.865, "基墩")


arrangements = [arrangement1, arrangement2]