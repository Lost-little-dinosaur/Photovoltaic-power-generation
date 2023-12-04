import numpy as np
from math import *
import shadowCalculation
from matplotlib.path import Path


def getConvexHull(allEdgeNodes):
    # 定义一些辅助函数
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def square_distance(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    # 找到最低点
    start = min(allEdgeNodes, key=lambda p: (p[1], p[0]))

    # 对点进行排序
    sorted_points = sorted(allEdgeNodes,
                           key=lambda p: (atan2(p[1] - start[1], p[0] - start[0]), square_distance(start, p)))

    # 构建凸包
    hull = []
    for p in sorted_points:
        while len(hull) >= 2 and cross_product(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull


def isPointInsideConvexHull(hullPoints, x1, y1):
    n = len(hullPoints)
    if n < 3:
        return False

    # 将点与凸包上的两点相连，形成一条射线
    count = 0
    for i in range(n):
        x2, y2 = hullPoints[i]
        x3, y3 = hullPoints[(i + 1) % n]
        # 检查射线是否与边相交
        if ((y2 > y1) != (y3 > y1)) and (x1 < (x3 - x2) * (y1 - y2) / (y3 - y2) + x2):
            count += 1

    # 如果与奇数条边相交，则点在凸包内
    return count % 2 == 1


class Obstacle:
    def __init__(self, height, edges, edgesHeight, length, width, ID):
        self.height = height
        self.edges = edges  # 棱边数组
        self.edgesHeight = edgesHeight  # 棱边高度数组
        assert len(edges) == len(edgesHeight)
        self.length = length
        self.width = width
        self.ID = ID

    def calculate_shadow(self, roof):
        allEdgeNodes = []
        for i in range(len(self.edges)):
            allEdgeNodes.append(self.edges[i])
            allEdgeNodes.extend(shadowCalculation.getShadowEdgeNodes(self.edges[i], self.edgesHeight[i], roof))

        # 使用Graham扫描法找出allEdgeNodes的凸包
        hullPoints = getConvexHull(allEdgeNodes)

        sorted(hullPoints, key=lambda p: p[0])
        minX = hullPoints[0][0]
        maxX = hullPoints[-1][0]
        sorted(hullPoints, key=lambda p: p[1])
        minY = hullPoints[0][1]
        maxY = hullPoints[-1][1]

        for x1 in range(minX, maxX + 1):
            for y1 in range(minY, maxY + 1):
                roof.bool_array[x1][y1] = not isPointInsideConvexHull(hullPoints, x1, y1)

# shadow_length = self.height / np.tan(np.radians(sun_angle))
# shadow_x = self.x + shadow_length * np.cos(np.radians(sun_angle))
# shadow_y = self.y + shadow_length * np.sin(np.radians(sun_angle))
# shadow_width = self.width
#
# shadow = {
#     'x': shadow_x,
#     'y': shadow_y,
#     'length': shadow_length,
#     'width': shadow_width
# }
#
# return shadow
