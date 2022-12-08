import typing
import common
from gui.drawer import Drawer
from gui.drawers.matplot import get_drawer_params
from gui.point import Point
from input.input_source import InputStream
import logging


class CenterFinder:
    _drawer: Drawer
    current_points: typing.List[Point] = []

    def __init__(self, in_stream: InputStream):
        self._in_stream = in_stream
        logging.info("Reading inputs...")
        self._in_stream.load()
        self.current_points = common.arr_to_point(self._in_stream.get_points(), [[1, 0, 0]])

        self.init_drawer()
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
        for p in self.current_points:
            self._drawer.draw_point(p)
        logging.info("%s points were drawn", len(self.current_points))
