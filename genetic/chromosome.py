from abc import abstractmethod
from genetic.phenotype import Phenotype
from gui.point import Point
import typing
import config


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
    def calc_fitness(self, points: typing.List[Phenotype]):
        pass


class StrChromosome(AbstractChromosome):
    def __init__(self, value: typing.Union[str, int]):
        if type(value) == int:
            res = ''
            while value > 0:
                res += str(int(value % 2))
                value = value // 2

            while len(res) != config.CHROMOSOME_LENGTH:
                res += '0'

            value = res

        super().__init__(value)

    def to_phenotype(self):
        dimension = len(config.GENOME_LEN)
        s_index = 0
        res = []
        for i in range(dimension):
            genome = self._value[s_index: s_index + config.GENOME_LEN[i]]
            s_index = s_index + config.GENOME_LEN[i]
            num = int(genome, 2)
            res.append(
                config.LOWER_BOUND[i] + (
                        num / ((2 ** config.GENOME_LEN[i]) - 1) * (config.UPPER_BOUND[i] - config.LOWER_BOUND[i])
                )
            )

        return Point(res)

    def calc_fitness(self, points: typing.List[Phenotype]):
        return self.to_phenotype().calc_distance_from_others(points)
