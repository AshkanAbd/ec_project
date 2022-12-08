import matplotlib.pyplot as plt
import typing
from gui.drawer import Drawer
from gui.point import Point


class MatplotDrawer2D(Drawer):
    _points = {}

    def __init__(self, figsize: typing.Tuple[int, int], pltsize: typing.Tuple[int, int]):
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        plt.plot(pltsize[0], pltsize[1])

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

    def __init__(self, figsize: typing.Tuple[int, int], pltsize: typing.Tuple[int]):
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        plt.plot(pltsize[0], 1)
        plt.xlim(-2, pltsize[0] + 2)
        plt.ylim(0, 0)
        plt.hlines(0, 0, pltsize[0], colors=[[0, 0, 0]])

    def draw_point(self, p: Point):
        self._points[p.__str__()] = plt.scatter(p.x, 0, c=p.color)
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()


class MatplotDrawer3D(Drawer):
    _points = {}

    def __init__(self, figsize: typing.Tuple[int, int], pltsize: typing.Tuple[int, int, int]):
        plt.ion()
        self._figure = plt.figure(figsize=figsize)
        self.ax = self._figure.add_subplot(111, projection='3d')
        plt.plot(pltsize[0], pltsize[1], pltsize[2])

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
