from logging import getLogger
import pygame as pg
from osu_python import utils
from osu_python.classes import ui, game_object
from osu_python.scenes import std


def setup(_height, _width, _screen: pg.Surface, is_fall):
    global height, width, screen, bg, mgr
    height = _height
    width = _width
    screen = _screen

    bg = std.bg

    btn_retry = ui.pause.ButtonRetry(height, width)
    btn_back = ui.pause.ButtonBack(height, width)

    if is_fall:
        mgr = ui.root.UiManager([btn_retry, btn_back])
    
    else:
        btn_play = ui.pause.ButtonContinue(height, width)

        mgr = ui.root.UiManager([btn_play, btn_retry, btn_back])


def draw(dt):
    mgr.draw(screen, dt)


def tick(dt: float, events):
    draw(dt)
    mgr.update(events)
