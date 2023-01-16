import typing as t


def calculate_fade_in(ar: float) -> t.Tuple[float, float]:
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

    return n / 384


def pixel_horizontal_scaling(m: int) -> float:
    """
    Calculates horizontal scaling applied
    to x coord of osu!pixel

    Parameters
    ----------
    m : int:
        Width of playfield (in px)
    """
    return m / 512


def pixel_vertical_scaling(n: int) -> float:
    """
    Calculates vertical scaling applied
    to y coord of osu!pixel

    Parameters
    ----------
    n : int:
        Height of playfield (in px)
    """
    return n / 384


def calculate_hit_windows(od: float) -> t.Tuple[int, int, int]:
    """
    Calculates score from OD

    Returns tuple of time windows in ms
    of 300, 100 and 50 hit results
    """
    return (80 - 6 * od, 140 - 8 * od, 200 - 10 * od)
