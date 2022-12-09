import math
import typing


class Point:
    def __init__(self, x, y: float = None, z: float = None, color=None) -> None:
        self.y = None
        self.z = None
        if type(x) is list:
            dimension = len(x)
            if dimension >= 1:
                self.x = x[0]
            if dimension >= 2:
                self.y = x[1]
            if dimension >= 3:
                self.z = x[2]
        elif type(x) is int or type(x) is float:
            self.x = x
            self.y = y
            self.z = z
        self.color = color

    def __str__(self) -> str:
        res = str(self.x)

        if self.y is not None:
            res += '-' + str(self.y)

        if self.z is not None:
            res += '-' + str(self.z)

        return res

    def get_dimension(self) -> int:
        dimension = 1

        if self.y is not None:
            dimension += 1

        if self.z is not None:
            dimension += 1

        return dimension

    def to_arr(self) -> typing.List[float]:
        res = [self.x]

        if self.y is not None:
            res.append(self.y)

        if self.z is not None:
            res.append(self.z)

        return res

    def calc_distance(self, point) -> float:
        res = 0
        dimension = self.get_dimension()
        self_arr = self.to_arr()
        point_arr = point.to_arr()

        for i in range(dimension):
            res += (self_arr[i] - point_arr[i]) ** 2

        return math.sqrt(res)

    def calc_distance_from_others(self, points) -> float:
        res = 0
        dimension = self.get_dimension()
        self_arr = self.to_arr()

        for i in range(dimension):
            tmp = 0
            for p in points:
                tmp += (p.to_arr()[i] - self_arr[i]) ** 2

            res += math.sqrt(tmp)

        return res

    def set_color(self, color):
        self.color = color
