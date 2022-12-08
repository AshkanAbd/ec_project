from abc import abstractmethod
from genetic.common import point_to_chromosome, chromosome_to_point, is_calibrated, calibrate, reset
from gui.point import Point
import typing


class AbstractGeneticAlgorithm:
    @abstractmethod
    def phenotype_to_genotype(self, points: typing.List[Point]):
        pass

    @abstractmethod
    def genotype_to_phenotype(self) -> typing.List[Point]:
        pass


class GeneticAlgorithm(AbstractGeneticAlgorithm):
    current_generation: typing.List[str] = []

    def __init__(self):
        reset()

    def phenotype_to_genotype(self, points: typing.List[Point]):
        if not is_calibrated():
            calibrate(points)

        self.current_generation = [point_to_chromosome(p) for p in points]
        print(self.current_generation)

    def genotype_to_phenotype(self) -> typing.List[Point]:
        return [chromosome_to_point(ch) for ch in self.current_generation]
