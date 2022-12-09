from abc import abstractmethod
import random
import genetic.chromosome as chromosome
from gui.point import Point
import logging
import typing
import math


class Replacement:
    _target_points: typing.List[Point] = []
    _preserved: chromosome.AbstractChromosome = None

    def setup(self, target_points: typing.List[Point]):
        self._target_points = target_points

    @abstractmethod
    def run(
            self,
            old_gen: typing.List[chromosome.AbstractChromosome],
            mid_gen: typing.List[chromosome.AbstractChromosome],
    ) -> typing.List[chromosome.AbstractChromosome]:
        pass

    def get_preserved(self):
        return self._preserved


class AlphaGenerationalReplacement(Replacement):
    _alpha: float

    def __init__(self, alpha: float):
        logging.info('Initializing alpha generational replacement...')
        if alpha <= 0 or alpha > 1:
            logging.error('Alpha should be in (0, 1] range.')
            logging.warning('Update alpha from %s to 0.5', alpha)
            alpha = 0.5

        self._alpha = alpha

    def run(
            self,
            old_gen: typing.List[chromosome.AbstractChromosome],
            mid_gen: typing.List[chromosome.AbstractChromosome],
    ) -> typing.List[chromosome.AbstractChromosome]:
        old_gen_len = len(old_gen)
        mid_gen_len = len(mid_gen)

        logging.info('Calculating fitness for alpha generational replacement...')
        old_gen_fitness = [ch.calc_fitness(self._target_points) for ch in old_gen]
        mid_gen_fitness = [ch.calc_fitness(self._target_points) for ch in mid_gen]

        self._update_preserved(old_gen, old_gen_fitness)

        new_gen = [x for x in old_gen]
        transferred = set()

        copy_count = math.ceil(mid_gen_len / 100 * self._alpha)
        logging.info('Running alpha generational replacement, alpha values is %s', copy_count)
        for _ in range(copy_count):
            mid_gen_best = -1
            for i in range(0, mid_gen_len):
                if i in transferred:
                    continue

                if mid_gen_best == -1 or mid_gen_fitness[i] > mid_gen_fitness[mid_gen_best]:
                    mid_gen_best = i

            if mid_gen_best == -1:
                break

            transferred.add(mid_gen_best)
            new_gen[random.randrange(0, old_gen_len)] = mid_gen[mid_gen_best]

        logging.info('Replacement was successful, new generation len: %s', len(new_gen))
        return new_gen

    def _update_preserved(
            self,
            old_gen: typing.List[chromosome.AbstractChromosome],
            old_gen_fitness: typing.List[float],
    ):
        logging.info('Looking for new best chromosome...')
        old_gen_len = len(old_gen)
        old_gen_best = 0
        for i in range(1, old_gen_len):
            if old_gen_fitness[i] > old_gen_fitness[old_gen_best]:
                old_gen_best = i

        if self._preserved is None or self._preserved.calc_fitness(self._target_points) < old_gen[old_gen_best]:
            self._preserved = old_gen[old_gen_best]
            logging.info('Updating best chromosome to %s.', self._preserved)
