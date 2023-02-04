import slider
import os
from osu_python.classes import game_object, Config
from osu_python import utils
from pathlib import Path
import zipfile


def unpack(path: os.PathLike):
    """
    Function for unpacking .osz file

    Parameters
    ----------
    path : os.PathLike
        Path to .osz file
    """
    f = zipfile.ZipFile(path, "r")

    path = "{}/songs/{}".format(Config.base_path, Path(path).name)
    os.mkdir(path)

    f.extractall(path)


def load_map(path: os.PathLike, scale: float, add_x: int, add_y: int):
    """
    Function for loading difficulty of beatmap

    Parameters
    ----------
    path : os.PathLike
        Path to .osu file. It should be stored in beatmap folder
        with song file, background and other
    scale : float
        Scale applied to osu!px values
    add_x : int
        Horizontal playfield offset
    add_y : int:
        Vertical playfield offset

    Returns
    -------
    Functions returns tuple:
    (
        objects_queue,
        audio_path,
        background_path (Not implemented)
    )
    """
    mp = slider.Beatmap.from_path(path)
    parent = Path(path).parent
    preempt = utils.calculate_preemt(mp.ar())
    fade_in = utils.calculate_fade_in(mp.ar())
    hit_size = utils.calculate_hit_r(mp.cs()) * scale * 2
    appr_size = utils.calculate_appr_r(mp.cs()) * scale * 2
    hit_windows = utils.calculate_hit_windows(mp.od())

    queue = []
    for obj in mp.hit_objects():
        if isinstance(obj, slider.beatmap.Circle):
            time = obj.time.total_seconds() * 1000
            queue.append(
                game_object.Circle(
                    time,
                    time - preempt,
                    time - preempt + fade_in,
                    (add_x + obj.position.x * scale, add_y + obj.position.y * scale),
                    False,
                    (),
                    hit_size,
                    appr_size,
                    hit_windows,
                )
            )

        if isinstance(obj, slider.beatmap.Slider):
            time = obj.time.total_seconds() * 1000

            body = []
            for n in range(100):
                c = obj.curve(n / 100)
                body.append((round(add_x + c.x * scale), round(add_y + c.y * scale)))

            queue.append(
                game_object.Slider(
                    time,
                    time - preempt,
                    time - preempt + fade_in,
                    (add_x + obj.position.x * scale, add_y + obj.position.y * scale),
                    False,
                    (),
                    hit_size,
                    appr_size,
                    hit_windows,
                    body,
                )
            )
    return (queue, parent.joinpath(mp.audio_filename).absolute(), None)
