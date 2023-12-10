import numpy as np

from const.const import UNIT, INF
from getData import dataDict, convertStrDirectionToDegrees
from hullCalculation import getConvexHull, isPointInsideConvexHull
from math import *


class Roof:
    def __init__(self, length, width, roofAngle, roofDirection, latitude):  # 输入的length和width是以米为单位的
        self.length = round(length / UNIT)
        self.width = round(width / UNIT)
        self.roofAngle = roofAngle
        self.roofDirection = roofDirection
        self.latitude = latitude
        self.obstacles = []
        self.bool_array = [[True] * self.width for _ in range(self.length)]

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
        # for i in range(self.length):
        #     for j in range(self.width):
        #         print(0 if self.bool_array[i][j] else 1, end=' ')
        #     print()
        from matplotlib import pyplot as plt
        # 将布尔数组转换为黑白颜色（True为白色，False为黑色）
        image = np.where(self.bool_array, 1, 0)

        # 显示图像
        plt.imshow(image, cmap='gray')
        plt.axis('off')  # 不显示坐标轴
        plt.show()
        plt.show()

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
        for eachObstacle in self.obstacles:
            allEdgeNodes = []
            for i in range(len(eachObstacle.edges)):
                allEdgeNodes.append(eachObstacle.edges[i])
                allEdgeNodes.extend(self.getShadowEdgeNodes(eachObstacle.edges[i], eachObstacle.edgesHeight[i]))

            # 使用Graham扫描法找出allEdgeNodes的凸包
            hullPoints = getConvexHull(allEdgeNodes)
            # # 画出这些点看看
            # from matplotlib import pyplot as plt
            # plt.scatter([i[0] for i in allEdgeNodes], [i[1] for i in allEdgeNodes])
            # # 将凸包点标红
            # plt.scatter([i[0] for i in hullPoints], [i[1] for i in hullPoints], c='r')
            # plt.show()
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

            for x1 in range(round(minX), round(maxX) + 1):
                for y1 in range(round(minY), round(maxY) + 1):
                    self.bool_array[x1][y1] = not isPointInsideConvexHull(hullPoints, x1, y1)

    def getBestOption(self, component_length, component_width):
        component_length_units = round(component_length / UNIT)
        component_width_units = round(component_width / UNIT)

        max_count = 0  # 当前找到的最大部署数量
        max_rects = []  # 当前找到的最大部署数量的矩形位置和大小

        for i in range(self.length - component_length_units + 1):
            for j in range(self.width - component_width_units + 1):
                count = 0  # 当前位置的部署数量
                for x in range(i, i + component_length_units):
                    for y in range(j, j + component_width_units):
                        if self.bool_array[x][y]:
                            count += 1

                if count > max_count:
                    max_count = count
                    max_rects = [((i, j), (i + component_length_units - 1, j + component_width_units - 1))]
                elif count == max_count:
                    max_rects.append(((i, j), (i + component_length_units - 1, j + component_width_units - 1)))

        # 将最大部署数量的矩形位置设置为False
        for rect in max_rects:
            start, end = rect
            for i in range(start[0], end[0] + 1):
                for j in range(start[1], end[1] + 1):
                    self.bool_array[i][j] = False

        return max_rects
