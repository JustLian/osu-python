from logging import getLogger
import pygame as pg
from glob import glob
from random import choice
from osu_python import utils
import audio2numpy as a2n


log = getLogger('scenes/main_menu')


def load_music(path):
    return a2n.audio_from_file(path)


def setup(_height, _width, _screen: pg.Surface):
    global height, width, screen, bg, logo
    height = _height
    width = _width
    screen = _screen

    # loading background
    bg = utils.fit_image_to_screen(
        pg.image.load(choice(glob('./ui/backgrounds/*'))),
        (width, height)
    )

    # osu! logo
    logo = pg.transform.scale(
        pg.image.load('./ui/menu/logo.png'),
        (height * .8, height * .8)
    )


def draw():
    screen.blit(bg, (0, 0))


def tick(dt: float, events):
    draw()