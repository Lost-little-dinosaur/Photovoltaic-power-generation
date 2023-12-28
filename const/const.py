# 规定一些常量
UNIT = 0.001  # 以米为单位
INF = 1000000000  # 无穷大
roofBoardLength = 5  # 打印屋顶示意图时，额外屋顶边缘的宽度（单位是单元格）
PhotovoltaicPanelBoardLength = 3  # 打印屋顶示意图时，额外屋顶边缘的宽度（单位是单元格）

# 地图中的元素（别删，之后可能会用到！！！）
# Empty = 0  # 空地
# Obstacle = 1  # 障碍物
# Shadow = 2  # 阴影
# PhotovoltaicPanel = 3  # 光伏板
# PhotovoltaicPanelBorder = 6  # 光伏板边框
# PhotovoltaicPanelMargin = 7  # 光伏板边缘
# Margin = 4  # 边缘
# RoofMargin = 5  # 屋顶边缘
# ColorDict = {Empty: (1.0, 1.0, 1.0, 1.0), Obstacle: (0.0, 0.0, 0.0, 1.0),
#              Shadow: (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0),
#              PhotovoltaicPanel: (1.0, 1.0, 0.0, 1.0), Margin: (1.0, 0.0, 0.0, 1.0), RoofMargin: (0.0, 0.0, 0.0, 1.0),
#              PhotovoltaicPanelMargin: (0.43, 0.43, 0.43, 1.0), PhotovoltaicPanelBorder: (0.0, 0.0, 0.0, 1.0)}
Empty = (1.0, 1.0, 1.0, 1.0)  # 空地
Obstacle = (0.0, 0.0, 0.0, 1.0)  # 障碍物
Shadow = (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0)  # 阴影
PhotovoltaicPanel = (1.0, 1.0, 0.0, 1.0)  # 光伏板
Margin = (1.0, 0.0, 0.0, 1.0)  # 边缘
RoofMargin = (0.0, 0.0, 0.0, 1.0)  # 屋顶边缘
PhotovoltaicPanelMargin = (0.43, 0.43, 0.43, 1.0)  # 光伏板边缘
PhotovoltaicPanelBorder = (0.0, 0.0, 0.0, 1.0)  # 光伏板边框

# 光伏板横竖排之间的间距
PhotovoltaicPanelCrossMargin = 0.006  # 以米为单位
PhotovoltaicPanelVerticalMargin = 0.006  # 以米为单位
PhotovoltaicPanelVerticalDiffMargin = 0.012 - PhotovoltaicPanelVerticalMargin  # 以米为单位
