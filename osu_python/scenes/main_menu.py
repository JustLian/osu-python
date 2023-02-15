from logging import getLogger
import pygame as pg
from glob import glob
from random import choice
from osu_python import utils
from osu_python.classes import ui
import audio2numpy as a2n


log = getLogger('scenes/main_menu')


def load_music(path):
    return a2n.audio_from_file(path)


def calc_bg_offset(pos):
    return (
        (pos[0] - width // 2) * .008,
        (pos[1] - height // 2) * .008
    )


def setup(_height, _width, _screen: pg.Surface):
    global height, width, screen, bg, logo, mgr, global_bg_offset
    height = _height
    width = _width
    screen = _screen

    # loading background
    global_bg_offset = calc_bg_offset((0, 0))
    bg = utils.fit_image_to_screen(
        pg.image.load(choice(glob('./ui/backgrounds/*'))),
        (width - global_bg_offset[0] * 2, height - global_bg_offset[1] * 2)
    ).convert()

    # osu! logo
    logo = ui.main_menu.OsuLogo(width, height)

    # setting up ui manager
    mgr = ui.root.UiManager([logo])


def draw(dt):
    offset = calc_bg_offset(pg.mouse.get_pos())
    screen.blit(bg, (
        global_bg_offset[0] + offset[0],
        global_bg_offset[1] + offset[1]
    ))
    mgr.draw(screen, dt)


def tick(dt: float, events):
    draw(dt)
    mgr.update(events)