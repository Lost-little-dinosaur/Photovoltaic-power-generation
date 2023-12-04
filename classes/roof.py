class Roof:
    def __init__(self, length, width, roofAngle, roofDirection, latitude):
        self.length = length
        self.width = width
        self.roofAngle = roofAngle
        self.roofDirection = roofDirection
        self.latitude = latitude
        self.obstacles = []
        self.bool_array = [[True] * width for _ in range(length)]

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def calculate_area(self):
        area = self.length * self.width
        return area

    def calculate_volume(self, height):
        area = self.calculate_area()
        volume = area * height
        return volume

    def print_bool_array(self):
        for i in range(self.length):
            for j in range(self.width):
                print(0 if self.bool_array[i][j] else 1, end=' ')
            print()
