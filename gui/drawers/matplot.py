import logging
import matplotlib.pyplot as plt
import typing
import common
from gui.drawer import Drawer
from gui.point import Point
import config


def _set_plot_limits(lims: typing.Tuple[int, int], fn):
    fn(lims[0] - config.PLOT_TOLERANCE, lims[1] + config.PLOT_TOLERANCE)


def _set_plot_for_x(x: typing.Tuple[int, int]):
    plt.xlim(x[0] - config.PLOT_TOLERANCE, x[1] + config.PLOT_TOLERANCE)


def _set_plot_for_y(y: typing.Tuple[int, int]):
    plt.ylim(y[0] - config.PLOT_TOLERANCE, y[1] + config.PLOT_TOLERANCE)


class MatplotDrawer2D(Drawer):
    _points = {}

    def __init__(
            self,
            figsize: typing.Tuple[int, int],
            pltsize: typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]
    ):
        if config.PLOT_TOLERANCE is None:
            config.PLOT_TOLERANCE = 10
        logging.info("Initializing 2D drawer...")
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        plt.plot(
            abs(pltsize[0][0] - pltsize[0][1]),
            abs(pltsize[1][0] - pltsize[1][1]),
        )
        _set_plot_limits(pltsize[0], plt.xlim)
        _set_plot_limits(pltsize[1], plt.ylim)
        logging.info("2D drawer initialized")

    def draw_point(self, p: Point):
        if p.__str__() in self._points:
            # logging.warning("%s was drawn before", p.__str__())
            return

        self._points[p.__str__()] = plt.scatter(p.x, p.y, c=p.color)
        # logging.info("%s was drawn", p.__str__())
        self.flush()

    def remove_point(self, p: Point) -> bool:
        if p.__str__() not in self._points:
            # logging.warning("%s hasn't been drawn yet", p.__str__())
            return False

        self._points[p.__str__()].remove()
        del self._points[p.__str__()]
        # logging.info("%s cleared", p.__str__())
        self.flush()
        return True

    def flush(self):
        common.ui_tick()
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()


class MatplotDrawer1D(MatplotDrawer2D):
    _points = {}

    def __init__(self, figsize: typing.Tuple[int, int], pltsize: typing.Tuple[typing.Tuple[int, int]]):
        logging.info("Initializing 1D drawer...")
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        plt.plot(abs(pltsize[0][0] - pltsize[0][1]), 1)
        _set_plot_limits(pltsize[0], plt.xlim)
        _set_plot_limits((0, 0), plt.ylim)
        plt.hlines(
            0,
            min(pltsize[0]) - config.PLOT_TOLERANCE,
            max(pltsize[0]) + config.PLOT_TOLERANCE,
            colors=[[0.8, 0.8, 0.8, 0.7]],
        )
        logging.info("1D drawer initialized")

    def draw_point(self, p: Point):
        if p.__str__() in self._points:
            # logging.warning("%s was drawn before", p.__str__())
            return

        self._points[p.__str__()] = plt.scatter(p.x, 0, c=p.color)
        # logging.info("%s was drawn", p.__str__())
        self.flush()


class MatplotDrawer3D(Drawer):
    _points = {}

    def __init__(
            self,
            figsize: typing.Tuple[int, int],
            pltsize: typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int], typing.Tuple[int, int]],
    ):
        logging.info("Initializing 3D drawer...")
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        self.ax = self._figure.add_subplot(111, projection='3d')
        plt.plot(
            abs(pltsize[0][0] - pltsize[0][1]),
            abs(pltsize[1][0] - pltsize[1][1]),
            abs(pltsize[2][0] - pltsize[2][1]),
        )
        _set_plot_limits(pltsize[0], plt.xlim)
        _set_plot_limits(pltsize[1], plt.ylim)
        _set_plot_limits(pltsize[2], self.ax.set_zlim)
        logging.info("3D drawer initialized")

    def draw_point(self, p: Point):
        if p.__str__() in self._points:
            # logging.warning("%s was drawn before", p.__str__())
            return

        self._points[p.__str__()] = self.ax.scatter(p.x, p.y, p.z, c=p.color)
        # logging.info("%s was drawn", p.__str__())
        self.flush()

    def remove_point(self, p: Point) -> bool:
        if p.__str__() not in self._points:
            # logging.warning("%s hasn't been drawn yet", p.__str__())
            return False

        self._points[p.__str__()].remove()
        del self._points[p.__str__()]
        # logging.info("%s cleared", p.__str__())
        self.flush()
        return True

    def flush(self):
        common.ui_tick()
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()


def drawer_params_builder(points: typing.List[typing.List[float]], dimension: int):
    return (
        common.float_to_real(common.find_min(points, dimension)),
        common.float_to_real(common.find_max(points, dimension)),
    )


def get_drawer_params(points: typing.List[typing.List[float]], dimension: int):
    if dimension == 1:
        logging.info("Calculating 1D drawer params...")
        return (
            drawer_params_builder(points, 0),
        )
    elif dimension == 2:
        logging.info("Calculating 2D drawer params...")
        return (
            drawer_params_builder(points, 0),
            drawer_params_builder(points, 1),
        )
    else:
        logging.info("Calculating 3D drawer params...")
        return (
            drawer_params_builder(points, 0),
            drawer_params_builder(points, 1),
            drawer_params_builder(points, 2),
        )
