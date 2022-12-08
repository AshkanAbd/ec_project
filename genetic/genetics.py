import math
from abc import abstractmethod
import genetic.common as gcommon
# from genetic.common import point_to_chromosome, chromosome_to_point, is_calibrated, calibrate, reset, CHROMOSOME_LENGTH, \
#     calc_chromosome
from gui.point import Point
import random
import time
import typing


class AbstractGeneticAlgorithm:
    @abstractmethod
    def set_target_points(self, points: typing.List[Point]):
        pass

    @abstractmethod
    def genotype_to_phenotype(self) -> typing.List[Point]:
        pass

    @abstractmethod
    def generate_initial_population(self):
        pass


class GeneticAlgorithm(AbstractGeneticAlgorithm):
    target_points: typing.List[str] = []
    current_generation: typing.List[str] = []

    def __init__(self):
        gcommon.reset()

    def set_target_points(self, points: typing.List[Point]):
        if not gcommon.is_calibrated():
            gcommon.calibrate(points)

        self.target_points = [gcommon.point_to_chromosome(p) for p in points]

    def genotype_to_phenotype(self) -> typing.List[Point]:
        return [gcommon.chromosome_to_point(ch, color=[[0, 1, 0]]) for ch in self.current_generation]

    def generate_initial_population(self):
        initial_count = math.ceil(1.65 * pow(2, 0.21 * gcommon.CHROMOSOME_LENGTH))
        random.seed(time.time())
        self.current_generation = []

        for _ in range(initial_count):
            chromosome_num = random.randrange(0, 2 ** gcommon.CHROMOSOME_LENGTH)
            self.current_generation.append(gcommon.calc_chromosome(chromosome_num))
