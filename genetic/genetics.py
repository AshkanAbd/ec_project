from abc import abstractmethod
from genetic.phenotype import Phenotype
import random
import time
import typing
import genetic.chromosome as chromosome
import genetic.op.crossover as crossover
import genetic.op.mutation as mutation
import genetic.op.selection as selection
import genetic.op.replacement as replacement
import genetic.mid_generation_strategy as strategy
import config
import logging


class AbstractGeneticAlgorithm:
    _current_generation: typing.List[chromosome.AbstractChromosome] = []
    _generation_counter = 0
    _selection_op: selection.Selection
    _crossover_op: crossover.Crossover
    _mutation_op: mutation.Mutation
    _replacement_op: replacement.Replacement
    _mid_gen_strategy: strategy.MidGenerationStrategy
    _preserved: chromosome.AbstractChromosome = None
    _preserved_fitness: float = None
    _targets: typing.List[Phenotype] = []
    _current_gen_fitness: typing.List[float] = []
    _fitness_counter = 0

    def __init__(
            self,
            selection_op: selection.Selection,
            crossover_op: crossover.Crossover,
            mutation_op: mutation.Mutation,
            replacement_op: replacement.Replacement,
            mid_gen_strategy: strategy.MidGenerationStrategy,
    ):
        self._selection_op = selection_op
        self._crossover_op = crossover_op
        self._mutation_op = mutation_op
        self._replacement_op = replacement_op
        self._mid_gen_strategy = mid_gen_strategy

    def increase_generation_counter(self):
        self._generation_counter += 1

    def get_generation_counter(self) -> int:
        return self._generation_counter

    def get_fitness_counter(self) -> int:
        return self._fitness_counter

    def calc_current_gen_fitness(self):
        self._current_gen_fitness = [ch.calc_fitness(self._targets) for ch in self._current_generation]
        self._fitness_counter += len(self._current_gen_fitness)

    def get_current_gen_fitness(self) -> typing.List[float]:
        return self._current_gen_fitness

    @abstractmethod
    def set_target_points(self, points: typing.List[Phenotype]):
        pass

    @abstractmethod
    def current_generation_to_phenotype(self) -> typing.List[Phenotype]:
        pass

    @abstractmethod
    def middle_generation_to_phenotype(self) -> typing.List[Phenotype]:
        pass

    @abstractmethod
    def generate_initial_population(self):
        pass

    @abstractmethod
    def check_end_condition(self) -> typing.Union[typing.Tuple[bool, Phenotype], typing.Tuple[bool, None]]:
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
    def set_target_points(self, points: typing.List[Phenotype]):
        self._targets = points
        self._selection_op.setup(self._targets, self)
        self._crossover_op.setup(self)
        self._mutation_op.setup(self)
        self._replacement_op.setup(self._targets, self)

    def current_generation_to_phenotype(self) -> typing.List[Phenotype]:
        return [ch.to_phenotype() for ch in self._current_generation]

    def middle_generation_to_phenotype(self) -> typing.List[Phenotype]:
        return [ch.to_phenotype() for ch in self._mid_gen_strategy.get_generation()]

    def generate_initial_population(self):
        random.seed(time.time())
        self._current_generation = []

        for _ in range(config.INITIAL_POPULATION):
            chromosome_num = random.randrange(0, 2 ** config.CHROMOSOME_LENGTH)
            self._current_generation.append(
                chromosome.StrChromosome(chromosome_num)
            )

    def check_end_condition(self) -> typing.Union[typing.Tuple[bool, Phenotype], typing.Tuple[bool, None]]:
        return False, None

    def run_selection_op(self):
        self._mid_gen_strategy.set_generation(
            self._selection_op.run(self._current_generation)
        )

    def run_crossover_op(self):
        crossover_chs = self._mid_gen_strategy.pick_for_crossover()
        crossover_chs_len = len(crossover_chs)
        crossover_res = []
        for i in range(crossover_chs_len // 2):
            crossover_res += self._crossover_op.run(
                (crossover_chs[i], crossover_chs[i + 1],)
            )

        self._mid_gen_strategy.apply_crossover_res(crossover_res)

    def run_mutation_op(self):
        mutation_chs = self._mid_gen_strategy.pick_for_mutation()
        mutation_res = []
        for ch in mutation_chs:
            mutation_res.append(
                self._mutation_op.run(ch)
            )

        self._mid_gen_strategy.apply_mutation_res(mutation_res)

    def run_replacement_op(self):
        self._current_generation = self._replacement_op.run(
            self._current_generation,
            self._mid_gen_strategy.pick_for_replacement()
        )
        self._update_preserved()

    def _update_preserved(self):
        logging.info('Looking for new best chromosome...')
        gen_len = len(self._current_generation)
        gen_best = 0
        for i in range(1, gen_len):
            if self._current_gen_fitness[i] < self._current_gen_fitness[gen_best]:
                gen_best = i

        if self._preserved is None or self._preserved_fitness > self._current_gen_fitness[gen_best]:
            self._preserved = self._current_generation[gen_best]
            self._preserved_fitness = self._current_gen_fitness[gen_best]
            logging.info(
                'Updating best chromosome to %s with %s fitness.',
                self._preserved.get_value(),
                self._preserved_fitness
            )
