from abc import abstractmethod
import genetic.chromosome as chromosome
import typing
import random
import logging
import config
import common


class Crossover:
    _genetic = None

    def setup(self, genetic):
        self._genetic = genetic

    @abstractmethod
    def run(
            self,
            chs: typing.Tuple[chromosome.AbstractChromosome, chromosome.AbstractChromosome]
    ) -> typing.Tuple[chromosome.AbstractChromosome, chromosome.AbstractChromosome]:
        pass


class StrNptCrossover(Crossover):
    def __init__(self, n: int):
        logging.info("Initializing str %s-pt crossover...", n)
        self.n = n
        if n <= 0:
            logging.error("Invalid %s-pt crossover.", n)

    def run(
            self,
            chs: typing.Tuple[chromosome.StrChromosome, chromosome.StrChromosome]
    ) -> typing.Tuple[chromosome.StrChromosome, chromosome.StrChromosome]:
        if self.n > config.CHROMOSOME_LENGTH - 1:
            logging.error(
                "chromosome with length %s doesn't support %s-pt crossover.",
                config.CHROMOSOME_LENGTH,
                self.n,
            )
            return chs

        if self.n <= 0:
            return chs

        pts = []
        for _ in range(self.n):
            num = random.randrange(1, config.CHROMOSOME_LENGTH - 1)
            if num not in pts:
                pts.append(num)

        pts.sort()
        logging.info('Points are: %s', pts)

        logging.info('Running %s-pt crossover on (%s, %s)...', self.n, chs[0].get_value(), chs[1].get_value())
        res = (
            chromosome.StrChromosome(chs[0].get_value()),
            chromosome.StrChromosome(chs[1].get_value()),
        )
        for i in pts:
            tmp = res[0].get_value()[:i + 1] + res[1].get_value()[i + 1:]
            res[1].set_value(res[1].get_value()[:i + 1] + res[0].get_value()[i + 1:])
            res[0].set_value(tmp)

        logging.info('Crossover was successful: (%s, %s)', res[1].get_value(), res[0].get_value())
        return res


class AdaptiveCrossover(Crossover):
    _pre_fitness_avg: float = None
    _pre_gen: int = None
    _n_pt = 1

    def _generation_changed(self) -> bool:
        if self._pre_gen is None:
            self._pre_gen = -1
            return True

        if self._pre_gen + 2 <= self._genetic.get_generation_counter():
            self._pre_gen = self._genetic.get_generation_counter() - 1
            return True

        return False

    def run(
            self,
            chs: typing.Tuple[chromosome.StrChromosome, chromosome.StrChromosome]
    ) -> typing.Tuple[chromosome.StrChromosome, chromosome.StrChromosome]:
        if self._generation_changed():
            current_avg = common.get_arr_avg(self._genetic.get_current_gen_fitness())
            self._n_pt = 1
            if self._pre_fitness_avg is None or self._pre_fitness_avg >= current_avg:
                self._n_pt = 2

            logging.info("Generation changed, recalculating adaptive crossover to %s-pt.", self._n_pt)
            self._pre_fitness_avg = current_avg

        pts = []
        for _ in range(self._n_pt):
            num = random.randrange(1, config.CHROMOSOME_LENGTH - 1)
            if num not in pts:
                pts.append(num)

        pts.sort()
        logging.info('Points are: %s', pts)

        logging.info('Running %s-pt crossover on (%s, %s)...', self._n_pt, chs[0].get_value(), chs[1].get_value())
        res = (
            chromosome.StrChromosome(chs[0].get_value()),
            chromosome.StrChromosome(chs[1].get_value()),
        )
        for i in pts:
            tmp = res[0].get_value()[:i + 1] + res[1].get_value()[i + 1:]
            res[1].set_value(res[1].get_value()[:i + 1] + res[0].get_value()[i + 1:])
            res[0].set_value(tmp)

        logging.info('Crossover was successful: (%s, %s)', res[1].get_value(), res[0].get_value())
        return res
