import math
import typing
from genetic.phenotype import Phenotype


class Point(Phenotype):
    def __init__(self, dimensions: typing.List, color=None) -> None:
        self.dimensions = []
        if type(dimensions) is list:
            for d in dimensions:
                self.dimensions.append(d)
        elif type(dimensions) is int or type(dimensions) is float:
            self.dimensions.append(dimensions)
        self.color = color

    def __str__(self) -> str:
        res = ''
        for d in self.dimensions:
            res += '-' + str(d)

        if self.color is not None:
            res += '-' + str(self.color[0][0]) + str(self.color[0][1]) + str(self.color[0][2])

        return res[1:]

    def get_dimension(self) -> int:
        return len(self.dimensions)

    def to_arr(self) -> typing.List[float]:
        return self.dimensions

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
