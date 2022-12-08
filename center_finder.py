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

    def __init__(self, in_stream: InputStream, genetic: AbstractGeneticAlgorithm):
        self._in_stream = in_stream
        logging.info("Reading inputs...")
        self._in_stream.load()

        self.init_drawer()
        current_points = common.arr_to_point(self._in_stream.get_points(), [[1, 0, 0]])

        self._genetic = genetic
        self._genetic.phenotype_to_genotype(current_points)
        logging.info("CenterFinder initialized.")

    def init_drawer(self):
        logging.info("Initializing drawer...")
        drawer_cons = common.get_drawer(self._in_stream.get_dimension())
        self._drawer = drawer_cons(
            (10, 8),
            get_drawer_params(self._in_stream.get_points(), self._in_stream.get_dimension())
        )

    def draw_current_points(self):
        logging.info("Drawing current points...")
        current_points = self._genetic.genotype_to_phenotype()
        for p in current_points:
            self._drawer.draw_point(p)
        logging.info("%s points were drawn", len(current_points))
