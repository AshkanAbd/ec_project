import typing
import common
from genetic.genetics import AbstractGeneticAlgorithm
from gui.drawer import Drawer
from gui.drawers.matplot import get_drawer_params
from gui.point import Point
from input.input_source import InputStream
import logging


class CenterFinder:
    _drawer: Drawer
    _genetic: AbstractGeneticAlgorithm
    _target_points: typing.List[Point] = []

    def __init__(self, in_stream: InputStream, genetic: AbstractGeneticAlgorithm):
        logging.info('Initializing center finder...')
        logging.info('Reading from input stream...')
        self._in_stream = in_stream
        self._in_stream.load()
        self._target_points = common.arr_to_point(self._in_stream.get_points(), color=[[1, 0, 0]])

        logging.info('Initializing genetic algorithm...')
        self._genetic = genetic
        self._genetic.set_target_points(self._target_points)
        self._genetic.generate_initial_population()

        logging.info("Initializing drawer...")
        self.init_drawer()

        logging.info("CenterFinder initialized.")

    def init_drawer(self):
        drawer_constructor = common.get_drawer(self._in_stream.get_dimension())
        self._drawer = drawer_constructor(
            (10, 8),
            get_drawer_params(self._in_stream.get_points(), self._in_stream.get_dimension())
        )

    def draw_target_points(self):
        logging.info("Drawing target points...")
        for p in self._target_points:
            self._drawer.draw_point(p)
        logging.info("%s target points were drawn", len(self._target_points))

    def draw_current_points(self, color=None):
        logging.info("Drawing current points...")
        current_points = self._genetic.current_generation_to_phenotype()
        for p in current_points:
            p.set_color(color)
            self._drawer.draw_point(p)
        logging.info("%s current points were drawn", len(current_points))

    def clear_current_points(self):
        logging.info('Clearing current points...')
        current_points = self._genetic.current_generation_to_phenotype()
        for p in current_points:
            self._drawer.remove_point(p)

    def draw_middle_points(self, color=None):
        logging.info("Drawing middle points...")
        middle_points = self._genetic.middle_generation_to_phenotype()
        for p in middle_points:
            p.set_color(color)
            self._drawer.draw_point(p)
        logging.info("%s middle points were drawn", len(middle_points))

    def clear_middle_points(self):
        logging.info('Clearing middle points...')
        middle_points = self._genetic.middle_generation_to_phenotype()
        for p in middle_points:
            self._drawer.remove_point(p)

    def check_end_condition(self) -> typing.Union[typing.Tuple[bool, Point], typing.Tuple[bool, None]]:
        return self._genetic.check_end_condition()
