from abc import abstractmethod
import random
import genetic.chromosome as chromosome
import genetic.common as gcommon
import logging


class Mutation:
    @abstractmethod
    def run(self, ch: chromosome.AbstractChromosome) -> chromosome.AbstractChromosome:
        pass


class StrBitFlippingMutation(Mutation):
    def __init__(self):
        logging.info('StrBitFlippingMutation initialized')

    def run(self, ch: chromosome.StrChromosome) -> chromosome.StrChromosome:
        logging.info('Run str bit flipping on: %s', ch.get_value())
        pos = random.randrange(0, gcommon.CHROMOSOME_LENGTH)
        logging.info('%s bit will flip', pos)

        ch_val: str = ch.get_value()
        if ch_val[pos] == '0':
            ch_val = ch_val[:pos] + '1' + ch_val[pos + 1:]
        else:
            ch_val = ch_val[:pos] + '0' + ch_val[pos + 1:]

        logging.info('Mutation was successful: %s', ch_val)
        return chromosome.StrChromosome(ch_val)
