from logging import getLogger
import pygame as pg
from glob import glob
from random import choice
from osu_python import utils
from osu_python.classes import ui
from osu_python import scenes


log = getLogger("scenes/main_menu")


def calc_bg_offset(pos):
    return ((pos[0] - width // 2) * 0.008, (pos[1] - height // 2) * 0.008)


def setup(_height, _width, _screen: pg.Surface, play_fn):
    global height, width, screen, bg, logo, mgr, global_bg_offset
    height = _height
    width = _width
    screen = _screen

    # loading background
    global_bg_offset = calc_bg_offset((0, 0))
    bg = utils.fit_image_to_screen(
        pg.image.load(choice(glob("./ui/backgrounds/*"))),
        (width - global_bg_offset[0] * 2, height - global_bg_offset[1] * 2),
    ).convert()

    # osu! logo
    logo = ui.main_menu.OsuLogo(width, height)

    btns_font = pg.font.Font("./ui/torus.otf", round(height * 0.3 * 0.25 * 0.25))

    def play_click_fn():
        play_fn(scenes.beatmap_choosing, logo.bm, 0, play_fn)

    btn_play = ui.main_menu.Button(
        True,
        logo,
        logo,
        pg.image.load("./ui/menu/icons/osu.png").convert_alpha(),
        "play",
        (102, 68, 204),
        width,
        height,
        btns_font,
        play_click_fn,
    )
    btn_exit = ui.main_menu.Button(
        False,
        btn_play,
        logo,
        pg.image.load("./ui/menu/icons/exit.png").convert_alpha(),
        "exit",
        (238, 51, 154),
        width,
        height,
        btns_font,
        exit,
    )

    # setting up ui manager
    mgr = ui.root.UiManager([logo, btn_exit, btn_play])


def draw(dt):
    offset = calc_bg_offset(pg.mouse.get_pos())
    screen.blit(bg, (global_bg_offset[0] + offset[0], global_bg_offset[1] + offset[1]))
    mgr.draw(screen, dt)


def tick(dt: float, events):
    draw(dt)
    mgr.update(events)
