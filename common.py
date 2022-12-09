import typing
from gui.drawers.matplot import MatplotDrawer1D, MatplotDrawer2D, MatplotDrawer3D
from gui.point import Point
import time
import config

DRAWERS = {
    1: MatplotDrawer1D,
    2: MatplotDrawer2D,
    3: MatplotDrawer3D
}


def print_active_config():
    print('-------------------------------- UI  CONFIG --------------------------------')
    print('PLOT_TOLERANCE', config.PLOT_TOLERANCE)
    print('UI_TICK_RATE', config.UI_TICK_RATE)
    print('DRAW_MUDDLE_POINTS', config.DRAW_MUDDLE_POINTS)
    print('DRAW_GENERATION_POINTS', config.DRAW_GENERATION_POINTS)
    print('------------------------------ GENETIC CONFIG ------------------------------')
    print('CROSSOVER_POSSIBILITY', config.CROSSOVER_POSSIBILITY)
    print('MUTATION_POSSIBILITY', config.MUTATION_POSSIBILITY)
    print('INITIAL_POPULATION', config.INITIAL_POPULATION)
    print('CHROMOSOME_LENGTH', config.CHROMOSOME_LENGTH)
    print('GENOME_LEN', config.GENOME_LEN)
    print('LOWER_BOUND', config.LOWER_BOUND)
    print('UPPER_BOUND', config.UPPER_BOUND)
    print('TARGET_TOLERANCE', config.TARGET_TOLERANCE)
    print('MAX_GENERATION', config.MAX_GENERATION)
    print('ALPHA_REPLACEMENT', config.ALPHA_REPLACEMENT)
    print('N_PTS_CROSSOVER', config.N_PTS_CROSSOVER)


def ui_tick():
    time.sleep(config.UI_TICK_RATE)


def get_drawer(dimension: int) -> typing.Type[typing.Union[MatplotDrawer1D, MatplotDrawer2D, MatplotDrawer3D]]:
    return DRAWERS[dimension]


def point_to_arr(points: typing.List[Point]) -> typing.List[typing.List[float]]:
    return [p.to_arr() for p in points]


def arr_to_point(arr: typing.List[typing.List[float]], color=None) -> typing.List[Point]:
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
