import logging
import common
from center_finder import CenterFinder
from genetic.genetics import GeneticAlgorithm
import input.input_source
import config

logging.getLogger().setLevel(logging.INFO)
in_source = input.input_source.TxtFileInput("./sample.txt")
finder = CenterFinder(
    in_source,
    GeneticAlgorithm(
        config.SELECTION_OP,
        config.CROSSOVER_OP,
        config.MUTATION_OP,
        config.REPLACEMENT_OP,
    ),
)
finder.set_limit_checker(
    config.LIMIT_FUNC
)

common.print_active_config()

finder.draw_target_points([[1, 0, 0]])
end_flag, res_point = finder.check_end_condition()
if config.DRAW_GENERATION_POINTS:
    finder.draw_current_points([[0, 1, 0]])

while True:
    print(f'------------------------------ GENERATION {finder.get_generation() + 1} ------------------------------')
    finder.run_cycle()
    end_flag, res_point = finder.check_end_condition()
    if finder.get_limit() >= config.MAX_LIMIT or end_flag:
        print('Algorithm reached to maximum possible generation.')
        finder.clear_current_points()
        break

finder.draw_best([[0, 0, 1]])
best_point = finder.get_best()
print('Best point:', best_point.to_arr())
print('Best point fitness:', finder.get_best_in_genotype().calc_fitness(finder._target_points))
print('Distance from targets are:', [t.calc_distance(best_point) for t in finder._target_points])

for _ in range(6000):
    finder._drawer.flush()
