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
        crossover.StrNptCrossover(10),
        mutation.StrBitFlippingMutation(),
        replacement.AlphaGenerationalReplacement(0.3),
    ),
)

finder.draw_target_points([[1, 0, 0]])
end_flag, res_point = finder.check_end_condition()

while not end_flag:
    print(f'------------------------------ GENERATION {finder.get_limit() + 1} ------------------------------')
    finder.run_cycle(draw_middle=False, draw_current=False)
    finder.draw_best([[0, 0, 1]])
    end_flag, res_point = finder.check_end_condition()
    if finder.get_limit() == config.MAX_GENERATION:
        print('Algorithm reached to maximum possible generation.')
        finder.clear_middle_points()
        break

best_point = finder.get_best()
print('Best point:', best_point.to_arr())
print('Best point fitness:', finder.get_best_in_genotype().calc_fitness(finder._target_points))
print('Distance from targets are:', [t.calc_distance(best_point) for t in finder._target_points])

for _ in range(6000):
    finder._drawer.flush()
