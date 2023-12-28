from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
from const.const import *
from getData import dataDict
from hullCalculation import getConvexHull, isPointInsideConvexHull
from math import tan, radians, cos, sin, sqrt
from classes.component import Component


class Roof:
    def __init__(self, length, width, roofAngle, roofDirection, latitude):  # 输入的length和width是以米为单位的
        time1 = time.time()
        self.length = round(length / UNIT)
        self.width = round(width / UNIT)
        self.roofAngle = roofAngle
        self.roofDirection = roofDirection
        self.latitude = latitude
        self.obstacles = []
        self.boolArray = np.full((self.length, self.width), True)
        # 构造差分数组
        # self.bool_array_diff = np.full((self.length, self.width), 0)
        # self.bool_array_diff[0, 0] = 1
        # 利用numpy快速构造前缀和数组
        self.boolArraySum = np.cumsum(np.cumsum(self.boolArray, axis=0), axis=1)
        self.showArray = np.full((self.length, self.width, 4), Empty)
        self.maxRects = []
        print("屋顶初始化完成，耗时", time.time() - time1, "秒\n")

    def addObstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def paintBoolArray(self, lib):
        time1 = time.time()
        # 额外加上roofBoardLength的屋顶边缘（不要删，留着备用！！！）
        # tempArr = np.pad(self.showArray, ((roofBoardLength, roofBoardLength), (roofBoardLength, roofBoardLength),
        #                                   (0, 0)), 'constant', constant_values=RoofMargin)
        # rgb_array = np.array([[ColorDict[value] for value in row] for row in tempArr])
        height, width, channels = self.showArray.shape
        tempArr = np.zeros((height + 2 * roofBoardLength, width + 2 * roofBoardLength, channels))
        # 设置边界值
        for i in range(channels):
            tempArr[:, :, i] = RoofMargin[i]
        # 填充中间区域
        tempArr[roofBoardLength:-roofBoardLength, roofBoardLength:-roofBoardLength, :] = self.showArray
        if lib == "plt":
            plt.imshow(tempArr)
            plt.axis('off')
            plt.show()
        elif lib == "img":
            img = Image.fromarray((tempArr * 255).astype(np.uint8))
            img.show()
        else:
            raise Exception("lib参数错误: ", lib)
        print("屋顶排布示意图绘制完成，耗时", time.time() - time1, "秒\n")

    def getShadowEdgeNodes(self, edgeNode, edgeNodeHeight):
        returnList = []
        # 检查纬度是否在字典中
        if self.latitude in dataDict:
            for k, v in dataDict[self.latitude].items():
                # 获取阴影长度和方向
                shadowLength, shadowDirection = v
                shadowLength /= 1000  # 将单位转换为米，只有在这里计算的时候用到的是米，其他都是UNIT

                # 计算阴影方向和平面倾斜方向之间的角度差
                angleDiff = abs(shadowDirection - self.roofDirection) % 360
                # 角度差超过180度时，取其补角
                if angleDiff > 180:
                    angleDiff = 360 - angleDiff
                if angleDiff <= 90:
                    adjustedLength = edgeNodeHeight * shadowLength / (
                            1 - shadowLength * tan(radians(self.roofAngle)) * cos(radians(angleDiff))) * sqrt(
                        tan(radians(self.roofAngle)) ** 2 * cos(radians(angleDiff)) ** 2 + 1)
                else:
                    angleDiff = 180 - angleDiff
                    adjustedLength = edgeNodeHeight * shadowLength / (
                            1 + shadowLength * tan(radians(self.roofAngle)) * cos(radians(angleDiff))) * sqrt(
                        tan(radians(self.roofAngle)) ** 2 * cos(radians(angleDiff)) ** 2 + 1)
                returnList.append([edgeNode[0] + adjustedLength * cos(radians(shadowDirection)),
                                   edgeNode[1] + adjustedLength * sin(radians(shadowDirection))])  # 这里先不取整
        else:
            if self.latitude not in dataDict:
                print("纬度 ", self.latitude, " 不在字典中")
        return returnList

    def calculateShadow(self):
        self.boolArray = np.full((self.length, self.width), True)
        time1 = time.time()
        print("正在计算阴影，当前时间为", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for eachObstacle in self.obstacles:
            allEdgeNodes = []
            for i in range(len(eachObstacle.edges)):
                allEdgeNodes.append(eachObstacle.edges[i])
                allEdgeNodes.extend(self.getShadowEdgeNodes(eachObstacle.edges[i], eachObstacle.edgesHeight[i]))

            # 使用Graham扫描法找出allEdgeNodes的凸包
            hullPoints = getConvexHull(allEdgeNodes)
            maxX, minX, maxY, minY = 0, INF, 0, INF
            for eachPoint in hullPoints:
                maxX = max(maxX, eachPoint[0])
                minX = min(minX, eachPoint[0])
                maxY = max(maxY, eachPoint[1])
                minY = min(minY, eachPoint[1])
            minX = max(0, minX)
            minY = max(0, minY)
            maxX = min(self.length - 1, maxX)
            maxY = min(self.width - 1, maxY)

            for x1 in range(round(minX), round(maxX) + 1):  # todo: 时间太长了，需要优化！
                for y1 in range(round(minY), round(maxY) + 1):
                    self.boolArray[x1, y1] = not isPointInsideConvexHull(hullPoints, x1, y1)
                    # self.bool_array_diff[x1, y1] = int(self.bool_array[x1, y1]) - int(self.bool_array[x1, y1 - 1]) - \
                    #                                int(self.bool_array[x1 - 1, y1]) + int(
                    #     self.bool_array[x1 - 1, y1 - 1])  # 根据bool_array修改差分数组bool_array_diff
                    self.showArray[x1, y1] = Empty if self.boolArray[x1, y1] else Shadow
        # numpy优化
        self.boolArraySum = np.cumsum(np.cumsum(self.boolArray.astype(int), axis=0), axis=1)
        print("阴影计算完成，耗时", time.time() - time1, "秒\n")

    def getBestOption(self, arrangements):
        time1 = time.time()
        print("正在计算最佳方案...当前时间为", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        def updateMaxRects(arrange, mY, mX, Len, Wid, maxRects, max_count, now_y, direct):  # 用于竖排放置方式的更新
            newRect = Component("tmp", INF, INF, INF, INF, INF, INF, mX - Wid + 1, mY - Len + 1, mX, mY, direct,
                                round(PhotovoltaicPanelCrossMargin / UNIT),
                                round(PhotovoltaicPanelVerticalMargin / UNIT))  # 先假装是一个组件，方便排布

            def overlaps(rect1, rect2):
                return not (
                        rect1.endX < rect2.startX or rect1.endY < rect2.startY or rect2.endX < rect1.startX or rect2.endY < rect1.startY)

            if not any(overlaps(existingRect, newRect) for existingRect in maxRects):
                arrange.calculateComponentArray(newRect.startX, newRect.startY)
                maxRects.extend(arrange.componentArray)
                max_count += 1
                return max_count, mY, True
            else:
                return max_count, now_y, False

        def renewJ(y, x, maxRects):
            for r in maxRects:
                if r.startY <= y <= r.endY and r.startX <= x <= r.endX:
                    return r.endX - x + 1
            return 1

        # 先对arrangements按不同关键字排序，verticalCount从大到小，crossCount从大到小
        arrangements.sort(key=lambda x: (x.verticalCount, x.crossCount), reverse=True)
        maxCount = 0
        self.maxRects = []
        for k in range(len(arrangements)):
            print("正在计算第", k + 1, "/", len(arrangements), "个组件的最佳方案，当前时间为",
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # if k == 29:
            #     break
            component_length_units = round(arrangements[k].length / UNIT)
            component_width_units = round(arrangements[k].width / UNIT)
            # if component_length_units < component_width_units:  # 确保length大于width（不需要额外判断了）
            #     component_length_units, component_width_units = component_width_units, component_length_units
            direction, length, width = 1, component_length_units, component_width_units
            i, nowY = length - 1, -INF
            if length > self.length or width > self.width:
                continue
            while i < self.length:
                j = width - 1
                while j < self.width:
                    if self.canPlaceRectangle(i, j, length, width):
                        maxCount, nowY, addFlag = updateMaxRects(arrangements[k], i, j, length, width, self.maxRects,
                                                                 maxCount, nowY, direction)
                        # 更新光伏板之间的间距（在最后利用maxRects一起更新bool数组和show数组）
                        if addFlag:
                            j += width - 2
                    j += renewJ(i - length + 1, j - width + 1, self.maxRects)  # 快速更新j（非常重要！！！）
                i += 1

        print("最佳方案计算完成，耗时", time.time() - time1, "秒，最多可以放置", maxCount, "块光伏板" + "，当前精度为",
              UNIT, "米\n")
        return self.maxRects

    def canPlaceRectangle(self, i, j, length, width):
        # 前缀和数组优化
        if i > length - 1 and j > width - 1:
            if self.boolArraySum[i, j] - self.boolArraySum[i - length, j] - self.boolArraySum[i, j - width] + \
                    self.boolArraySum[i - length, j - width] != length * width:
                return False
        elif i == length - 1 and j > width - 1:
            if self.boolArraySum[i, j] - self.boolArraySum[i, j - width] != length * width:
                return False
        elif i > length - 1 and j == width - 1:
            if self.boolArraySum[i, j] - self.boolArraySum[i - length, j] != length * width:
                return False
        else:
            if self.boolArraySum[i, j] != length * width:
                return False
        return True

    # def removeComponentsWithFalseFool(self):
    #     # 创建一个新的列表用于存储要保留的元素
    #     updated_rects = []
    #     for rect in self.maxRects:
    #         if self.canPlaceRectangle(rect.endY, rect.endX, rect.endY - rect.startY + 1, rect.endX - rect.startX + 1):
    #             updated_rects.append(rect)
    #     self.maxRects = updated_rects  # 更新 maxRects 列表为新列表

    def renewRects2Array(self):
        time1 = time.time()
        for rect1 in self.maxRects:  # todo: 还需要考虑一下万一PhotovoltaicPanelBoardLength超过了start和end的范围的情况
            self.boolArray[rect1.startY:rect1.endY + 1, rect1.startX:rect1.endX + 1] = False
            # 修边
            rect1.marginRight, rect1.marginBottom, = round(PhotovoltaicPanelCrossMargin / UNIT), round(
                PhotovoltaicPanelVerticalMargin / UNIT)

        for rect1 in self.maxRects:
            # 修边
            if rect1.direction == 1:
                for rect2 in self.maxRects:
                    if rect2.direction == 2:
                        # 如果rect1下方+round(PhotovoltaicPanelVerticalDiffMargin / UNIT)+1的位置有rect2，那么rect1的下边距就要加上这个间距
                        tempY = rect1.endY + rect1.marginBottom + round(PhotovoltaicPanelVerticalDiffMargin / UNIT) + 1
                        for tempX in range(rect1.startX, rect1.endX + 1):
                            if rect2.startX <= tempX <= rect2.endX and rect2.startY <= tempY <= rect2.endY:
                                rect1.marginBottom += round(PhotovoltaicPanelVerticalDiffMargin / UNIT)
                                break
            else:
                for rect2 in self.maxRects:
                    if rect2.direction == 1:
                        # 如果rect1下方+round(PhotovoltaicPanelVerticalDiffMargin / UNIT)+1的位置有rect2，那么rect1的下边距就要加上这个间距
                        tempY = rect1.endY + rect1.marginBottom + round(PhotovoltaicPanelVerticalDiffMargin / UNIT) + 1
                        for tempX in range(rect1.startX, rect1.endX + 1):
                            if rect2.startX <= tempX <= rect2.endX and rect2.startY <= tempY <= rect2.endY:
                                rect1.marginBottom += round(PhotovoltaicPanelVerticalDiffMargin / UNIT)
                                break

            if rect1.marginRight + rect1.endX + 1 < self.width and np.sum(
                    self.boolArray[rect1.startY:rect1.endY + 1, rect1.endX + rect1.marginRight + 1:
                    rect1.endX + rect1.marginRight + 2]) == rect1.endY - rect1.startY + 1:
                rect1.marginRight = 0
            if rect1.marginBottom + rect1.endY + 1 < self.length and np.sum(
                    self.boolArray[rect1.endY + rect1.marginBottom + 1:rect1.endY + rect1.marginBottom + 2,
                    rect1.startX:rect1.endX + 1]) == rect1.endX - rect1.startX + 1:
                rect1.marginBottom = 0

            self.showArray[rect1.startY:rect1.endY + 1,
            rect1.startX:rect1.startX + PhotovoltaicPanelBoardLength] = PhotovoltaicPanelBorder
            self.showArray[rect1.startY:rect1.endY + 1,
            rect1.endX - PhotovoltaicPanelBoardLength + 1:rect1.endX + 1] = PhotovoltaicPanelBorder
            self.showArray[rect1.startY:rect1.startY + PhotovoltaicPanelBoardLength,
            rect1.startX + PhotovoltaicPanelBoardLength:rect1.endX - PhotovoltaicPanelBoardLength + 1] = PhotovoltaicPanelBorder
            self.showArray[rect1.endY - PhotovoltaicPanelBoardLength + 1:rect1.endY + 1,
            rect1.startX + PhotovoltaicPanelBoardLength:rect1.endX - PhotovoltaicPanelBoardLength + 1] = PhotovoltaicPanelBorder
            self.showArray[rect1.startY + PhotovoltaicPanelBoardLength:rect1.endY - PhotovoltaicPanelBoardLength + 1,
            rect1.startX + PhotovoltaicPanelBoardLength:rect1.endX - PhotovoltaicPanelBoardLength + 1] = PhotovoltaicPanel

            self.showArray[rect1.endY + 1:rect1.endY + rect1.marginBottom + 1,
            rect1.startX:rect1.endX + rect1.marginRight + 1] = PhotovoltaicPanelMargin
            self.showArray[rect1.startY:rect1.endY + 1,
            rect1.endX + 1:rect1.endX + rect1.marginRight + 1] = PhotovoltaicPanelMargin

            # 再次更新bool_array
            self.boolArray[rect1.startY:rect1.endY + rect1.marginBottom + 1,
            rect1.startX:rect1.endX + rect1.marginRight + 1] = False

        print("已更新show_array和bool_array，耗时", time.time() - time1, "秒\n")

# 单个组件的排布函数（留着备用！！！）
#     def getBestOption(self, component):
#         time1 = time.time()
#         print("正在计算最佳方案...当前时间为", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#         component_length_units = round(component.length / UNIT)
#         component_width_units = round(component.width / UNIT)
#         if component_length_units < component_width_units:  # 确保length大于width
#             component_length_units, component_width_units = component_width_units, component_length_units
#
#         maxCount = 0
#         self.maxRects = []
#
#         def updateMaxRects1(mY, mX, Len, Wid, maxRects, max_count, now_row, now_y, direct):  # 用于竖排放置方式的更新
#             newRect = Rectangle(mY - Len + 1, mX - Wid + 1, mY, mX, direct, now_row,
#                                 round(PhotovoltaicPanelCrossMargin / UNIT),
#                                 round(PhotovoltaicPanelVerticalMargin / UNIT))
#
#             def overlaps(rect1, rect2):
#                 return not (
#                         rect1.endX + rect1.marginRight < rect2.startX or rect1.endY + rect1.marginBottom <
#                         rect2.startY or rect2.endX + rect2.marginRight < rect1.startX or rect2.endY +
#                         rect2.marginBottom < rect1.startY)
#
#             if not any(overlaps(existing_rect, newRect) for existing_rect in maxRects):
#                 maxRects.append(newRect)
#                 max_count += 1
#                 if now_y != mY and now_y != -INF:
#                     now_row += 1
#                 return max_count, now_row, mY, True
#             else:
#                 return max_count, now_row, now_y, False
#
#         def updateMaxRects2(mY, mX, Len, Wid, maxRects, max_count, now_row, now_y, direct):  # 用于竖排放置方式的更新
#             newRect = Rectangle(mY - Len + 1, mX - Wid + 1, mY, mX, direct, now_row,
#                                 round(PhotovoltaicPanelCrossMargin / UNIT),
#                                 round(PhotovoltaicPanelVerticalMargin / UNIT))
#
#             def overlaps(rect1, rect2):
#                 if rect1.direction != rect2.direction:
#                     return not (
#                             rect1.endX + rect1.marginRight < rect2.startX or rect1.endY + rect1.marginBottom +
#                             round(PhotovoltaicPanelVerticalDiffMargin / UNIT) < rect2.startY or rect2.endX + rect2.
#                             marginRight < rect1.startX or rect2.endY + rect2.marginBottom +
#                             round(PhotovoltaicPanelVerticalDiffMargin / UNIT) < rect1.startY)
#                 else:
#                     return not (
#                             rect1.endX + rect1.marginRight < rect2.startX or rect1.endY + rect1.marginBottom <
#                             rect2.startY or rect2.endX + rect2.marginRight < rect1.startX or rect2.endY +
#                             rect2.marginBottom < rect1.startY)
#
#             if not any(overlaps(existingRect, newRect) for existingRect in maxRects):
#                 maxRects.append(newRect)
#                 max_count += 1
#                 if now_y != mY and now_y != -INF:
#                     now_row += 1
#                 return max_count, now_row, mY, True
#             else:
#                 return max_count, now_row, now_y, False
#
#         def renewJ(y, x, maxRects):
#             for r in maxRects:
#                 if r.startY <= y <= r.endY and r.startX <= x <= r.endX:
#                     return r.endX - x + 1
#             return 1
#
#         # 先检查竖排放置方式
#         addFlag = False
#         direction, length, width = 1, component_length_units, component_width_units
#         i, nowRow, nowY = length - 1, 1, -INF
#         while i < self.length:
#             j = width - 1
#             while j < self.width:
#                 if self.canPlaceRectangle(i, j, length, width):
#                     maxCount, nowRow, nowY, addFlag = updateMaxRects1(i, j, length, width, self.maxRects, maxCount,
#                                                                       nowRow, nowY, direction)
#                     # 更新光伏板之间的间距（在最后利用maxRects一起更新bool数组和show数组）
#                     if addFlag:
#                         j += width - 2 + round(PhotovoltaicPanelCrossMargin / UNIT)
#                 j += renewJ(i - length + 1, j - width + 1, self.maxRects)  # 快速更新j（非常重要！！！）
#             if not addFlag:
#                 i += 1
#             else:
#                 i += round(PhotovoltaicPanelVerticalMargin / UNIT) + 1
#                 addFlag = False
#         # 再检查横排放置方式（只能放一行）
#         addFlag = False
#         direction, length, width = 2, component_width_units, component_length_units
#         i, nowRow, nowY = length - 1, 1, -INF
#         while i < self.length:
#             j = width - 1
#             while j < self.width:
#                 if self.canPlaceRectangle(i, j, length, width):
#                     maxCount, nowRow, nowY, addFlag = updateMaxRects2(i, j, length, width, self.maxRects, maxCount,
#                                                                       nowRow, nowY, direction)
#                     if nowRow == 2:  # 只能放一行横排
#                         break
#                     # 更新光伏板之间的间距（在最后利用maxRects一起更新bool数组和show数组）
#                     if addFlag:
#                         j += width - 2 + round(PhotovoltaicPanelCrossMargin / UNIT)
#                 j += renewJ(i - length + 1, j - width + 1, self.maxRects)
#             if nowRow == 2:  # 只能放一行横排
#                 break
#             if not addFlag:
#                 i += 1
#             else:
#                 i += round(PhotovoltaicPanelVerticalMargin / UNIT) + 1
#                 addFlag = False
#
#         print("最佳方案计算完成，耗时", time.time() - time1, "秒，最多可以放置", maxCount,
#               "块光伏板" + "，光伏组件规格为", component.specification, "，当前精度为", UNIT, "米\n")
#         return self.maxRects
