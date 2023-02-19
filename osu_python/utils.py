import typing as t
import os
from time import time as now


def calculate_fade_in(ar: float) -> float:
    """Calculates fade_in time from AR"""
    if ar < 5:
        return 800 + 400 * (5 - ar) / 5

    if ar == 5:
        return 800

    if ar > 5:
        return 800 - 500 * (ar - 5) / 5


def calculate_preemt(ar: float) -> float:
    """Calculates preempt from AR"""
    if ar < 5:
        return 1200 + 600 * (5 - ar) / 5

    if ar == 5:
        return 1200

    if ar > 5:
        return 1200 - 750 * (ar - 5) / 5


def calculate_hit_r(cs: float) -> float:
    """
    Calculates hit circle radius from CS in osu!pixels
    Use convertion function to get size in pixels by using scaling
    """
    return 54.4 - 4.48 * cs


def calculate_appr_r(cs: float) -> float:
    """
    Calculates approach circle radius from CS in osu!pixels
    Use convertion function to get size in pixels by using scaling
    """
    return calculate_hit_r(cs) * 2


def playfield_size(h: int) -> t.Tuple[int, int]:
    """
    Calculates size of playfield
    from screen height
    """
    return ((4 / 3) * h * 0.9, h * 0.9)


def osu_scale(n: int) -> float:
    """
    Calculates scaling applied
    to osu!pixel values

    Parameters
    ----------
    n : int:
        Height of playfield (in px)
    """

    return n / 480


def calculate_hit_windows(od: float) -> t.Tuple[int, int, int]:
    """
    Calculates score from OD

    Returns tuple of time windows in ms
    of 300, 100 and 50 hit results
    """
    return (80 - 6 * od, 140 - 8 * od, 200 - 10 * od)


def calculate_accuracy(scores: t.Tuple[int, int, int, int]) -> float:
    """
    Calculates accuracy from hit scores

    Returns value between 0 and 1

    Parameters
    ----------
    scores: t.Tuple[int, int, int, int]
        All of the hit scores in descending order: 300, 100, 50, 0"""
    s300, s100, s50, _ = scores
    try:
        accuracy = (s300 * 300 + s100 * 100 + s50 * 50) / (300 * sum(scores))
    except ZeroDivisionError:
        accuracy = 1.0
    return accuracy


def calculate_difficulty_multiplier(
    HP: float, CS: float, OD: float, hit_objects_count: int, drain_time: float
):
    """
    Calculates map's difficulty multiplier

    Parameters
    ----------
    HP: float
        HP Drain of the map
    CS: float
        Circle Size of the map
    OD: float
        Overall Difficulty of the map
    hit_objects_count: int
        Amount of hit objects in the map
    drain_time: float
        Time period from first and last hit object in the map, not including breaks, in seconds
    """
    return round(
        HP + CS + OD + max(min(hit_objects_count / drain_time * 8, 16), 0) / 38 * 5
    )


def convert_type(value: str):
    value.split("//")[0]
    try:
        return int(value)
    except ValueError:
        pass

    l_values = value.split(",")
    length = len(l_values)
    if length != 1:
        return [convert_type(v) for v in l_values]

    return value.strip()


def parse_ini(path: os.PathLike):
    f = open(path, encoding="utf-8-sig")
    all_lines = f.readlines()
    category = None
    output = {"No category": []}
    for line in all_lines:
        if len(line) < 2:
            continue
        if line[0] == "[":
            category = line.strip()
            output[category] = {}
            continue
        if line[:2] == "//":
            continue
        try:
            key, value = line.split(":")
        except ValueError:
            if category == None:
                output["No category"].append(line.strip())
            continue
        key = key.strip()
        value = value.strip()
        if category != None:
            output[category][key] = convert_type(value)
        else:
            output["No category"].append(line)
    return output


def parse_additional_info(path: os.PathLike):
    f = open(path, encoding="utf-8-sig")
    all_lines = f.readlines()
    category = None
    colours = []
    obj_types = []
    for line in all_lines:
        if line.strip() == "[Colours]":
            category = "[Colours]"
            continue
        if line.strip() == "[HitObjects]":
            category = "[HitObjects]"
            continue
        if category == "[Colours]" and line.strip().startswith("Combo"):
            try:
                colour = line.split(":")[1]
                colours.append(convert_type(colour))
            except IndexError:
                continue
        if category == "[HitObjects]":
            if line.startswith("["):
                break
            obj_type = line.split(",")[3]
            obj_types.append(int(obj_type))
    return colours, obj_types


def chunks(lst, n):
    """Return continuous n-sized chunks from lst."""
    return [lst[i::n] for i in range(n)]
