import classes.obstacle
import classes.roof
import shadowCalculation

if __name__ == '__main__':
    filePath = 'static/冬至日各纬度下1m长竖直线在地面上投影范围表.xlsx'
    dataDict = shadowCalculation.getDictFromExcel(filePath)
    # 示例参数
    roof = classes.roof.Roof(length=5, width=3, roofAngle=0, roofDirection=0, latitude=0.5)
    roof.print_bool_array()
    obstacle = classes.obstacle.Obstacle(1, 2, 1, 1, 1, 1)
    roof.add_obstacle(obstacle)
    x = 2  # 杆子坐标x
    y = 1  # 杆子坐标y
    length = 1
    latitude = 0.5  # 纬度
    time = 12  # 时间
    roofAngle = 0  # 平面倾斜角度
    roofDirection = "正北"  # 平面倾斜方向

    shadowLength, shadowDirection = shadowCalculation.getShadowEdgeNodes(length, x, y, latitude, time,
                                                                         roofAngle,
                                                                         roofDirection, dataDict)
    print("Shadow Length:", shadowLength, "Shadow Direction:", shadowDirection)
