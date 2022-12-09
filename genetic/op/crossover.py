from abc import abstractmethod
import genetic.chromosome as chromosome
import typing
import random
import genetic.common as gcommon
import logging


class Crossover:
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
        if self.n > gcommon.CHROMOSOME_LENGTH - 1:
            logging.error(
                "chromosome with length %s doesn't support %s-pt crossover.",
                gcommon.CHROMOSOME_LENGTH,
                self.n,
            )
            return chs

        logging.info('Running %s-pt crossover on (%s, %s)...', self.n, chs[0].get_value(), chs[1].get_value())
        if self.n <= 0:
            return chs

        pts = []
        for _ in range(self.n):
            num = random.randrange(1, gcommon.CHROMOSOME_LENGTH - 1)
            if num not in pts:
                pts.append(num)

        pts.sort()
        logging.info('Points are: %s', pts)

        res = (
            chromosome.StrChromosome(chs[0].get_value()),
            chromosome.StrChromosome(chs[1].get_value()),
        )
        for i in pts:
            tmp = res[0].get_value()[:i + 1] + res[1].get_value()[i + 1:]
            res[1].set_value(res[1].get_value()[:i + 1] + res[0].get_value()[i + 1:])
            res[0].set_value(tmp)

        logging.info('Crossover was successful: (%s, %s)', res[0].get_value(), res[1].get_value())
        return res
