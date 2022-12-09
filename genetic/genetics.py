import math
from abc import abstractmethod
import genetic.common as gcommon
from gui.point import Point
import random
import time
import typing
import genetic.chromosome as chromosome


class AbstractGeneticAlgorithm:
    _current_generation: typing.List[chromosome.AbstractChromosome] = []
    _generation_counter = 0

    def _increase_generation_counter(self):
        self._generation_counter += 1

    def get_generation_counter(self) -> int:
        return self._generation_counter

    @abstractmethod
    def set_target_points(self, points: typing.List[Point]):
        pass

    @abstractmethod
    def genotype_to_phenotype(self) -> typing.List[Point]:
        pass

    @abstractmethod
    def generate_initial_population(self):
        pass

    @abstractmethod
    def check_end_condition(self) -> typing.Union[typing.Tuple[bool, Point], typing.Tuple[bool, None]]:
        pass

    @abstractmethod
    def selection_op(self):
        pass

    @abstractmethod
    def crossover_op(self):
        pass

    @abstractmethod
    def mutation_op(self):
        pass


class GeneticAlgorithm(AbstractGeneticAlgorithm):
    target_points: typing.List[Point] = []

    def __init__(self):
        gcommon.reset()

    def set_target_points(self, points: typing.List[Point]):
        if not gcommon.is_calibrated():
            gcommon.calibrate(points)

        self.target_points = points

    def genotype_to_phenotype(self) -> typing.List[Point]:
        return [ch.to_phenotype() for ch in self._current_generation]

    def generate_initial_population(self):
        initial_count = math.ceil(1.65 * pow(2, 0.21 * gcommon.CHROMOSOME_LENGTH))
        random.seed(time.time())
        self._current_generation = []

        for _ in range(initial_count):
            chromosome_num = random.randrange(0, 2 ** gcommon.CHROMOSOME_LENGTH)
            self._current_generation.append(
                chromosome.StrChromosome(gcommon.calc_chromosome(chromosome_num))
            )

    def check_end_condition(self) -> typing.Union[typing.Tuple[bool, Point], typing.Tuple[bool, None]]:
        for ch in self._current_generation:
            res = None
            flag = True
            ch_phenotype = ch.to_phenotype()
            for target in self.target_points:
                if res is None:
                    res = target.calc_distance(ch_phenotype)
                else:
                    if math.fabs(res - target.calc_distance(ch_phenotype)) > 0.0000001:
                        flag = False
                        break

            if flag:
                return True, ch_phenotype

        return False, None

    def selection_op(self):
        fitness_arr = [ch.calc_fitness(self.target_points) for ch in self._current_generation]

        avg_fitness = gcommon.arr_avg(fitness_arr)

        pass

    def crossover_op(self):
        pass

    def mutation_op(self):
        pass
