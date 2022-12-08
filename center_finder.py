import common
from gui.drawer import Drawer
from gui.drawers.matplot import get_drawer_params
from input.input_source import InputStream
import logging


class CenterFinder:
    _drawer: Drawer

    def __init__(self, in_stream: InputStream):
        self._in_stream = in_stream
        logging.info("Reading inputs...")
        self._in_stream.load()
        self.init_drawer()

        logging.info("CenterFinder initialized.")

    def a(self, dimension: int):
        return (
            common.float_to_real(common.find_min(self._in_stream.get_points(), dimension)),
            common.float_to_real(common.find_max(self._in_stream.get_points(), dimension)),
        )

    def init_drawer(self):
        logging.info("Initializing drawer...")
        drawer_cons = common.get_drawer(self._in_stream.get_dimension())
        self._drawer = drawer_cons(
            (10, 8),
            get_drawer_params(self._in_stream.get_points(), self._in_stream.get_dimension())
        )
