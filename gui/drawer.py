from gui.point import Point
from abc import abstractmethod


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
