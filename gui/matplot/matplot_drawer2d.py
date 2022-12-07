import matplotlib.pyplot as plt

from abc import ABC

import typing

from gui.drawer import Drawer

from gui.point import Point


class MatplotDrawer2D(Drawer, ABC):
    figure: None

    def __init__(self, figsize: typing.Tuple[int, int], pltsize: typing.Tuple[int, int]):
        plt.ion()
        self.figure = plt.figure(figsize=figsize)
        plt.plot(pltsize[0], pltsize[1])

    def draw_point(self, p: Point):
        plt.scatter([p.x, p.y])
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def remove_point(self, p: Point):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def flush(self):
        pass
