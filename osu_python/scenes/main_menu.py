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


def setup(_height, _width, _screen: pg.Surface):
    global height, width, screen, bg, logo, mgr
    height = _height
    width = _width
    screen = _screen

    # loading background
    bg = utils.fit_image_to_screen(
        pg.image.load(choice(glob('./ui/backgrounds/*'))),
        (width, height)
    ).convert()

    # osu! logo
    logo = ui.main_menu.OsuLogo(width, height)

    # setting up ui manager
    mgr = ui.root.UiManager([logo])


def draw(dt):
    screen.blit(bg, (0, 0))
    mgr.draw(screen, dt)


def tick(dt: float, events):
    draw(dt)
    mgr.update(events)