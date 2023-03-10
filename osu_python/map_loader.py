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
from osu_python.classes.game_object import Spinner
from glob import glob


log = logging.getLogger("map_loader")


def update():
    """Loads all new .osz files from `songs` dir"""
    new = glob(Config.base_path + "/songs/*.osz")
    log.info("found {} .osz files. Unpacking...".format(len(new)))
    for o in new:
        unpack(o)
        os.remove(o)


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
    hit_callback : t.Callable
        Hit callback function

    Returns
    -------
    Functions returns tuple:
    (
        objects_queue,
        audio_path,
        background_path
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
            point_count = round(obj.length / 8)
            for n in range(point_count):
                c = obj.curve(n / point_count)
                body.append((add_x + c.x * scale, add_y + c.y * scale))

            tick_points = []
            for p in obj.tick_points:
                tick_points.append(
                    (
                        add_x + p.x * scale,
                        add_y + p.y * scale,
                        p.offset.total_seconds() * 1000,
                    )
                )

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
                    tick_points,
                    obj.repeat,
                )
            )

        if isinstance(obj, slider.beatmap.Spinner):
            continue
            time = obj.time.total_seconds() * 1000
            endtime = obj.end_time.total_seconds() * 1000
            hitsound = obj.hitsound

            bottom_top_size = round(0.75 * height)
            appr_size = round(0.9 * height)

            coeff = bottom_top_size / Spinner.bottom_img.get_size()[0]

            glow_size = Spinner.glow_img.get_size()[0] * coeff
            middle_size = Spinner.middle_img.get_size()[0] * coeff
            middle2_size = Spinner.middle2_img.get_size()[0] * coeff
            spin_size = (
                Spinner.spin_img.get_size()[0] * coeff,
                Spinner.spin_img.get_size()[1] * coeff,
            )
            clear_size = (
                Spinner.clear_img.get_size()[0] * coeff,
                Spinner.clear_img.get_size()[1] * coeff,
            )

            queue.append(
                game_object.Spinner(
                    time,
                    time - preempt,
                    time - preempt + fade_in,
                    endtime,
                    bottom_top_size,
                    glow_size,
                    middle_size,
                    middle2_size,
                    spin_size,
                    clear_size,
                    appr_size,
                    (int(width / 2), int(height / 2)),
                    (),
                    hit_callback,
                    hit_size,
                )
            )

    bg = get_background(path)
    return (queue, parent.joinpath(mp.audio_filename).absolute(), bg, mp)


def get_background(path: os.PathLike):
    bg = pg.Surface((640, 480))
    bg.fill((0, 0, 0))
    try:
        f = open(path, encoding="utf-8-sig")
    except FileNotFoundError:
        log.warning("Map background was not found in map's directory")
        return bg

    bg_path = None
    all_lines = f.readlines()
    for i, line in enumerate(all_lines):
        if "[Events]" in line:
            for i2 in range(20):
                i3 = i2 + i
                if all_lines[i3].startswith("0,0,"):
                    str_path = str(path)
                    bg_path = (
                        path[: len(str_path) - len(str_path.split(Config.path_sep)[-1])]
                        + all_lines[i3].split('"')[1]
                    )
                    break
    if bg_path:
        try:
            bg = pg.image.load(bg_path)
        except FileNotFoundError:
            log.warning("Map background was not found in map's directory")
            bg = pg.Surface((2, 2))
            bg.fill((0, 0, 0))
    return bg


def check_colours(colours: t.List) -> t.List:
    if colours == []:
        skin_colours = Config.skin_ini["[Colours]"]
        return [
            color for name, color in skin_colours.items() if name.startswith("Combo")
        ]
    return colours
