from common import point_to_arr, find_min, find_max
from gui.point import Point
import typing
import math
import config

_CALIBRATED = False


def is_calibrated() -> bool:
    return _CALIBRATED


def get_calibration_status() -> typing.Tuple[bool, bool, bool, bool]:
    set_chromosome_len = True
    set_gnome_len = True
    set_lower_bounds = True
    set_upper_bounds = True

    if config.CHROMOSOME_LENGTH is not None:
        set_chromosome_len = False
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


def calc_chromosome(num: int) -> str:
    res = ''
    while num > 0:
        res += str(int(num % 2))
        num = num // 2

    while len(res) != config.CHROMOSOME_LENGTH:
        res += '0'

    return res[::-1]


def arr_avg(num_arr: typing.Union[typing.List[int], typing.List[float]]) -> float:
    arr_sum = 0
    for num in num_arr:
        arr_sum += num

    return arr_sum / len(num_arr)
