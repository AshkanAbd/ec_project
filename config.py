import genetic.genetics as genetic

# ---------------- UI CONFIG ---------------- #
PLOT_TOLERANCE = 2
UI_TICK_RATE = 0
DRAW_MUDDLE_POINTS = False
DRAW_GENERATION_POINTS = False
DRAW_BEST_POINT = True

# -------------- GENETIC CONFIG -------------- #
# -------------- GENETIC POSSIBILITY CONFIG -------------- #
CROSSOVER_POSSIBILITY = 0.85
MUTATION_POSSIBILITY = 0.1
# -------------- GENETIC STOP CONDITION CONFIG -------------- #
LIMIT_FUNC = genetic.AbstractGeneticAlgorithm.get_fitness_counter
MAX_LIMIT = 20 * 20
TARGET_TOLERANCE = 0.01
# -------------- GENETIC OPERATORS CONFIG -------------- #
SELECTION_OP = genetic.selection.AverageFitnessSelection()
CROSSOVER_OP = genetic.crossover.AdaptiveCrossover()
MUTATION_OP = genetic.mutation.StrBitFlippingMutation()
REPLACEMENT_OP = genetic.replacement.AlphaGenerationalReplacement(0.1)
# -------------- OPTIONAL GENETIC CONFIG -------------- #
DIMENSION = 3
ONE_GENOME_LENGTH = 10
INITIAL_POPULATION = 20  # Can be None
CHROMOSOME_LENGTH = ONE_GENOME_LENGTH * DIMENSION  # Can be None
GENOME_LEN = [ONE_GENOME_LENGTH for x in range(DIMENSION)]  # Can be []
LOWER_BOUND = []  # Can be []
UPPER_BOUND = []  # Can be []
