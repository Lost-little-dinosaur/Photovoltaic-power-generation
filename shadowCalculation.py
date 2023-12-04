from math import *
import pandas as pd
import sympy as sp


def convertStrDirectionToDegrees(direction):
    if direction == "正北":
        return 270.0
    elif direction == "正东":
        return 0.0
    elif direction == "正南":
        return 90.0
    elif direction == "正西":
        return 180.0
    elif direction.startswith("西偏北"):
        return 180.0 + float(direction.replace("西偏北", "").replace("°", ""))
    elif direction.startswith("北偏西"):
        return 270.0 - float(direction.replace("北偏西", "").replace("°", ""))
    elif direction.startswith("北偏东"):
        return 270.0 + float(direction.replace("北偏东", "").replace("°", ""))
    elif direction.startswith("东偏北"):
        return 360 - float(direction.replace("东偏北", "").replace("°", ""))
    elif direction.startswith("东偏南"):
        return float(direction.replace("东偏南", "").replace("°", ""))
    elif direction.startswith("南偏东"):
        return 90.0 - float(direction.replace("南偏东", "").replace("°", ""))
    elif direction.startswith("南偏西"):
        return 90.0 + float(direction.replace("南偏西", "").replace("°", ""))
    elif direction.startswith("西偏南"):
        return 180.0 - float(direction.replace("西偏南", "").replace("°", ""))
    else:
        return None


def getDictFromExcel(excelPath):
    df = pd.read_excel(excelPath, skiprows=[0])

    # 初始化字典
    resultDict = {}

    latitude = None  # 用于记录当前的坐标纬度
    timeList = []  # 用于存储时间
    shadowLengthList = []  # 用于存储影子长度
    shadowAngleList = []  # 用于存储影子朝向

    # 遍历数据并构建字典
    for index, row in df.iterrows():
        if pd.notna(row['坐标纬度']):  # 如果当前行有坐标纬度数据
            if latitude is not None:  # 如果latitude已经被赋值
                # 将时间、影子长度和影子朝向数据存入字典
                resultDict[latitude] = {}
                for i in range(len(timeList)):
                    resultDict[latitude][timeList[i]] = [shadowLengthList[i], shadowAngleList[i]]

            # 更新坐标纬度和清空时间、影子长度和影子朝向列表
            latitude = float(row['坐标纬度'])
            timeList = []
            shadowLengthList = []
            shadowAngleList = []

        # 存储时间、影子长度和影子朝向数据
        timeList.append(row['时间'].hour)
        shadowLengthList.append(row['影子长度mm'])
        shadowAngleList.append(convertStrDirectionToDegrees(row['影子朝向']))

    # 将最后一个坐标纬度的数据存入字典
    if latitude is not None:
        resultDict[latitude] = {}
        for i in range(len(timeList)):
            resultDict[latitude][timeList[i]] = [shadowLengthList[i], shadowAngleList[i]]

    return resultDict


filePath = 'E:\shadowcal\冬至日各纬度下1m长竖直线在地面上投影范围表.xlsx'
dataDict = getDictFromExcel(filePath)


def getShadowEdgeNodes(edgeNode, edgeNodeHeight, roof):
    returnList = []
    # 检查纬度是否在字典中
    if roof.latitude in dataDict:
        for k, v in dataDict[roof.latitude].items():
            # 获取阴影长度和方向
            shadowLength, shadowDirection = v

            # 转换平面倾斜方向为度数
            roofDirectionDegree = convertStrDirectionToDegrees(roof.roofDirection)

            # 计算阴影方向和平面倾斜方向之间的角度差
            angleDiff = abs(shadowDirection - roofDirectionDegree) % 360
            # 角度差超过180度时，取其补角
            if angleDiff > 180:
                angleDiff = 360 - angleDiff
            if angleDiff < 90:
                adjustedLength = edgeNodeHeight * shadowLength / (
                        1 - shadowLength * tan(radians(roof.roofAngle)) * cos(radians(angleDiff))) * sqrt(
                    tan(radians(angleDiff)) ** 2 * cos(radians(roof.roofAngle)) ** 2 + 1)
            else:
                angleDiff = 180 - angleDiff
                adjustedLength = edgeNodeHeight * shadowLength / (
                        1 + shadowLength * tan(radians(roof.roofAngle)) * cos(radians(angleDiff))) * sqrt(
                    tan(radians(angleDiff)) ** 2 * cos(radians(roof.roofAngle)) ** 2 + 1)
            returnList.append([round(edgeNode[0] + adjustedLength * cos(radians(shadowDirection))),
                               round(edgeNode[1] + adjustedLength * sin(radians(shadowDirection)))])  # 暂时以四舍五入的方法取整
    else:
        if roof.latitude not in dataDict:
            print("纬度 ", roof.latitude, " 不在字典中")
    return returnList

# 示例使用
# if __name__ == '__main__':
#     filePath = 'E:\shadowcal\冬至日各纬度下1m长竖直线在地面上投影范围表.xlsx'
#     dataDict = getDictFromExcel(filePath)
#     # # 示例参数
#     x = 5  # 杆子坐标x
#     y = 10  # 杆子坐标y
#     length = 4 * 3 ** 0.5 - 4
#     latitude = 0.5  # 纬度
#     time = 12  # 时间
#     roofAngle = 45  # 平面倾斜角度
#     roofDirection = "正北"  # 平面倾斜方向
#
#     shadowLength, shadowDirection = calculateShadowOnInclinedPlane(length, x, y, latitude, time, roofAngle,
#                                                                    roofDirection, dataDict)
#     print("Shadow Length:", shadowLength, "Shadow Direction:", shadowDirection)
