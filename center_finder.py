import typing
import common
from genetic.genetics import AbstractGeneticAlgorithm
from gui.drawer import Drawer
from gui.drawers.matplot import get_drawer_params
from gui.point import Point
from input.input_source import InputStream
import logging
import config


class CenterFinder:
    _drawer: Drawer
    _genetic: AbstractGeneticAlgorithm
    _best: Point = None
    _target_points: typing.List[Point] = []
    _current_points: typing.List[Point] = []
    _middle_points: typing.List[Point] = []

    def __init__(self, in_stream: InputStream, genetic: AbstractGeneticAlgorithm):
        logging.info('Initializing center finder...')
        logging.info('Reading from input stream...')
        self._in_stream = in_stream
        self._in_stream.load()
        self._target_points = common.arr_to_point(self._in_stream.get_points())

        logging.info('Calibrating genetic configs...')
        if not common.is_calibrated():
            common.calibrate(self._target_points)

        logging.info('Initializing genetic algorithm...')
        self._genetic = genetic
        self._genetic.set_target_points(self._target_points)
        self._genetic.generate_initial_population()

        logging.info("Initializing drawer...")
        self.init_drawer()

        logging.info("CenterFinder initialized.")

    def init_drawer(self):
        drawer_constructor = common.get_drawer(self._in_stream.get_dimension())
        if drawer_constructor is None:
            self._drawer = Drawer()
            return
        self._drawer = drawer_constructor(
            (10, 8),
            get_drawer_params(self._in_stream.get_points(), self._in_stream.get_dimension())
        )

    def draw_target_points(self, color=None):
        logging.info("Drawing target points...")
        for p in self._target_points:
            p.set_color(color)
            self._drawer.draw_point(p)
        logging.info("%s target points were drawn", len(self._target_points))

    def draw_current_points(self, color=None):
        if self._current_points:
            logging.warning('Current points has been drawn')
            return

        logging.info("Drawing current points...")
        self._current_points = self._genetic.current_generation_to_phenotype()
        for p in self._current_points:
            p.set_color(color)
            self._drawer.draw_point(p)
        logging.info("%s current points were drawn", len(self._current_points))

    def clear_current_points(self):
        if not self._current_points:
            logging.warning("Current points have don't drawn yet")
            return

        logging.info('Clearing current points...')
        for p in self._current_points:
            self._drawer.remove_point(p)
        self._current_points.clear()

    def draw_middle_points(self, color=None):
        if self._middle_points:
            logging.warning('Middle points has been drawn')
            return

        logging.info("Drawing middle points...")
        self._middle_points = self._genetic.middle_generation_to_phenotype()
        for p in self._middle_points:
            p.set_color(color)
            self._drawer.draw_point(p)
        logging.info("%s middle points were drawn", len(self._middle_points))

    def clear_middle_points(self):
        if not self._middle_points:
            logging.warning("Middle points have don't drawn yet")
            return

        logging.info('Clearing middle points...')
        for p in self._middle_points:
            self._drawer.remove_point(p)
        self._middle_points.clear()

    def check_end_condition(self) -> typing.Union[typing.Tuple[bool, Point], typing.Tuple[bool, None]]:
        return self._genetic.check_end_condition()

    def run_cycle(self):
        self._genetic.run_selection_op()
        if config.DRAW_MUDDLE_POINTS:
            self.draw_middle_points([[0, 1, 1]])
        # input('Enter to continue...')
        self._genetic.run_crossover_op()
        if config.DRAW_MUDDLE_POINTS:
            self.clear_middle_points()
            self.draw_middle_points([[1, 0, 1]])
        # input('Enter to continue...')
        self._genetic.run_mutation_op()
        if config.DRAW_MUDDLE_POINTS:
            self.clear_middle_points()
            self.draw_middle_points([[0, 0.5, 0.5]])
        # input('Enter to continue...')
        self._genetic.run_replacement_op()
        # input('Enter to continue...')
        if config.DRAW_GENERATION_POINTS:
            self.clear_current_points()
            self.draw_current_points([[0, 1, 0]])
        # input('Enter to continue...')
        if config.DRAW_MUDDLE_POINTS:
            self.clear_middle_points()
        self._genetic.increase_generation_counter()
        if config.DRAW_BEST_POINT:
            self.draw_best([[0, 0, 1]])

    def get_limit(self) -> int:
        return self._genetic.get_generation_counter()

    def get_best_in_genotype(self):
        return self._genetic.get_preserved()

    def get_best(self) -> Point:
        return self._genetic.get_preserved().to_phenotype()

    def draw_best(self, color=None):
        if self._best is not None:
            self._drawer.remove_point(self._best)

        self._best = self.get_best()
        self._best.set_color(color)
        self._drawer.draw_point(self._best)
