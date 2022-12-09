import math
from abc import abstractmethod
import genetic.common as gcommon
from gui.point import Point
import random
import time
import typing
import genetic.chromosome as chromosome
import genetic.op.crossover as crossover
import genetic.op.mutation as mutation
import genetic.op.selection as selection
import genetic.op.replacement as replacement
import config
import logging


class AbstractGeneticAlgorithm:
    _current_generation: typing.List[chromosome.AbstractChromosome] = []
    _middle_generation: typing.List[chromosome.AbstractChromosome] = []
    _generation_counter = 0
    _selection_op: selection.Selection
    _crossover_op: crossover.Crossover
    _mutation_op: mutation.Mutation
    _replacement_op: replacement.Replacement
    _preserved: chromosome.AbstractChromosome = None

    def __init__(
            self,
            selection_op: selection.Selection,
            crossover_op: crossover.Crossover,
            mutation_op: mutation.Mutation,
            replacement_op: replacement.Replacement,
    ):
        self._selection_op = selection_op
        self._crossover_op = crossover_op
        self._mutation_op = mutation_op
        self._replacement_op = replacement_op

    def increase_generation_counter(self):
        self._generation_counter += 1

    def get_generation_counter(self) -> int:
        return self._generation_counter

    @abstractmethod
    def set_target_points(self, points: typing.List[Point]):
        pass

    @abstractmethod
    def current_generation_to_phenotype(self) -> typing.List[Point]:
        pass

    @abstractmethod
    def middle_generation_to_phenotype(self) -> typing.List[Point]:
        pass

    @abstractmethod
    def generate_initial_population(self):
        pass

    @abstractmethod
    def check_end_condition(self) -> typing.Union[typing.Tuple[bool, Point], typing.Tuple[bool, None]]:
        pass

    @abstractmethod
    def run_selection_op(self):
        pass

    @abstractmethod
    def run_crossover_op(self):
        pass

    @abstractmethod
    def run_mutation_op(self):
        pass

    @abstractmethod
    def run_replacement_op(self):
        pass

    def get_preserved(self):
        return self._preserved


class GeneticAlgorithm(AbstractGeneticAlgorithm):
    target_points: typing.List[Point] = []

    def __init__(
            self,
            selection_op: selection.Selection,
            crossover_op: crossover.Crossover,
            mutation_op: mutation.Mutation,
            replacement_op: replacement.Replacement,
    ):
        super().__init__(selection_op, crossover_op, mutation_op, replacement_op)

    def set_target_points(self, points: typing.List[Point]):
        if not gcommon.is_calibrated():
            gcommon.calibrate(points)

        self.target_points = points
        self._selection_op.setup(self.target_points)
        self._replacement_op.setup(self.target_points)

    def current_generation_to_phenotype(self) -> typing.List[Point]:
        return [ch.to_phenotype() for ch in self._current_generation]

    def middle_generation_to_phenotype(self) -> typing.List[Point]:
        return [ch.to_phenotype() for ch in self._middle_generation]

    def generate_initial_population(self):
        random.seed(time.time())
        self._current_generation = []

        for _ in range(config.INITIAL_POPULATION):
            chromosome_num = random.randrange(0, 2 ** config.CHROMOSOME_LENGTH)
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
                    if math.fabs(res - target.calc_distance(ch_phenotype)) > config.TARGET_TOLERANCE:
                        flag = False
                        break

            if flag:
                return True, ch_phenotype

        return False, None

    def run_selection_op(self):
        self._middle_generation = self._selection_op.run(self._current_generation)
        fitness_arr = [ch.calc_fitness(self.target_points) for ch in self._current_generation]
        fitness_avg = gcommon.arr_avg(fitness_arr)

        self._middle_generation = []
        fitness_arr_len = len(fitness_arr)

        for i in range(fitness_arr_len):
            f = fitness_arr[i]
            target_ch = self._current_generation[i]
            int_part = f // fitness_avg

            self._middle_generation += [target_ch for _ in range(int(int_part))]

            if random.random() + int_part <= f / fitness_avg:
                self._middle_generation.append(target_ch)

        if len(self._middle_generation) % 2 != 0:
            self._middle_generation.append(
                self._current_generation[random.randrange(0, fitness_arr_len)]
            )

        self._update_preserved(
            self._middle_generation,
            [ch.calc_fitness(self.target_points) for ch in self._middle_generation]
        )

    def run_crossover_op(self):
        new_mid_gen = []
        mid_gen_len = len(self._middle_generation)
        check_list = [i for i in range(mid_gen_len)]
        for i in range(mid_gen_len // 2):
            random.shuffle(check_list)
            if random.random() > config.CROSSOVER_POSSIBILITY:
                new_mid_gen.append(self._middle_generation[check_list[0]])
                new_mid_gen.append(self._middle_generation[check_list[1]])
                continue

            crossover_res = self._crossover_op.run(
                (self._middle_generation[check_list[0]], self._middle_generation[check_list[1]])
            )
            new_mid_gen.append(crossover_res[0])
            new_mid_gen.append(crossover_res[1])

        self._middle_generation = new_mid_gen
        self._update_preserved(
            self._middle_generation,
            [ch.calc_fitness(self.target_points) for ch in self._middle_generation]
        )

    def run_mutation_op(self):
        new_mid_gen = []
        for ch in self._middle_generation:
            if random.random() > config.MUTATION_POSSIBILITY:
                new_mid_gen.append(ch)
                continue

            new_mid_gen.append(self._mutation_op.run(ch))

        self._middle_generation = new_mid_gen
        self._update_preserved(
            self._middle_generation,
            [ch.calc_fitness(self.target_points) for ch in self._middle_generation]
        )

    def run_replacement_op(self):
        self._current_generation = self._replacement_op.run(
            self._current_generation,
            self._middle_generation
        )
        self._update_preserved(
            self._middle_generation,
            [ch.calc_fitness(self.target_points) for ch in self._middle_generation]
        )

    def _update_preserved(
            self,
            gen: typing.List[chromosome.AbstractChromosome],
            gen_fitness: typing.List[float],
    ):
        logging.info('Looking for new best chromosome...')
        gen_len = len(gen)
        gen_best = 0
        for i in range(1, gen_len):
            if gen_fitness[i] < gen_fitness[gen_best]:
                gen_best = i

        if self._preserved is None or self._preserved.calc_fitness(self.target_points) > gen_fitness[gen_best]:
            self._preserved = gen[gen_best]
            logging.info('Updating best chromosome to %s.', self._preserved.get_value())
