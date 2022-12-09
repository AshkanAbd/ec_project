from abc import abstractmethod
import random
import genetic.chromosome as chromosome
import genetic.common as gcommon
from gui.point import Point
import logging
import typing


class Selection:
    _target_points: typing.List[Point] = []

    def setup(self, target_points: typing.List[Point]):
        self._target_points = target_points

    @abstractmethod
    def run(self, chs: typing.List[chromosome.AbstractChromosome]) -> typing.List[chromosome.AbstractChromosome]:
        pass


class AverageFitnessSelection(Selection):
    def __init__(self):
        logging.info('AverageFitness selection initialized')

    def run(self, chs: typing.List[chromosome.AbstractChromosome]) -> typing.List[chromosome.AbstractChromosome]:
        logging.info('Calculating fitness for average fitness selection...')
        fitness_arr = [ch.calc_fitness(self._target_points) for ch in chs]
        fitness_avg = gcommon.arr_avg(fitness_arr)

        new_gen = []
        fitness_arr_len = len(fitness_arr)

        logging.info('Running average fitness selection on current generation...')
        for i in range(fitness_arr_len):
            f = fitness_arr[i]
            target_ch = chs[i]
            int_part = f // fitness_avg

            new_gen += [target_ch for _ in range(int(int_part))]

            if random.random() + int_part <= f / fitness_avg:
                new_gen.append(target_ch)

        if len(new_gen) % 2 != 0:
            new_gen.append(chs[random.randrange(0, fitness_arr_len)])

        logging.info('Selection was successful, middle generation count: %s', len(new_gen))
        return new_gen
