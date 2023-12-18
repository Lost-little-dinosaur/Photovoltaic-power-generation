import numpy as np
import time
import matplotlib.pyplot as plt
from const.const import *
from getData import dataDict
from hullCalculation import getConvexHull, isPointInsideConvexHull
from math import tan, radians, cos, sin, sqrt


class Roof:
    def __init__(self, length, width, roofAngle, roofDirection, latitude):  # 输入的length和width是以米为单位的
        time1 = time.time()
        self.length = round(length / UNIT)
        self.width = round(width / UNIT)
        self.roofAngle = roofAngle
        self.roofDirection = roofDirection
        self.latitude = latitude
        self.obstacles = []
        self.bool_array = np.full((self.length, self.width), True)
        # 构造差分数组
        # self.bool_array_diff = np.full((self.length, self.width), 0)
        # self.bool_array_diff[0, 0] = 1
        # 利用numpy快速构造前缀和数组
        self.bool_array_sum = np.cumsum(np.cumsum(self.bool_array, axis=0), axis=1)
        self.show_array = np.full((self.length, self.width), Empty)
        self.maxrects_array = []
        print("屋顶初始化完成，耗时", time.time() - time1, "秒\n")

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def calculate_area(self):
        area = self.length * self.width
        return area

    def calculate_volume(self, height):
        area = self.calculate_area()
        volume = area * height
        return volume

    def paint_bool_array(self):
        time1 = time.time()
        tempArr = np.pad(self.show_array, ((roofBoardLength, roofBoardLength), (roofBoardLength, roofBoardLength)),
                         'constant',
                         constant_values=RoofMargin)
        rgb_array = np.array([[ColorDict[value] for value in row] for row in tempArr])
        plt.imshow(rgb_array)
        plt.axis('off')  # Turn off axis
        plt.show()
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

    def calculate_shadow(self):
        self.bool_array = np.full((self.length, self.width), True)
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
                    self.bool_array[x1, y1] = not isPointInsideConvexHull(hullPoints, x1, y1)
                    # self.bool_array_diff[x1, y1] = int(self.bool_array[x1, y1]) - int(self.bool_array[x1, y1 - 1]) - \
                    #                                int(self.bool_array[x1 - 1, y1]) + int(
                    #     self.bool_array[x1 - 1, y1 - 1])  # 根据bool_array修改差分数组bool_array_diff
                    self.show_array[x1, y1] = Empty if self.bool_array[x1, y1] else Shadow
        # numpy优化
        self.bool_array_sum = np.cumsum(np.cumsum(self.bool_array.astype(int), axis=0), axis=1)
        print("阴影计算完成，耗时", time.time() - time1, "秒\n")

    def getBestOption(self, component):
        time1 = time.time()
        print("正在计算最佳方案...当前时间为", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        component_length_units = round(component.length / UNIT)
        component_width_units = round(component.width / UNIT)

        max_count = 0
        max_rects = []

        def updateMaxRects(mY, mX, Len, Wid, maxRects, maxCount):
            new_rect = ((mY - Len + 1, mX - Wid + 1), (mY, mX))

            def overlaps(rect1, rect2):  # 可能有问题
                (start1, end1), (start2, end2) = rect1, rect2
                return not (end1[0] < start2[0] or end1[1] < start2[1] or end2[0] < start1[0] or end2[1] < start1[
                    1])

            if not any(overlaps(existing_rect, new_rect) for existing_rect in maxRects):
                maxRects.append(new_rect)
                maxCount += 1
            return maxCount

        def renewJ(y, x, maxRects):
            for s, e in maxRects:
                if s[0] <= y <= e[0] and s[1] <= x <= e[1]:
                    return e[1] - x + 1
            return 1

        # 检查两种放置方式
        for length, width in [(component_length_units, component_width_units),
                              (component_width_units, component_length_units)]:  # todo: 反过来会怎么样？
            i = length - 1
            while i < self.length:
                j = width - 1
                while j < self.width:
                    if self.canPlaceRectangle(i, j, length, width):
                        max_count = updateMaxRects(i, j, length, width, max_rects, max_count)
                        j += width - 1
                    j += renewJ(i - length + 1, j - width + 1, max_rects)  # 快速更新j（非常重要！！！）
                i += 1
        self.maxrects_array = max_rects
        print("最佳方案计算完成，耗时", time.time() - time1, "秒，最多可以放置", max_count,
              "块光伏板" + "，光伏组件规格为", component.specification, "，当前精度为", UNIT, "米\n")
        return max_rects
        '''
       for rect in max_rects:
           start, end = rect  # todo: 还需要考虑一下万一PhotovoltaicPanelBoardLength超过了start和end的范围的情况
           self.show_array[start[0]:end[0] + 1,
           start[1]:start[1] + PhotovoltaicPanelBoardLength] = PhotovoltaicPanelMargin
           self.show_array[start[0]:end[0] + 1,
           end[1] - PhotovoltaicPanelBoardLength + 1:end[1] + 1] = PhotovoltaicPanelMargin
           self.show_array[start[0]:start[0] + PhotovoltaicPanelBoardLength,
           start[1]:end[1] + 1] = PhotovoltaicPanelMargin
           self.show_array[end[0] - PhotovoltaicPanelBoardLength + 1:end[0] + 1,
           start[1]:end[1] + 1] = PhotovoltaicPanelMargin
           self.show_array[start[0] + PhotovoltaicPanelBoardLength:end[0] - PhotovoltaicPanelBoardLength + 1,
           start[1] + PhotovoltaicPanelBoardLength:end[1] - PhotovoltaicPanelBoardLength + 1] = PhotovoltaicPanel
           self.bool_array[start[0]:end[0] + 1, start[1]:end[1] + 1] = False  # todo: 可以用差分数组优化（其实感觉没必要了）
        '''


    def canPlaceRectangle(self, i, j, length, width):
        # 前缀和数组优化
        if i > length - 1 and j > width - 1:
            if self.bool_array_sum[i, j] - self.bool_array_sum[i - length, j] - self.bool_array_sum[i, j - width] + \
                    self.bool_array_sum[i - length, j - width] != length * width:
                return False
        elif i == length - 1 and j > width - 1:
            if self.bool_array_sum[i, j] - self.bool_array_sum[i, j - width] != length * width:
                return False
        elif i > length - 1 and j == width - 1:
            if self.bool_array_sum[i, j] - self.bool_array_sum[i - length, j] != length * width:
                return False
        else:
            if self.bool_array_sum[i, j] != length * width:
                return False
        return True
    def remove_components_with_false_bool(self, component):
        component_length_units = round(component.length / UNIT)
        component_width_units = round(component.width / UNIT)
        # 创建一个新的列表用于存储要保留的元素
        updated_rects = []
        for rect in self.maxrects_array:
            (start_x, start_y), (end_x, end_y) = rect
            if self.canPlaceRectangle(end_x, end_y, component_length_units, component_width_units):# todo: 还要再考虑竖着的情况
                updated_rects.append(rect)  # 将没有 False 值的 rect 添加到新列表中
        self.maxrects_array = updated_rects  # 更新 Maxrects 列表为新列表
        print("已移除所有位置中被阴影遮挡的组件，一共还有" + str(len(self.maxrects_array)) + "个组件")
        for rect in self.maxrects_array:
            start, end = rect  # todo: 还需要考虑一下万一PhotovoltaicPanelBoardLength超过了start和end的范围的情况
            self.show_array[start[0]:end[0] + 1,
            start[1]:start[1] + PhotovoltaicPanelBoardLength] = PhotovoltaicPanelMargin
            self.show_array[start[0]:end[0] + 1,
            end[1] - PhotovoltaicPanelBoardLength + 1:end[1] + 1] = PhotovoltaicPanelMargin
            self.show_array[start[0]:start[0] + PhotovoltaicPanelBoardLength,
            start[1]:end[1] + 1] = PhotovoltaicPanelMargin
            self.show_array[end[0] - PhotovoltaicPanelBoardLength + 1:end[0] + 1,
            start[1]:end[1] + 1] = PhotovoltaicPanelMargin
            self.show_array[start[0] + PhotovoltaicPanelBoardLength:end[0] - PhotovoltaicPanelBoardLength + 1,
            start[1] + PhotovoltaicPanelBoardLength:end[1] - PhotovoltaicPanelBoardLength + 1] = PhotovoltaicPanel



