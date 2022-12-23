from abc import abstractmethod
import random
import genetic.chromosome as chromosome
from genetic.phenotype import Phenotype
import logging
import typing
import math


class Replacement:
    _targets: typing.List[Phenotype] = []
    _genetic = None

    def setup(self, target_points: typing.List[Phenotype], genetic):
        self._targets = target_points
        self._genetic = genetic

    @abstractmethod
    def run(
            self,
            old_gen: typing.List[chromosome.AbstractChromosome],
            mid_gen: typing.List[chromosome.AbstractChromosome],
    ) -> typing.List[chromosome.AbstractChromosome]:
        pass


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
        old_gen_fitness = self._genetic.get_current_gen_fitness()
        mid_gen_fitness = [ch.calc_fitness(self._targets) for ch in mid_gen]
        self._genetic._fitness_counter += mid_gen_len

        new_gen = [x for x in old_gen]
        transferred = set()
        updated = [x for x in range(old_gen_len)]

        copy_count = math.ceil(mid_gen_len / 1 * self._alpha)
        logging.info('Running alpha generational replacement, alpha values is %s(%s)', copy_count, self._alpha)
        for _ in range(copy_count):
            mid_gen_best = -1
            for i in range(0, mid_gen_len):
                if i in transferred:
                    continue

                if mid_gen_best == -1 or mid_gen_fitness[i] < mid_gen_fitness[mid_gen_best]:
                    mid_gen_best = i

            if mid_gen_best == -1:
                break

            transferred.add(mid_gen_best)
            if len(updated) == 0:
                new_gen.append(mid_gen[mid_gen_best])
                continue
            random.shuffle(updated)

            if old_gen_fitness[updated[0]] > mid_gen_fitness[mid_gen_best]:
                new_gen[updated[0]] = mid_gen[mid_gen_best]
            updated = updated[1:]

        logging.info('Replacement was successful, generation len: %s', len(new_gen))
        return new_gen
