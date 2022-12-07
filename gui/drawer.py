from abc import ABC, abstractmethod

from gui.point import Point


class Drawer:
    @abstractmethod
    def draw_point(self, p: Point):
        pass

    @abstractmethod
    def remove_point(self, p: Point):
        pass

    @abstractmethod
    def flush(self):
        pass
