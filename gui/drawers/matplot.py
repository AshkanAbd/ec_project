import matplotlib.pyplot as plt
import typing
from gui.drawer import Drawer
from gui.point import Point

_PLOT_TOLERANCE = 10


def _set_plot_limits(lims: typing.Tuple[int, int], fn):
    fn(lims[0] - _PLOT_TOLERANCE, lims[1] + _PLOT_TOLERANCE)


def _set_plot_for_x(x: typing.Tuple[int, int]):
    plt.xlim(x[0] - _PLOT_TOLERANCE, x[1] + _PLOT_TOLERANCE)


def _set_plot_for_y(y: typing.Tuple[int, int]):
    plt.ylim(y[0] - _PLOT_TOLERANCE, y[1] + _PLOT_TOLERANCE)


class MatplotDrawer2D(Drawer):
    _points = {}

    def __init__(
            self,
            figsize: typing.Tuple[int, int],
            pltsize: typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]
    ):
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        plt.plot(
            abs(pltsize[0][0] - pltsize[0][1]),
            abs(pltsize[1][0] - pltsize[1][1]),
        )
        _set_plot_limits(pltsize[0], plt.xlim)
        _set_plot_limits(pltsize[1], plt.ylim)

    def draw_point(self, p: Point):
        self._points[p.__str__()] = plt.scatter(p.x, p.y, c=p.color)
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()

    def remove_point(self, p: Point) -> bool:
        if p.__str__() not in self._points:
            return False

        self._points[p.__str__()].remove()
        del self._points[p.__str__()]
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()
        return True

    def flush(self):
        pass


class MatplotDrawer1D(MatplotDrawer2D):
    _points = {}

    def __init__(self, figsize: typing.Tuple[int, int], pltsize: typing.Tuple[typing.Tuple[int, int]]):
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        plt.plot(abs(pltsize[0][0] - pltsize[0][1]), 1)
        _set_plot_limits(pltsize[0], plt.xlim)
        _set_plot_limits((0, 0), plt.ylim)
        plt.hlines(
            0,
            min(pltsize[0]) - _PLOT_TOLERANCE,
            max(pltsize[0]) + _PLOT_TOLERANCE,
            colors=[[0.8, 0.8, 0.8, 0.7]],
        )

    def draw_point(self, p: Point):
        self._points[p.__str__()] = plt.scatter(p.x, 0, c=p.color)
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()


class MatplotDrawer3D(Drawer):
    _points = {}

    def __init__(
            self,
            figsize: typing.Tuple[int, int],
            pltsize: typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int], typing.Tuple[int, int]],
    ):
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

    def draw_point(self, p: Point):
        self._points[p.__str__()] = self.ax.scatter(p.x, p.y, p.z, c=p.color)
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()

    def remove_point(self, p: Point) -> bool:
        if p.__str__() not in self._points:
            return False

        self._points[p.__str__()].remove()
        del self._points[p.__str__()]
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()
        return True

    def flush(self):
        pass