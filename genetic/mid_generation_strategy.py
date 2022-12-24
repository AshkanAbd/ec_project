import random
import typing
import config
from abc import abstractmethod
from genetic.chromosome import AbstractChromosome


class MidGenerationStrategy:
    _generation: typing.List[AbstractChromosome]

    def set_generation(self, gen: typing.List[AbstractChromosome]):
        self._generation = gen

    def get_generation(self) -> typing.List[AbstractChromosome]:
        return self._generation

    @abstractmethod
    def pick_for_crossover(self) -> typing.List[AbstractChromosome]:
        pass

    @abstractmethod
    def apply_crossover_res(self, chs: typing.List[AbstractChromosome]):
        pass

    @abstractmethod
    def pick_for_mutation(self) -> typing.List[AbstractChromosome]:
        pass

    @abstractmethod
    def apply_mutation_res(self, chs: typing.List[AbstractChromosome]):
        pass

    @abstractmethod
    def pick_for_replacement(self) -> typing.List[AbstractChromosome]:
        pass


class RandomStrategy(MidGenerationStrategy):
    _survived_chs = []

    def pick_for_crossover(self) -> typing.List[AbstractChromosome]:
        self._survived_chs.clear()
        gen_len = len(self._generation)
        check_list = [i for i in range(gen_len)]
        res = []
        for i in range(gen_len // 2):
            random.shuffle(check_list)
            if random.random() > config.CROSSOVER_POSSIBILITY:
                self._survived_chs.append(self._generation[check_list[0]])
                self._survived_chs.append(self._generation[check_list[1]])
                continue

            res.append(self._generation[check_list[0]])
            res.append(self._generation[check_list[1]])

        return res

    def apply_crossover_res(self, chs: typing.List[AbstractChromosome]):
        self.set_generation(self._survived_chs + chs)

    def pick_for_mutation(self) -> typing.List[AbstractChromosome]:
        self._survived_chs.clear()
        res = []
        for ch in self._generation:
            if random.random() > config.MUTATION_POSSIBILITY:
                self._survived_chs.append(ch)
                continue

            res.append(ch)

        return res

    def apply_mutation_res(self, chs: typing.List[AbstractChromosome]):
        self.set_generation(self._survived_chs + chs)

    def pick_for_replacement(self) -> typing.List[AbstractChromosome]:
        return self.get_generation()


class AdaptiveMutationStrategy(MidGenerationStrategy):
    _crossover_chs = []
    _survived_chs = []

    def pick_for_crossover(self) -> typing.List[AbstractChromosome]:
        self._crossover_chs.clear()
        self._survived_chs.clear()
        gen_len = len(self._generation)
        check_list = [i for i in range(gen_len)]
        res = []
        for i in range(gen_len // 2):
            random.shuffle(check_list)
            if random.random() > config.CROSSOVER_POSSIBILITY:
                self._survived_chs.append(self._generation[check_list[0]])
                self._survived_chs.append(self._generation[check_list[1]])
                continue

            res.append(self._generation[check_list[0]])
            res.append(self._generation[check_list[1]])

        self._crossover_chs += res

        return res

    def apply_crossover_res(self, chs: typing.List[AbstractChromosome]):
        self._crossover_chs.clear()
        self._crossover_chs += chs
        self.set_generation(self._survived_chs + chs)

    def pick_for_mutation(self) -> typing.List[AbstractChromosome]:
        return self._crossover_chs

    def apply_mutation_res(self, chs: typing.List[AbstractChromosome]):
        self.set_generation(self._survived_chs + chs)

    def pick_for_replacement(self) -> typing.List[AbstractChromosome]:
        return self.get_generation()
