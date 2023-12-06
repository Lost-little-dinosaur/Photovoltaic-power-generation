from const.const import UNIT


class Obstacle:
    def __init__(self, edges, edgesHeight, ID):
        try:
            assert len(edges) == len(edgesHeight)
        except AssertionError:
            print("棱边数组和棱边高度数组长度不一致，edges长度为", len(edges), "edgesHeight长度为", len(edgesHeight))
            return
        self.edges = [[i / UNIT for i in j] for j in edges]  # 棱边数组
        self.edgesHeight = [i / UNIT for i in edgesHeight]  # 棱边高度数组
        self.ID = ID



# shadow_length = self.height / np.tan(np.radians(sun_angle))
# shadow_x = self.x + shadow_length * np.cos(np.radians(sun_angle))
# shadow_y = self.y + shadow_length * np.sin(np.radians(sun_angle))
# shadow_width = self.width
#
# shadow = {
#     'x': shadow_x,
#     'y': shadow_y,
#     'length': shadow_length,
#     'width': shadow_width
# }
#
# return shadow
