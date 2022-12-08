import logging
from abc import abstractmethod
import typing


class InputStream:
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        pass

    @abstractmethod
    def get_point_count(self) -> int:
        pass

    @abstractmethod
    def get_points(self) -> typing.List[typing.List[float]]:
        pass


class TxtFileInput(InputStream):
    _dimension = 0
    _point_count = 0
    _points = []

    def __init__(self, file_path: str):
        logging.info("Txt file input initialized with file %s", file_path)
        self._file_path = file_path
        self.loaded = False

    def load(self):
        if self.loaded:
            logging.warning("Txt file already loaded.")
            return

        logging.info("Reading txt file %s", self._file_path)

        with open(self._file_path) as fs:
            logging.info("Reading dimension...")
            self._dimension = int(fs.readline())

            logging.info("Reading point count...")
            self._point_count = int(fs.readline())

            logging.info("Reading points...")
            for _ in range(self._point_count):
                self._points.append(
                    [float(x) for x in fs.readline().split(" ")][:self._dimension]
                )

        self.loaded = True
        logging.info("Txt file has read successfully.")

    def get_dimension(self) -> int:
        if not self.loaded:
            logging.error("Txt file didn't loaded yet.")

        return self._dimension

    def get_point_count(self) -> int:
        if not self.loaded:
            logging.error("Txt file didn't loaded yet.")

        return self._point_count

    def get_points(self) -> typing.List[typing.List[float]]:
        if not self.loaded:
            logging.error("Txt file didn't loaded yet.")

        return self._points
