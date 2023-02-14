import slider
import os
from osu_python.classes import game_object, Config
from osu_python import utils
from pathlib import Path
import zipfile
import logging
import typing as t
import pygame as pg
from osu_python.__main__ import width, height


log = logging.getLogger("map_loader")


def unpack(path: os.PathLike) -> bool:
    """
    Function for unpacking .osz file

    Parameters
    ----------
    path : os.PathLike
        Path to .osz file

    Returns
    -------
    Functions returns if map was successfully unpacked or not
    """
    logging.debug("unpacking beatmap from {}".format(path))
    try:
        f = zipfile.ZipFile(path, "r")

        path = "{}/songs/{}".format(Config.base_path, Path(path).name[:-4])
        os.mkdir(path)

        f.extractall(path)
        return True
    except Exception as e:
        logging.error(
            "error occurred when unpacking beatmap from {}: {}".format(path, e)
        )
        return False


def load_map(
    path: os.PathLike, scale: float, add_x: int, add_y: int, hit_callback: t.Callable
):
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
    callback : t.Callable
        Miss callback function

    Returns
    -------
    Functions returns tuple:
    (
        objects_queue,
        audio_path,
        background_path (Not implemented)
    )
    """
    log.debug("loading beatmap from {}".format(path))
    mp = slider.Beatmap.from_path(path)
    parent = Path(path).parent
    preempt = utils.calculate_preemt(mp.ar())
    fade_in = utils.calculate_fade_in(mp.ar())
    hit_size = utils.calculate_hit_r(mp.cs()) * scale * 2
    appr_size = utils.calculate_appr_r(mp.cs()) * scale * 2
    hit_windows = utils.calculate_hit_windows(mp.od())

    queue = []
    colours, obj_types = utils.parse_additional_info(path)
    objs = mp.hit_objects()
    log.debug("fetching objects ({})".format(len(objs)))
    color_index = 0
    combo_value = 0

    colours = check_colours(colours)
    slider_border = Config.skin_ini["[Colours]"]["SliderBorder"]

    for i, obj in enumerate(objs):
        if obj_types[i] & 4 or obj_types[i] & 8:
            combo_value = 0
            color_index = (color_index + 1) % len(colours)
        combo_value += 1
        if isinstance(obj, slider.beatmap.Circle):
            time = obj.time.total_seconds() * 1000
            queue.append(
                game_object.Circle(
                    time,
                    time - preempt,
                    time - preempt + fade_in,
                    (add_x + obj.position.x * scale, add_y + obj.position.y * scale),
                    combo_value,
                    colours[color_index],
                    (),
                    hit_size,
                    appr_size,
                    hit_windows,
                    hit_callback,
                )
            )

        if isinstance(obj, slider.beatmap.Slider):
            time = obj.time.total_seconds() * 1000
            endtime = obj.end_time.total_seconds() * 1000

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
                    combo_value,
                    colours[color_index],
                    (),
                    hit_size,
                    appr_size,
                    hit_windows,
                    hit_callback,
                    body,
                    endtime,
                    slider_border,
                )
            )

        if isinstance(obj, slider.beatmap.Spinner):
            time = obj.time.total_seconds() * 1000
            endtime = obj.end_time.total_seconds() * 1000
            hitsound = obj.hitsound

            queue.append(
                game_object.Spinner(
                    time,
                    time - preempt,
                    time - preempt + fade_in,
                    (int(width / 2), int(height / 2)),
                    (),
                    667,
                    1000,
                    hit_callback,
                    endtime,
                )
            )

            # TODO: calc sizes of spinner circles

    bg = get_background(path)
    return (queue, parent.joinpath(mp.audio_filename).absolute(), bg, mp)


def get_background(path: os.PathLike):
    f = open(path, encoding="utf-8-sig")
    all_lines = f.readlines()
    for i, line in enumerate(all_lines):
        if "[Events]" in line:
            str_path = str(path)
            bg_path = (
                path[: len(str_path) - len(str_path.split("/")[-1])]
                + all_lines[i + 2].split('"')[1]
            )
            break
    bg = None
    if bg_path:
        try:
            bg = pg.image.load(bg_path)
        except FileNotFoundError:
            log.warning("Map background was not found in map's directory")
            bg = pg.Surface((640, 480))
            bg.fill((0, 0, 0))
    return bg


def check_colours(colours: t.List) -> t.List:
    if colours == []:
        skin_colours = Config.skin_ini["[Colours]"]
        return [
            color for name, color in skin_colours.items() if name.startswith("Combo")
        ]
    return colours
