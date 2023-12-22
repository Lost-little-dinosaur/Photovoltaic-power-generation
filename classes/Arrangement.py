from const.const import components


class Arrangement:
    def __init__(self, specification, component, width, length, type):
        self.specification = specification
        self.component = component
        self.type = type
        self.width = width
        self.length = length
        self.array_x = []
        self.array_y = []

    def chooselayout(self):
        if self.specification == "竖二" and self.type == "基墩":
            array_x = [107, 1707, 3307]
            array_y = [459, 1859, 2706, 4135]

        elif self.specification == "竖四横一" and self.type == "基墩":
            array_x = [417, 2417, 4417, 6417, 6834]
            array_y = [458, 1858, 2725, 4143, 5016, 6428, 6849, 8007, 8465, 9865]
        else:
            layout = "Default Layout"

        return array_x, array_y




