import typing
from gui.drawers.matplot import MatplotDrawer1D, MatplotDrawer2D, MatplotDrawer3D
from gui.point import Point

DRAWERS = {
    1: MatplotDrawer1D,
    2: MatplotDrawer2D,
    3: MatplotDrawer3D
}


def get_drawer(dimension: int) -> typing.Type[typing.Union[MatplotDrawer1D, MatplotDrawer2D, MatplotDrawer3D]]:
    return DRAWERS[dimension]


def arr_to_point(arr: typing.List[typing.List[float]], color) -> typing.List[Point]:
    return [Point(i, color=color) for i in arr]


def find_min(arr: typing.List[typing.List[float]], index: int) -> float:
    res = arr[0][index]

    for i in arr:
        if i[index] < res:
            res = i[index]

    return res


def find_max(arr: typing.List[typing.List[float]], index: int) -> float:
    res = arr[0][index]

    for i in arr:
        if i[index] > res:
            res = i[index]

    return res


def float_to_real(f: float) -> int:
    res = int(f)

    if res != f and f < 0:
        return res - 1

    return res
