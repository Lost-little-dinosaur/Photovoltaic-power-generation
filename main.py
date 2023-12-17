import classes.obstacle
import classes.roof
from const.const import components

if __name__ == '__main__':
    # 示例参数
    roof = classes.roof.Roof(length=15, width=7.5, roofAngle=0, roofDirection=0, latitude=0.5)  # 输入的单位是米
    obstacle = classes.obstacle.Obstacle([[1, 1], [2, 2], [2, 1], [1, 2]], [1, 1, 1, 1], "烟囱")  # 输入的单位是米
    roof.add_obstacle(obstacle)


    roof.getBestOption(components[0])  # 计算铺设光伏板的最佳方案
    roof.calculate_shadow()
    roof.remove_components_with_false_bool(components[0])
    roof.paint_bool_array()

