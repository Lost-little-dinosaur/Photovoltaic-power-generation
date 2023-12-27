from classes.component import Component, components
from const.const import UNIT, INF, PhotovoltaicPanelCrossMargin, PhotovoltaicPanelVerticalMargin, \
    PhotovoltaicPanelVerticalDiffMargin


class Arrangement:
    def __init__(self, verticalCount, crossCount, verticalNum, crossNum, component, arrangeType, maxWindPressure):
        # self.specification = specification  # 排布的类型
        self.verticalCount = verticalCount  # 竖排布数量
        self.crossCount = crossCount  # 横排布数量
        self.verticalNum = verticalNum  # 竖排布列数量
        self.crossNum = crossNum  # 横排布列数量
        for c in components:
            if component == c.specification:
                self.component = c  # 使用组件的类型
                break
        else:
            raise Exception("组件'{}'不存在".format(component))
        self.componentArray = []  # 组合排布中组件的详细信息
        self.arrangeType = arrangeType  # 排布的类型：基墩，膨胀常规，膨胀抬高
        self.maxWindPressure = maxWindPressure  # 风压
        if crossCount == 0:
            self.width = verticalNum * self.component.width + (verticalNum - 1) * PhotovoltaicPanelCrossMargin
            self.length = verticalCount * self.component.length + (verticalCount - 1) * (
                    PhotovoltaicPanelVerticalMargin + PhotovoltaicPanelVerticalDiffMargin)
        elif verticalCount == 0:
            self.width = crossCount * self.component.length + (crossNum - 1) * PhotovoltaicPanelCrossMargin
            self.length = self.component.width
        else:
            self.width = max(crossCount * self.component.length + (crossCount - 1) * PhotovoltaicPanelCrossMargin,
                             verticalNum * self.component.width + (verticalNum - 1) * PhotovoltaicPanelCrossMargin)
            self.length = verticalCount * self.component.length + crossCount * self.component.length + (
                    verticalCount + crossCount - 1) * (
                                  PhotovoltaicPanelVerticalMargin + PhotovoltaicPanelVerticalDiffMargin)  # 计算长度和crossCount=0时一样就行

        self.crossPosition = INF  # 横排组件的位置
        self.arrayX = []  # 竖梁相对位置
        self.arrayY = []  # 横梁相对位置
        self.startX = 0  # 排布左上角坐标x
        self.startY = 0  # 排布左上角坐标y

    def calculateComponentArray(self, startX, startY):
        # 通过输入的startX, startY和Arrangement本就有的信息计算出组件的排布坐标，添加到self.componentArray里
        if self.verticalCount == 0: # 只有横排布（横一）
            for i in range(self.crossNum):
                cp = self.component, cp.startX = startX, cp.startY = startY
                cp.direction = 2
                cp.row = 1
                cp.endX = round((startX + self.component.length) / UNIT)
                cp.endY = round((startY + self.component.width) / UNIT)
                self.componentArray.append(cp)
                startX += round((self.component.width + 0.006) / UNIT)
        elif self.crossCount == 0:  # 只有竖排
            for i in range(self.verticalCount):
                for j in range(self.verticalNum):
                    cp = self.component, cp.startX = startX, cp.startY = startY
                    cp.direction = 1
                    cp.row = i
                    cp.endX = round((startX + self.component.width) / UNIT)
                    cp.endY = round((startY + self.component.length) / UNIT)
                    self.componentArray.append(cp)
                    startX += round((self.component.width + 0.006) / UNIT)
                startX -= round((self.component.width + 0.006) * self.verticalnum / UNIT)
                startY += round((self.component.length + 0.006) / UNIT)
        elif self.verticalCount == 1 and self.crossCount == 1: # 竖一横一
            for i in range(self.verticalNum):
                cp = self.component, cp.startX = startX, cp.startY = startY
                cp.direction = 1
                cp.row = 1
                cp.endX = round((startX + self.component.width) / UNIT)
                cp.endY = round((startY + self.component.length) / UNIT)
                self.componentArray.append(cp)
                startX += round((self.component.width + 0.006) / UNIT)
            startX = round((startX + self.component.width) / UNIT)
            startY = round((startY + self.component.width + 0.012) / UNIT)
            for i in range(self.crossNum):
                cp = self.component, cp.startY = startY
                cp.startX = round((startX - self.component.length) / UNIT)
                cp.row = 2
                cp.direction = 2
                cp.endX = startX
                cp.endY = round((startY + self.component.width) / UNIT)
                self.componentArray.append(cp)
                startX -= round((self.component.length + 0.006) / UNIT)
        else:#其他横竖情况
            for i in range(self.verticalCount - 1):
                for j in range(self.verticalNum):
                    cp = self.component, cp.startX = startX, cp.startY = startY
                    cp.direction = 1
                    cp.row = i
                    cp.endX = round((startX + self.component.width) / UNIT)
                    cp.endY = round((startY + self.component.length) / UNIT)
                    self.componentArray.append(cp)
                    startX += round((self.component.width + 0.006) / UNIT)
                startX -= round((self.component.width + 0.006) * self.verticalnum / UNIT)
                startY += round((self.component.length + 0.006) / UNIT)
            startY += round((self.component.width + 0.006 + 0.012) / UNIT)
            for i in range(self.verticalNum):
                cp = self.component, cp.startX = startX, cp.startY = startY
                cp.direction = 1
                cp.row = self.verticalNum
                cp.endX = round((startX + self.component.width) / UNIT)
                cp.endY = round((startY + self.component.length) / UNIT)
                self.componentArray.append(cp)
                startX += round((self.component.width + 0.006) / UNIT)
            startX -= round((0.006) / UNIT)
            startY -= round((self.component.width - 0.012) / UNIT)
            for i in range(self.crossNum):
                cp = self.component, cp.startY = startY
                cp.startX = round((startX - self.component.length) / UNIT)
                cp.row = self.verticalCount
                cp.direction = 2
                cp.endX = startX
                cp.endY = round((startY + self.component.width) / UNIT)
                self.componentArray.append(cp)
                startX -= round((self.component.length + 0.006) / UNIT)



        #if self.verticalCount == 2 and self.crossCount == 0:  # 竖二
        #    for i in range(2):
        #        for j in range(self.num):
        #            self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
        #                                                 startX, startY, startX + 1.134, startY + 2.279, 1, i))
        #            startX += round((self.component.width + 0.006) / UNIT)
        #    startX -= round((self.component.width + 0.006) * self.num / UNIT)
        #    startY += round((self.component.length + 0.012) / UNIT)
        #if self.verticalCount == 4 and self.crossCount == 1:  # 竖四横一
        #    for i in range(3):
        #        for j in range(self.num):
        #            self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
        #                                                 startX, startY, startX + 1.134, startY + 2.279, 1, i))
        #            # startX = startX + self.component.width + 0.006
        #            startX += round((self.component.width + 0.006) / UNIT)
        #    startX -= round((self.component.width + 0.006) * self.num / UNIT)
        #    startY += round((self.component.length + 0.012) / UNIT)
        #    for j in range(3):
        #        self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
        #                                             startX, startY, startX + 2.279, startY + 1.134, 2, 4))
        #        startX += round((self.component.length + 0.006) / UNIT)
        #    startX -= round((self.component.length + 0.006) * 3 / UNIT)
        #    for i in range(3):
        #        for j in range(self.num):
        #            self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
        #                                                 startX, startY, startX + 1.134, startY + 2.279, 1, i))
        #            startX += round((self.component.width + 0.006) / UNIT)
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


def calculateVerticalWidth(verticalNum, componentWidth):
    return verticalNum * componentWidth + (verticalNum - 1) * PhotovoltaicPanelCrossMargin


# component1 = Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35)  # 以米、瓦为单位
# component2 = Component("182-78", 1.134, 2.465, 580, 600, 0.30, 0.35)  # 以米、瓦为单位
# component3 = Component("210-60", 1.303, 2.172, 595, 605, 0.33, 0.35)  # 以米、瓦为单位
# component4 = Component("210-66", 1.303, 2.384, 650, 665, 0.33, 0.35)  # 以米、瓦为单位
# components = [component1, component2, component3, component4]
# 组件排布的规格
# verticalCount, crossCount, verticalNum, crossNum, component, arrangeType, maxWindPressure
arrangements = []
arrangements.append(Arrangement(1, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(1, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(2, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(2, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(3, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(3, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(4, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(4, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
arrangements.append(Arrangement(5, 0, INF, INF, "182-78", "膨胀常规", 1.2614))

arrangements.append(Arrangement(1, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(1, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(0, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(2, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(2, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(3, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(4, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
arrangements.append(Arrangement(5, 0, INF, INF, "210-60", "膨胀常规", 0.9785))

arrangements.append(Arrangement(0, 1, INF, INF, "210-60", "基墩", 0.9785))
arrangements.append(Arrangement(2, 0, INF, INF, "210-60", "基墩", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "210-60", "基墩", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "210-60", "基墩", 0.9785))
arrangements.append(Arrangement(1, 0, INF, INF, "210-60", "基墩", 0.9785))

arrangements.append(Arrangement(2, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(2, 1, INF, INF, "210-60", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(3, 1, INF, INF, "210-60", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(4, 1, INF, INF, "210-60", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(5, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))

arrangements.append(Arrangement(0, 1, INF, INF, "182-72", "基墩", 0.9785))
arrangements.append(Arrangement(2, 0, INF, INF, "182-72", "基墩", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "182-72", "基墩", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "182-72", "基墩", 0.9785))
arrangements.append(Arrangement(1, 0, INF, INF, "182-72", "基墩", 0.9785))

arrangements.append(Arrangement(1, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(1, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(0, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(2, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(2, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(3, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(4, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
arrangements.append(Arrangement(5, 0, INF, INF, "182-72", "膨胀常规", 0.9785))

arrangements.append(Arrangement(2, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(2, 1, INF, INF, "182-72", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(3, 1, INF, INF, "182-72", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(4, 1, INF, INF, "182-72", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(5, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))

arrangements.append(Arrangement(1, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(1, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(0, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(2, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(2, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(3, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(4, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
arrangements.append(Arrangement(5, 0, INF, INF, "182-78", "膨胀常规", 0.9785))

arrangements.append(Arrangement(0, 1, INF, INF, "182-78", "基墩", 0.9785))
arrangements.append(Arrangement(2, 0, INF, INF, "182-78", "基墩", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "182-78", "基墩", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "182-78", "基墩", 0.9785))
arrangements.append(Arrangement(1, 0, INF, INF, "182-78", "基墩", 0.9785))

arrangements.append(Arrangement(2, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(2, 1, INF, INF, "182-78", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(3, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(3, 1, INF, INF, "182-78", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(4, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(4, 1, INF, INF, "182-78", "膨胀抬高", 0.9785))
arrangements.append(Arrangement(5, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))

tempLength = len(arrangements)
for i in range(tempLength):
    if arrangements[i].verticalCount == 0:
        for j in range(2, 31):
            arrangements.append(Arrangement(arrangements[i].verticalCount, arrangements[i].crossCount, j,
                                            arrangements[i].crossNum, arrangements[i].component.specification,
                                            arrangements[i].arrangeType, arrangements[i].maxWindPressure))
            arrangements[-1].crossPosition = INF  # 没有竖排的时候，横排的位置是没有意义的
    elif arrangements[i].crossCount == 0:
        for j in range(1, 16):
            arrangements.append(Arrangement(arrangements[i].verticalCount, arrangements[i].crossCount,
                                            arrangements[i].verticalNum, j, arrangements[i].component.specification,
                                            arrangements[i].arrangeType, arrangements[i].maxWindPressure))
            arrangements[-1].crossPosition = INF  # 没有横排的时候，横排的位置是没有意义的
    elif arrangements[i].verticalCount == 1 and arrangements[i].crossCount == 1:
        for j in range(2, 31):
            maxCrossNum = 0
            while calculateVerticalWidth(j, arrangements[i].component.width) - maxCrossNum * arrangements[
                i].component.length - (maxCrossNum - 1) * PhotovoltaicPanelCrossMargin > 0:
                maxCrossNum += 1
            arrangements.append(Arrangement(arrangements[i].verticalCount, arrangements[i].crossCount, j,
                                            maxCrossNum, arrangements[i].component.specification,
                                            arrangements[i].arrangeType, arrangements[i].maxWindPressure))
            arrangements[-1].crossPosition = 1
    else:
        for j in range(2, 31):
            maxCrossNum = 0
            while calculateVerticalWidth(j, arrangements[i].component.width) - maxCrossNum * arrangements[
                i].component.length - (maxCrossNum - 1) * PhotovoltaicPanelCrossMargin > 0:
                maxCrossNum += 1
            arrangements.append(Arrangement(arrangements[i].verticalCount, arrangements[i].crossCount, j,
                                            maxCrossNum, arrangements[i].component.specification,
                                            arrangements[i].arrangeType, arrangements[i].maxWindPressure))
        arrangements[-1].crossPosition = arrangements[i].verticalCount - 1
arrangements = arrangements[tempLength:]
# print(len(arrangements))
# print(arrangements)
