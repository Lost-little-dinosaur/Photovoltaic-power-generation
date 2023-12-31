import classes.obstacle
import classes.roof
from classes.arrangement import arrangements, screenArrangements

if __name__ == '__main__':
    # 示例参数
    roof = classes.roof.Roof(length=15, width=7.5, roofAngle=0, roofDirection=0, latitude=0.5)  # 输入的单位是米
    obstacle = classes.obstacle.Obstacle([[1, 1], [2, 2], [2, 1], [1, 2]], [1, 1, 1, 1], "烟囱")  # 输入的单位是米
    roof.addObstacle(obstacle)
    screenedArrangements = screenArrangements(arrangements, roof.width, roof.length, "182-72", "膨胀常规", 0.9785)

    roof.calculateShadow()

    roof.getBestOption(screenedArrangements)  # 计算铺设光伏板的最佳方案

    roof.renewRects2Array()
    roof.paintBoolArray("plt")  # img库会打开一张图片，更方便观察细节，但稍微慢个几秒钟；plt库不会打开图片，更快，适合批量处理
