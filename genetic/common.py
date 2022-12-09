from common import point_to_arr, find_min, find_max
from gui.point import Point
import typing
import math

CHROMOSOME_LENGTH = 0
GENOME_LEN = []
LOWER_BOUND = []
UPPER_BOUND = []
_CALIBRATED = False


def is_calibrated() -> bool:
    return _CALIBRATED


def reset():
    global GENOME_LEN, UPPER_BOUND, LOWER_BOUND, _CALIBRATED, CHROMOSOME_LENGTH
    GENOME_LEN = []
    UPPER_BOUND = []
    LOWER_BOUND = []
    _CALIBRATED = False
    CHROMOSOME_LENGTH = 0


def calibrate(points: typing.List[Point]):
    global _CALIBRATED, UPPER_BOUND, LOWER_BOUND, GENOME_LEN, CHROMOSOME_LENGTH
    reset()
    points_arr = point_to_arr(points)
    dimension = points[0].get_dimension()
    for i in range(dimension):
        l_bound = find_min(points_arr, i)
        u_bound = find_max(points_arr, i)
        l_bound -= l_bound / 10 * 2
        u_bound += u_bound / 10 * 2
        LOWER_BOUND.append(l_bound)
        UPPER_BOUND.append(u_bound)
        g_len = math.ceil(math.log2(u_bound - l_bound + 1))
        GENOME_LEN.append(g_len)
        CHROMOSOME_LENGTH += g_len

    _CALIBRATED = True


def set_genome_len(v: typing.List[int]):
    global GENOME_LEN
    GENOME_LEN = v


def set_upper_bound(v: typing.List[float]):
    global UPPER_BOUND
    UPPER_BOUND = v


def set_lower_bound(v: typing.List[float]):
    global LOWER_BOUND
    LOWER_BOUND = v


def chromosome_to_point(ch: str, color=None) -> Point:
    dimension = len(GENOME_LEN)
    s_index = 0
    res = []
    for i in range(dimension):
        genome = ch[s_index: s_index + GENOME_LEN[i]]
        s_index = s_index + GENOME_LEN[i]
        num = int(genome, 2)
        res.append(
            LOWER_BOUND[i] + (num / ((2 ** GENOME_LEN[i]) - 1) * (UPPER_BOUND[i] - LOWER_BOUND[i]))
        )

    return Point(res, color=color)


def point_to_chromosome(p: Point) -> str:
    p_arr = p.to_arr()
    p_len = len(p_arr)

    chromosome = ''

    for i in range(p_len):
        genome = calc_genome(p_arr[i] - LOWER_BOUND[i])
        while len(genome) != GENOME_LEN[i]:
            genome += '0'

        chromosome += genome[::-1]

    return chromosome


def calc_chromosome(num: int) -> str:
    res = ''
    while num > 0:
        res += str(int(num % 2))
        num = num // 2

    while len(res) != CHROMOSOME_LENGTH:
        res += '0'

    return res[::-1]


def calc_genome(num) -> str:
    res = ''
    while num > 2:
        res += str(int(num % 2))
        num = num // 2

    return res


def arr_avg(num_arr: typing.Union[typing.List[int], typing.List[float]]) -> float:
    arr_sum = 0
    for num in num_arr:
        arr_sum += num

    return arr_sum / len(num_arr)
