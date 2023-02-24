import pygame as pg
from osu_python.classes import Config
from osu_python.classes import ui
import random


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
    draw_background(screen)
    draw_title(screen)
    draw_ranking_panel(screen)


def setup(_height, _width, _screen, _diff_path, _retry_func, _rank, _draw_bg_func, _score, _results, _combo, _accuracy):
    global height, width, screen, diff_path, retry_func, rank, draw_bg_func, score, results, combo, accuracy, btn_retry, btn_replay, mgr_btns, ranking_panel, ranking_title, h_title, h_panel

    height = _height
    width = _width
    screen = _screen
    diff_path = _diff_path
    retry_func = _retry_func
    rank = _rank
    draw_bg_func = _draw_bg_func
    score = _score
    results = _results
    combo = _combo
    accuracy = _accuracy

    h_title = round(height * (2 / 13))
    h_panel = round(width * (11 / 13))

    btn_retry = ui.ranking.ButtonRetry(height, width)
    btn_replay = ui.ranking.ButtonReplay(height, width)

    mgr_btns = ui.root.UiManager([btn_retry, btn_replay])

    im = pg.image.load(Config.base_path + "/skins/" + Config.cfg["skin"] + "/ranking_title.png")
    w_size = h_title / im.get_height() * im.get_width() 
    ranking_title = pg.transform.scale(im, (w_size, h_title))

    im = pg.image.load(Config.base_path + "/skins/" + Config.cfg["skin"] + "/ranking_panel.png")
    w_size = h_panel / im.get_height() * im.get_width()
    ranking_panel = pg.transform.scale(im, (w_size, h_title))


def tick(dt, events):
    update(events)
    draw(screen)


def draw_background(screen):
    draw_bg_func()


def draw_title(screen):
    pg.draw.rect(screen, (0, 0, 0) (0, 0, width, h_title))
    screen.blit(ranking_title,
        (round(width * (12.5 / 17.5)), h_title)
    )
    # TODO: beatmap_title


def draw_ranking_panel(screen):
    screen.blit(ranking_panel, (0, h_panel))
    # TODO: draw score, results, combo and accuracy
