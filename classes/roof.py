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
        max_rect = None  # 当前找到的最大部署数量的矩形位置和大小

        for i in range(self.length - component_length_units + 1):
            for j in range(self.width - component_width_units + 1):
                # 检查当前位置是否都为True，如果不是则跳过
                if not all(
                        self.bool_array[x][y]
                        for x in range(i, i + component_length_units)
                        for y in range(j, j + component_width_units)
                ):
                    continue

                count = 0  # 当前位置的部署数量
                for x in range(i, i + component_length_units):
                    for y in range(j, j + component_width_units):
                        if (
                                x == i
                                or x == i + component_length_units - 1
                                or y == j
                                or y == j + component_width_units - 1
                        ):
                            self.bool_array[x][y] = False
                        else:
                            self.bool_array[x][y] = True
                            count += 1

                if count > max_count:
                    max_count = count
                    max_rect = ((i, j), (i + component_length_units - 1, j + component_width_units - 1))
        return max_rect

    def layoutPillars(self, east_west_span, north_south_span):
        # 将东西跨距和南北跨距转换为以 UNIT 为单位的长度
        east_west_span_units = round(east_west_span / UNIT)
        north_south_span_units = round(north_south_span / UNIT)

        max_spacing = round(2200 / UNIT)  # 最大间距
        max_spacing_multiple = round(50 / UNIT)  # 间距取整的倍数

        max_total_span = round(4000 / UNIT)  # 相邻跨距之和的最大值

        # 初始化立柱坐标列表
        pillar_coordinates = []

        for i in range(self.length):
            for j in range(self.width):
                if self.bool_array[i][j]:
                    # 检查当前位置是否可用
                    # 检查南北跨距是否超出边界
                    if i + north_south_span_units > self.length:
                        continue

                    # 检查东西跨距是否超出边界
                    if j + east_west_span_units > self.width:
                        continue

                    # 检查当前位置及相邻位置之间的间距是否满足要求
                    valid = True
                    for x in range(i, i + north_south_span_units):
                        for y in range(j, j + east_west_span_units):
                            if not self.bool_array[x][y]:
                                valid = False
                                break
                        if not valid:
                            break

                    if not valid:
                        continue

                    # 检查相邻东西跨距之和是否超过最大值
                    if j > 0:
                        total_span = east_west_span_units + 1
                        if total_span > max_total_span:
                            continue

                    # 检查相邻东西跨距之和是否超过最大值
                    if j + east_west_span_units < self.width - 1:
                        total_span = east_west_span_units + 1
                        if total_span > max_total_span:
                            continue

                    # 检查立柱之间的间距是否超过最大值
                    if len(pillar_coordinates) > 0:
                        last_x, last_y = pillar_coordinates[-1]
                        spacing = abs(i - last_x) + abs(j - last_y)
                        if spacing > max_spacing:
                            continue

                        # 检查立柱之间的间距是否为整数倍
                        if spacing % max_spacing_multiple != 0:
                            continue

                    # 将当前位置及相邻位置置为不可用（False）
                    for x in range(i, i + north_south_span_units):
                        for y in range(j, j + east_west_span_units):
                            self.bool_array[x][y] = False

                    # 将当前立柱坐标添加到列表中
                    pillar_coordinates.append((i, j))

                    # 每个组件至少需要一个立柱
                    return pillar_coordinates

        return None  # 如果无法找到合适的位置布置立柱，则返回 None

