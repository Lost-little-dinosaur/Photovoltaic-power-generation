import classes.obstacle
import classes.roof
from classes.arrangement import screenArrangements
from classes.component import assignComponentParameters
import json

if __name__ == '__main__':
    with open('input.json', 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
    roof = classes.roof.Roof(length=jsonData["Roof"]["length"], width=jsonData["Roof"]["width"],
                             roofAngle=jsonData["Roof"]["roofAngle"], roofDirection=jsonData["Roof"]["roofDirection"],
                             latitude=jsonData["Roof"]["latitude"])  # 输入的单位是米
    for obstacle in jsonData["Obstacles"]:
        roof.addObstacle(classes.obstacle.Obstacle(obstacle["points"], obstacle["heights"], obstacle["name"]))
    tempObject = {}
    for component in jsonData["Components"]:
        tempObject[component["specification"]] = {"power": component["power"], "thickness": component["thickness"]}
    assignComponentParameters(tempObject)
    screenedArrangements = screenArrangements(roof.width, roof.length, jsonData["SelectedArrangement"]["specification"],
                                              jsonData["SelectedArrangement"]["arrangeType"],
                                              jsonData["SelectedArrangement"]["windPressure"])

    roof.getBestOption(screenedArrangements)  # 计算铺设光伏板的最佳方案

    roof.calculateShadow()

    roof.removeComponentsWithFalseFool()
    roof.renewRects2Array()

    roof.paintBoolArray("plt")  # img库会打开一张图片，更方便观察细节，但稍微慢个几秒钟；plt库不会打开图片，更快，适合批量处理
    # test commit
