import typing as t


def calculate_ar(ar: float) -> t.Tuple[float, float]:
    """Calculates preempt and fade_in time from AR"""
    if ar < 5:
        return (1200 + 600 * (5 - ar) / 5, 800 + 400 * (5 - ar) / 5)

    if ar == 5:
        return (1200, 800)

    if ar > 5:
        return (1200 - 750 * (ar - 5) / 5, 800 - 500 * (ar - 5) / 5)


def calculate_hit_r(cs: float) -> float:
    """
    Calculates hit circle radius from CS in osu!pixels
    Use convertion function to get size in pixels
    """
    return 54.4 - 4.48 * cs


def calculate_appr_r(cs: float) -> float:
    """
    Calculates approach circle radius from CS in osu!pixels
    Use convertion function to get size in pixels
    """
    return calculate_hit_r(cs) * 2


def playfield_size(h: int) -> t.Tuple[int, int]:
    """
    Calculates size of playfield
    from screen height
    """
    return (
        (h * 4) // 3, h
    )


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