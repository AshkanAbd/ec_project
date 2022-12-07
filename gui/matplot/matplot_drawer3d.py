import matplotlib.pyplot as plt
import typing
from gui.drawer import Drawer
from gui.point import Point


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
