from math import *

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
