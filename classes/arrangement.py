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
        self.value = self.component.maximumPower * (
                self.verticalCount * self.verticalNum + self.crossCount * self.crossNum)  # todo: 以组件功率最大值计算每个arrangement的价值
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
        if self.verticalCount == 0:  # 只有横排布（横一）
            for i in range(self.crossNum):
                cp = Component(self.component.specification, self.component.width, self.component.length,
                               self.component.minimumPower, self.component.maximumPower, self.component.minThickness,
                               self.component.maxThickness)
                cp.startX = startX
                cp.startY = startY
                cp.direction = 2
                cp.endX = startX + self.component.length
                cp.endY = startY + self.component.width
                self.componentArray.append(cp)
                startX += self.component.width + PhotovoltaicPanelCrossMargin   # 横横间隙
        elif self.crossCount == 0:  # 只有竖排
            for i in range(self.verticalCount):
                for j in range(self.verticalNum):
                    cp = Component(self.component.specification, self.component.width, self.component.length,
                                   self.component.minimumPower, self.component.maximumPower,
                                   self.component.minThickness,
                                   self.component.maxThickness)
                    cp.startX = startX
                    cp.startY = startY
                    cp.direction = 1
                    cp.endX = startX + self.component.width
                    cp.endY = startY + self.component.length
                    self.componentArray.append(cp)
                    startX += self.component.width + PhotovoltaicPanelCrossMargin
                startX -= (self.component.width + PhotovoltaicPanelCrossMargin) * self.verticalNum
                startY += self.component.length + PhotovoltaicPanelVerticalMargin
        elif self.verticalCount == 1 and self.crossCount == 1:  # 竖一横一
            for i in range(self.verticalNum):
                cp = Component(self.component.specification, self.component.width, self.component.length,
                               self.component.minimumPower, self.component.maximumPower, self.component.minThickness,
                               self.component.maxThickness)
                cp.startX = startX
                cp.startY = startY
                cp.direction = 1
                cp.endX = startX + self.component.width
                cp.endY = startY + self.component.length
                self.componentArray.append(cp)
                startX += self.component.width + PhotovoltaicPanelCrossMargin
            startX = startX + self.component.width
            startY = startY + self.component.width + PhotovoltaicPanelVerticalDiffMargin
            for i in range(self.crossNum):
                cp = Component(self.component.specification, self.component.width, self.component.length,
                               self.component.minimumPower, self.component.maximumPower, self.component.minThickness,
                               self.component.maxThickness)
                cp.startY = startY
                cp.startX = startX - self.component.length
                cp.direction = 2
                cp.endX = startX
                cp.endY = startY + self.component.width
                self.componentArray.append(cp)
                startX -= self.component.length + PhotovoltaicPanelCrossMargin
        else:  # 其他横竖情况
            for i in range(self.verticalCount - 1):
                for j in range(self.verticalNum):
                    cp = Component(self.component.specification, self.component.width, self.component.length,
                                   self.component.minimumPower, self.component.maximumPower, self.component.minThickness,
                                   self.component.maxThickness)
                    cp.startX = startX
                    cp.startY = startY
                    cp.direction = 1
                    cp.endX = (startX + self.component.width)
                    cp.endY = (startY + self.component.length)
                    self.componentArray.append(cp)
                    startX += (self.component.width + PhotovoltaicPanelCrossMargin)
                startX -= (self.component.width + PhotovoltaicPanelCrossMargin) * self.verticalNum
                startY += (self.component.length + PhotovoltaicPanelVerticalMargin)
            startY += (self.component.width + PhotovoltaicPanelVerticalDiffMargin * 2 - PhotovoltaicPanelVerticalMargin)
            for i in range(self.verticalNum):  # 最后一排
                cp = Component(self.component.specification, self.component.width, self.component.length,
                               self.component.minimumPower, self.component.maximumPower, self.component.minThickness,
                               self.component.maxThickness)
                cp.startX = startX
                cp.startY = startY
                cp.direction = 1
                cp.endX = startX + self.component.width
                cp.endY = startY + self.component.length
                self.componentArray.append(cp)
                startX += (self.component.width + PhotovoltaicPanelCrossMargin)

            startX -= PhotovoltaicPanelCrossMargin
            startY -= (self.component.width - PhotovoltaicPanelVerticalDiffMargin)

            for i in range(self.crossNum):
                cp = Component(self.component.specification, self.component.width, self.component.length,
                               self.component.minimumPower, self.component.maximumPower, self.component.minThickness,
                               self.component.maxThickness)
                cp.startY = startY
                cp.startX = startX - self.component.length
                cp.direction = 2
                cp.endX = startX
                cp.endY = startY + self.component.width
                self.componentArray.append(cp)
                startX -= self.component.length + PhotovoltaicPanelCrossMargin
        return self.componentArray


        # if self.verticalCount == 2 and self.crossCount == 0:  # 竖二
        #    for i in range(2):
        #        for j in range(self.num):
        #            self.componentArray.append(Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35,
        #                                                 startX, startY, startX + 1.134, startY + 2.279, 1, i))
        #            startX += round((self.component.width + 0.006) / UNIT)
        #    startX -= round((self.component.width + 0.006) * self.num / UNIT)
        #    startY += round((self.component.length + 0.012) / UNIT)
        # if self.verticalCount == 4 and self.crossCount == 1:  # 竖四横一
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
        # return self.componentArray

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


def calculateCrossWidth(crossNum, componentLength):
    return crossNum * componentLength + (crossNum - 1) * PhotovoltaicPanelCrossMargin


def screenArrangements(arrangementArray, roofWidth, roofLength, componentSpecification, arrangeType, windPressure):
    # 通过输入的屋顶宽度、屋顶长度、组件类型、排布类型和风压，筛选出合适的排布
    result = []
    for arrangement in arrangementArray:
        if arrangement.width <= roofWidth and arrangement.length <= roofLength and arrangement.component.specification == componentSpecification and arrangement.arrangeType == arrangeType and arrangement.maxWindPressure + 0.00001 >= windPressure:
            result.append(arrangement)
        # if arrangement.width <= roofWidth and arrangement.length <= roofLength:
        #     if arrangement.component.specification == componentSpecification:
        #         if arrangement.arrangeType == arrangeType:
        #             if arrangement.maxWindPressure + 0.00001 >= windPressure:
        #                 result.append(arrangement)
        #             else:
        #                 print("风压不符合，要求风压为", windPressure, "实际风压为", arrangement.maxWindPressure)
        #         else:
        #             print("排布类型不符合，要求排布类型为", arrangeType, "实际排布类型为", arrangement.arrangeType)
        #     else:
        #         print("组件类型不符合，要求组件类型为", componentSpecification, "实际组件类型为",
        #               arrangement.component.specification)
        # else:
        #     print("排布尺寸不符合，要求排布尺寸为", roofWidth, roofLength, "实际排布尺寸为", arrangement.width,
        #           arrangement.length)

    return result


# component1 = Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35)  # 以米、瓦为单位
# component2 = Component("182-78", 1.134, 2.465, 580, 600, 0.30, 0.35)  # 以米、瓦为单位
# component3 = Component("210-60", 1.303, 2.172, 595, 605, 0.33, 0.35)  # 以米、瓦为单位
# component4 = Component("210-66", 1.303, 2.384, 650, 665, 0.33, 0.35)  # 以米、瓦为单位
# components = [component1, component2, component3, component4]
# 组件排布的规格
# verticalCount, crossCount, verticalNum, crossNum, component, arrangeType, maxWindPressure
tempArrangements = []
tempArrangements.append(Arrangement(1, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(1, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(2, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(2, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(3, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(3, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(4, 0, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(4, 1, INF, INF, "182-78", "膨胀常规", 1.2614))
tempArrangements.append(Arrangement(5, 0, INF, INF, "182-78", "膨胀常规", 1.2614))

tempArrangements.append(Arrangement(1, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(1, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(0, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(2, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(2, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(3, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(4, 1, INF, INF, "210-60", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(5, 0, INF, INF, "210-60", "膨胀常规", 0.9785))

tempArrangements.append(Arrangement(0, 1, INF, INF, "210-60", "基墩", 0.9785))
tempArrangements.append(Arrangement(2, 0, INF, INF, "210-60", "基墩", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "210-60", "基墩", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "210-60", "基墩", 0.9785))
tempArrangements.append(Arrangement(1, 0, INF, INF, "210-60", "基墩", 0.9785))

tempArrangements.append(Arrangement(2, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(2, 1, INF, INF, "210-60", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(3, 1, INF, INF, "210-60", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(4, 1, INF, INF, "210-60", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(5, 0, INF, INF, "210-60", "膨胀抬高", 0.9785))

tempArrangements.append(Arrangement(0, 1, INF, INF, "182-72", "基墩", 0.9785))
tempArrangements.append(Arrangement(2, 0, INF, INF, "182-72", "基墩", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "182-72", "基墩", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "182-72", "基墩", 0.9785))
tempArrangements.append(Arrangement(1, 0, INF, INF, "182-72", "基墩", 0.9785))

tempArrangements.append(Arrangement(1, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(1, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(0, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(2, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(2, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(3, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(4, 1, INF, INF, "182-72", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(5, 0, INF, INF, "182-72", "膨胀常规", 0.9785))

tempArrangements.append(Arrangement(2, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(2, 1, INF, INF, "182-72", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(3, 1, INF, INF, "182-72", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(4, 1, INF, INF, "182-72", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(5, 0, INF, INF, "182-72", "膨胀抬高", 0.9785))

tempArrangements.append(Arrangement(1, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(1, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(0, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(2, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(2, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(3, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(4, 1, INF, INF, "182-78", "膨胀常规", 0.9785))
tempArrangements.append(Arrangement(5, 0, INF, INF, "182-78", "膨胀常规", 0.9785))

tempArrangements.append(Arrangement(0, 1, INF, INF, "182-78", "基墩", 0.9785))
tempArrangements.append(Arrangement(2, 0, INF, INF, "182-78", "基墩", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "182-78", "基墩", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "182-78", "基墩", 0.9785))
tempArrangements.append(Arrangement(1, 0, INF, INF, "182-78", "基墩", 0.9785))

tempArrangements.append(Arrangement(2, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(2, 1, INF, INF, "182-78", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(3, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(3, 1, INF, INF, "182-78", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(4, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(4, 1, INF, INF, "182-78", "膨胀抬高", 0.9785))
tempArrangements.append(Arrangement(5, 0, INF, INF, "182-78", "膨胀抬高", 0.9785))

tempLength = len(tempArrangements)
for i in range(tempLength):
    if tempArrangements[i].crossCount == 0:
        for j in range(2, 31):
            tempArrangements.append(Arrangement(tempArrangements[i].verticalCount, 0, j, tempArrangements[i].crossNum,
                                                tempArrangements[i].component.specification,
                                                tempArrangements[i].arrangeType,
                                                tempArrangements[i].maxWindPressure))
            tempArrangements[-1].crossPosition = INF  # 没有竖排的时候，横排的位置是没有意义的
    elif tempArrangements[i].verticalCount == 0:
        for j in range(1, 16):
            tempArrangements.append(Arrangement(0, tempArrangements[i].crossCount, tempArrangements[i].verticalNum, j,
                                                tempArrangements[i].component.specification,
                                                tempArrangements[i].arrangeType,
                                                tempArrangements[i].maxWindPressure))
            tempArrangements[-1].crossPosition = INF  # 没有横排的时候，横排的位置是没有意义的
    else:
        minVerticalNum = 2
        while calculateVerticalWidth(minVerticalNum, tempArrangements[i].component.width) <= tempArrangements[
            i].component.length:
            minVerticalNum += 1
        for j in range(minVerticalNum, 31):
            maxCrossNum = 0
            while calculateVerticalWidth(j, tempArrangements[i].component.width) > \
                    calculateCrossWidth(maxCrossNum, tempArrangements[i].component.length):
                maxCrossNum += 1
            maxCrossNum -= 1
            tempArrangements.append(Arrangement(tempArrangements[i].verticalCount, tempArrangements[i].crossCount, j,
                                                maxCrossNum, tempArrangements[i].component.specification,
                                                tempArrangements[i].arrangeType, tempArrangements[i].maxWindPressure))
            if tempArrangements[i].verticalCount == 1:
                tempArrangements[-1].crossPosition = 1
            else:
                tempArrangements[-1].crossPosition = tempArrangements[i].verticalCount - 1
tempArrangements = tempArrangements[tempLength:]
# 去重
tempArrangements.sort(key=lambda x: (x.verticalCount, x.verticalNum, x.crossCount, x.crossNum), reverse=True)
arrangements = [tempArrangements[0]]
for i in range(1, len(tempArrangements)):
    if arrangements[-1].verticalCount == tempArrangements[i].verticalCount and arrangements[-1].verticalNum == \
            tempArrangements[i].verticalNum and arrangements[-1].crossCount == tempArrangements[i].crossCount and \
            arrangements[-1].crossNum == tempArrangements[i].crossNum:
        continue
    else:
        arrangements.append(tempArrangements[i])
        # if arrangements[-1].component.specification == "182-72" and arrangements[-1].arrangeType == "膨胀常规" \
        #         and arrangements[-1].maxWindPressure == 0.9785:
        #     print(arrangements[-1].verticalCount, arrangements[-1].verticalNum, arrangements[-1].crossCount,
        #           arrangements[-1].crossNum, "hhh")

# i = 0
# while i < len(tempArrangements) - 1:
#     if tempArrangements[i].verticalCount == tempArrangements[i + 1].verticalCount and tempArrangements[
#         i].verticalNum == tempArrangements[i + 1].verticalNum and tempArrangements[i].crossCount == tempArrangements[
#         i + 1].crossCount and tempArrangements[i].crossNum == tempArrangements[i + 1].crossNum:
#         del tempArrangements[i]
#     else:
#         i += 1
# print(len(tempArrangements))
# print(tempArrangements)
