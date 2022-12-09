import logging
import time
from center_finder import CenterFinder
from genetic.genetics import GeneticAlgorithm
import input.input_source
import genetic.op.crossover as crossover
import genetic.op.mutation as mutation
import genetic.op.selection as selection
import genetic.op.replacement as replacement
import config

logging.getLogger().setLevel(logging.INFO)
in_source = input.input_source.TxtFileInput("./sample.txt")
finder = CenterFinder(
    in_source,
    GeneticAlgorithm(
        selection.AverageFitnessSelection(),
        crossover.StrNptCrossover(1),
        mutation.StrBitFlippingMutation(),
        replacement.AlphaGenerationalReplacement(0.3),
    ),
)

print(config.CHROMOSOME_LENGTH)
finder.draw_target_points([[1, 0, 0]])
end_flag, res_point = finder.check_end_condition()

while not end_flag:
    print(f'----------------------------------- GENERATION {finder.get_limit()} -----------------------------------')
    finder.run_cycle(True)
    finder.draw_best([[0, 0, 1]])
    end_flag, res_point = finder.check_end_condition()
    if finder.get_limit() == 20:
        finder.clear_middle_points()
        break

best_point = finder.get_best()
print('Best point:', best_point.to_arr())
print('Best point fitness:', finder.get_best_in_genotype().calc_fitness(finder._target_points))

time.sleep(60)
