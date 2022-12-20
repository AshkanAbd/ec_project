import typing
from gui.drawers.matplot import MatplotDrawer1D, MatplotDrawer2D, MatplotDrawer3D
from gui.point import Point
import time
import config
import math

DRAWERS = {
    1: MatplotDrawer1D,
    2: MatplotDrawer2D,
    3: MatplotDrawer3D
}
_CALIBRATED = False


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


def get_drawer(dimension: int) -> typing.Type[typing.Union[MatplotDrawer1D, MatplotDrawer2D, MatplotDrawer3D, None]]:
    if dimension not in DRAWERS:
        return None
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


def is_calibrated() -> bool:
    return _CALIBRATED


def get_calibration_status() -> typing.Tuple[bool, bool, bool, bool]:
    set_chromosome_len = True
    set_gnome_len = True
    set_lower_bounds = True
    set_upper_bounds = True

    if config.CHROMOSOME_LENGTH is not None:
        set_chromosome_len = False
    else:
        config.CHROMOSOME_LENGTH = 0

    if config.GENOME_LEN:
        set_gnome_len = False
    if config.LOWER_BOUND:
        set_lower_bounds = False
    if config.UPPER_BOUND:
        set_upper_bounds = False

    return set_chromosome_len, set_gnome_len, set_upper_bounds, set_lower_bounds


def calibrate(points: typing.List[Point]):
    global _CALIBRATED
    points_arr = point_to_arr(points)
    dimension = points[0].get_dimension()
    calibrate_status = get_calibration_status()
    for i in range(dimension):
        l_bound = find_min(points_arr, i)
        u_bound = find_max(points_arr, i)
        l_bound -= l_bound / 10 * 2
        u_bound += u_bound / 10 * 2
        if calibrate_status[3]:
            config.LOWER_BOUND.append(l_bound)
        if calibrate_status[2]:
            config.UPPER_BOUND.append(u_bound)
        g_len = math.ceil(math.log2(u_bound - l_bound + 1))
        if calibrate_status[1]:
            config.GENOME_LEN.append(g_len)
        if calibrate_status[0]:
            config.CHROMOSOME_LENGTH += g_len

    if config.INITIAL_POPULATION is None:
        config.INITIAL_POPULATION = math.ceil(1.65 * (2 ** (0.21 * config.CHROMOSOME_LENGTH)))

    if config.INITIAL_POPULATION % 2 != 0:
        config.INITIAL_POPULATION += 1

    if config.TARGET_TOLERANCE is None:
        config.TARGET_TOLERANCE = 0.001

    _CALIBRATED = True
