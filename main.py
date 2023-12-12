import classes.obstacle
import classes.roof
import getData

if __name__ == '__main__':
    # 示例参数
    roof = classes.roof.Roof(length=15, width=7.5, roofAngle=0, roofDirection=0, latitude=0.5)  # 输入的单位是米
    # roof.print_bool_array()
    obstacle = classes.obstacle.Obstacle([[1, 1], [2, 2], [2, 1], [1, 2]], [1, 1, 1, 1], "烟囱")  # 输入的单位是米
    roof.add_obstacle(obstacle)

    roof.calculate_shadow()
    roof.paint_bool_array()
    print(roof.getBestOption(1.134, 2.279))  # 计算铺设光伏板的最佳方案
    roof.paint_bool_array()
    roof.layoutPillars(0.2, 0.3)
    roof.paint_bool_array()