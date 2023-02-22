import pygame as pg
from osu_python.classes import Library
import random
from osu_python.classes.ui import beatmap_choosing as bmc
from osu_python import map_loader, utils


BUFFER_CARDS = 3


def change_bms(new_bms_index, new_diff_index):
    global bms_index, diff_index, old_bg, old_bms_index, bg

    old_bms_index, bms_index = bms_index, new_bms_index
    diff_index = new_diff_index
    dp = Library.path_for_diff(Library.db.get(doc_id=bms_index), diff_index)
    old_bg, bg = bg, utils.fit_image_to_screen(
        map_loader.get_background(dp),
        (width, height)
    ).convert_alpha()
    bg.set_alpha(120)


def update(events):
    global scroll
    for event in events:
        if event.type == pg.MOUSEWHEEL:
            scroll[2] += event.y * 10
            scroll[0] += abs(event.y * 10)

    return
    # TODO: fix this pls
    if cards_below > BUFFER_CARDS:
        for _ in range(cards_below - BUFFER_CARDS):
            cards.pop(-1)
        for _ in range(BUFFER_CARDS - cards_above):
            d = Library.db.get(doc_id=bms_index + _cur)
            while d is None or 'diffs' not in d or d['diffs'] == []:
                _cur += 1
                _lim += 1
                d = Library.db.get(doc_id=bms_index + _cur)

            data.append(d)
            cards.insert(
                0, bmc.BeatmapSetCard(
                    bms_index + _cur, bms_card_height, font,
                    height_constant
                )
            )
            _cur += 1


def draw(dt: float):
    global scroll, cards_above, cards_below
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    lh = bms_card_height // 2
    scroll[1] = max(min(scroll[2] + scroll[1], bms_card_height * 3.7), -bms_card_height * len(cards) + bms_card_height * 3.7)
    scroll[0] *= 0.95
    scroll[2] *= 0.9
    cards_below, cards_above = 0, 0
    for card in cards:
        r = card.draw(lh, screen, 0, scroll)
        if r is True:
            cards_below += 1
        if r is False:
            cards_above += 1
        lh += bms_card_height * 1.01


def setup(_height, _width, _screen: pg.Surface, _bms_index: int, _diff_index: int):
    global height, width, screen, old_bg, old_bms_index, bms_index, diff_index, bg, bms_card_height, cards, scroll, cards_above, cards_below, font, data, height_constant
    height = _height
    width = _width
    screen = _screen
    # x, y, y_xeleration
    scroll = [0, 0, 0]

    cards_above, cards_below = 0, 0

    bms_index = -1
    diff_index = -1
    bg = None

    old_bms_index = -1
    old_bg = pg.Surface((width, height))
    old_bg.fill((0, 0, 0))

    data = []
    cards = []
    bms_card_height = height // 8
    height_constant = bms_card_height * 0.035
    font = pg.font.Font('./ui/aller_light.ttf', round(bms_card_height * .5))
    _cur, _lim = -BUFFER_CARDS - 4, BUFFER_CARDS + 4
    while _cur <= _lim:
        d = Library.db.get(doc_id=bms_index + _cur)
        while d is None or 'diffs' not in d or d['diffs'] == []:
            _cur += 1
            _lim += 1
            d = Library.db.get(doc_id=bms_index + _cur)

        data.append(d)
        cards.append(
            bmc.BeatmapSetCard(
                bms_index + _cur, bms_card_height, font,
                height_constant
            )
        )
        _cur += 1

    change_bms(_bms_index, _diff_index)


def tick(dt: float, events):
    draw(dt)
    update(events)
