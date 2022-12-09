from abc import abstractmethod
import random
import genetic.chromosome as chromosome
import logging
import config


class Mutation:
    @abstractmethod
    def run(self, ch: chromosome.AbstractChromosome) -> chromosome.AbstractChromosome:
        pass


class StrBitFlippingMutation(Mutation):
    def __init__(self):
        logging.info('StrBitFlippingMutation initialized')

    def run(self, ch: chromosome.StrChromosome) -> chromosome.StrChromosome:
        pos = random.randrange(0, config.CHROMOSOME_LENGTH)
        logging.info('bit %s will flip', pos)

        logging.info('Run str bit flipping on: %s', ch.get_value())
        ch_val: str = ch.get_value()
        if ch_val[pos] == '0':
            ch_val = ch_val[:pos] + '1' + ch_val[pos + 1:]
        else:
            ch_val = ch_val[:pos] + '0' + ch_val[pos + 1:]

        logging.info('Mutation was successful: %s', ch_val)
        return chromosome.StrChromosome(ch_val)
