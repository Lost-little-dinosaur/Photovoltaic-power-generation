from classes.component import Component

# 规定一些常量
UNIT = 0.1  # 以米为单位
INF = 1000000000  # 无穷大
roofBoard = 1  # 打印屋顶示意图时，额外屋顶边缘的宽度

# 光伏板的规格
component1 = Component("182-72", 1.134, 2.279, 535, 550, 0.30, 0.35)  # 以米、瓦为单位
component2 = Component("182-78", 1.134, 2.465, 580, 600, 0.30, 0.35)  # 以米、瓦为单位
component3 = Component("210-60", 1.303, 2.172, 595, 605, 0.33, 0.35)  # 以米、瓦为单位
component4 = Component("210-66", 1.303, 2.384, 650, 665, 0.33, 0.35)  # 以米、瓦为单位
components = [component1, component2, component3, component4]
