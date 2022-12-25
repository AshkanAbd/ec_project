import genetic.genetics as genetic

# ---------------- UI CONFIG ---------------- #
PLOT_TOLERANCE = 2
UI_TICK_RATE = 0
DRAW_MUDDLE_POINTS = False
DRAW_GENERATION_POINTS = True
DRAW_BEST_POINT = True

# -------------- COLOR CONFIG -------------- #
TARGET_COLOR = [1, 0, 0]
SOLUTION_COLOR = [0, 0, 1]
GEN_COLOR = [0, 1, 0]
SELECTION_COLOR = [0, 1, 1]
CROSSOVER_COLOR = [1, 0, 1]
MUTATION_COLOR = [0, 0.5, 0.5]

# -------------- GENETIC CONFIG -------------- #
# -------------- GENETIC POSSIBILITY CONFIG -------------- #
CROSSOVER_POSSIBILITY = 0.85
MUTATION_POSSIBILITY = 0.1

# -------------- GENETIC STOP CONDITION CONFIG -------------- #
LIMIT_FUNC = genetic.AbstractGeneticAlgorithm.get_fitness_counter
MAX_LIMIT = 20 * 60
TARGET_TOLERANCE = 0.01

# -------------- GENETIC OPERATORS CONFIG -------------- #
SELECTION_OP = genetic.selection.FPSSelection()
CROSSOVER_OP = genetic.crossover.AdaptiveCrossover()
MUTATION_OP = genetic.mutation.StrBitFlippingMutation()
REPLACEMENT_OP = genetic.replacement.AlphaGenerationalReplacement(alpha=0.1, elitism=True)
MID_GEN_STRATEGY = genetic.strategy.AdaptiveMutationStrategy()

# -------------- OPTIONAL GENETIC CONFIG -------------- #
DIMENSION = 2
ONE_GENOME_LENGTH = 10
INITIAL_POPULATION = 20  # Can be None
CHROMOSOME_LENGTH = ONE_GENOME_LENGTH * DIMENSION  # Can be None
GENOME_LEN = [ONE_GENOME_LENGTH for x in range(DIMENSION)]  # Can be []
LOWER_BOUND = []  # Can be []
UPPER_BOUND = []  # Can be []
LOWER_BOUND_TOLERANCE = 0.2
UPPER_BOUND_TOLERANCE = 0.2
