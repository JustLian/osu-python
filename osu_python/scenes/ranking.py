import pygame as pg
from osu_python.classes import Config
from osu_python.classes import ui


all_objects = []


def click(mouse_pos):
    for obj in all_objects:
        if obj.rect.collidepoint(mouse_pos):
            obj.click()


def update(events):
    for event in events:
        if (Config.cfg['mouse_buttons'] and event.type == pg.MOUSEBUTTONDOWN) or (
            event.type == pg.KEYDOWN
            and int(event.key)
            in [Config.cfg["keys"]["key1"], Config.cfg["keys"]["key2"]]
        ):
            click(pg.mouse.get_pos())


def draw(screen):
    for obj in all_objects:
        obj.draw()


def setup(_height, _width, _screen, _diff_path, _retry_func, _rank):
    global height, width, screen, diff_path, retry_func, rank

    height = _height
    width = _width
    screen = _screen
    diff_path = _diff_path
    retry_func = _retry_func
    rank = _rank


def tick(dt, events):
    update(events)
    draw(screen)
