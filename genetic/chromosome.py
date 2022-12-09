from abc import abstractmethod
import genetic.common as gcommon
from gui.point import Point
import typing


class AbstractChromosome:
    _value = None

    @abstractmethod
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    @abstractmethod
    def to_phenotype(self):
        pass

    @abstractmethod
    def calc_fitness(self, points: typing.List[Point]):
        pass


class StrChromosome(AbstractChromosome):
    def __init__(self, value: str):
        super().__init__(value)

    def to_phenotype(self):
        dimension = len(gcommon.GENOME_LEN)
        s_index = 0
        res = []
        for i in range(dimension):
            genome = self._value[s_index: s_index + gcommon.GENOME_LEN[i]]
            s_index = s_index + gcommon.GENOME_LEN[i]
            num = int(genome, 2)
            res.append(
                gcommon.LOWER_BOUND[i] + (
                        num / ((2 ** gcommon.GENOME_LEN[i]) - 1) * (gcommon.UPPER_BOUND[i] - gcommon.LOWER_BOUND[i])
                )
            )

        return Point(res)

    def calc_fitness(self, points: typing.List[Point]):
        return self.to_phenotype().calc_distance_from_others(points)
