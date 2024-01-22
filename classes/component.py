from const.const import INF, UNIT


class Component:
    def __init__(self, specification, width, length, verticalspacing, verticalshortsidesize, crossspacing, crossshortsidesize, power=INF, thickness=INF, statX=INF, statY=INF, endX=INF, endY=INF,
                 direction=INF, marginRight=INF, marginBottom=INF):
        self.specification = specification
        # 将width和length转换成以UNIT为单位
        self.width = round(width / UNIT)
        self.length = round(length / UNIT)
        self.power = power
        self.thickness = thickness
        self.startX = statX
        self.startY = statY
        self.endX = endX
        self.endY = endY
        self.direction = direction  # 1表示纵向，2表示横向
        self.marginRight = marginRight  # 该矩形右边的间距（只记录每个矩形下边的间距和右边的间距）
        self.marginBottom = marginBottom  # 该矩形下边的间距（只记录每个矩形下边的间距和右边的间距）
        self.verticalspacing = round(verticalspacing / UNIT)  # 横梁间距（竖排放）
        self.verticalshortsidesize = round(verticalshortsidesize / UNIT)  # 横梁离短边距离（竖排放）
        self.crossspacing = round(crossspacing / UNIT)  # 横梁间距（横排放）
        self.crossshortsidesize = round(crossshortsidesize / UNIT)  # 横梁离短边距离（横排放）



def assignComponentParameters(parameterDict):
    global components
    for component in components:
        component.power = parameterDict[component.specification]["power"]
        component.thickness = parameterDict[component.specification]["thickness"]


# 光伏板的规格
component1 = Component("182-72", 1.134, 2.279, 1.400, 0.439, 1.108, 0.013)  # 以米、瓦为单位
component2 = Component("182-78", 1.134, 2.465, 1.500, 0.4825, 1.108, 0.013)  # 以米、瓦为单位
component3 = Component("210-60", 1.303, 2.172, 1.400, 0.386, 1.277, 0.013)  # 以米、瓦为单位
component4 = Component("210-66", 1.303, 2.384, 1.400, 0.492, 0, 0)  # 以米、瓦为单位
components = [component1, component2, component3, component4]

