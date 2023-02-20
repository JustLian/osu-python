import pygame as pg
from osu_python.classes import Library
import random
from osu_python.classes.ui import beatmap_choosing as bmc
from osu_python import map_loader, utils


def change_bms(new_bms_index, new_diff_index):
    global bms_index, diff_index, old_bg, old_bms_index, bg

    old_bms_index, bms_index = bms_index, new_bms_index
    dp = Library.path_for_diff(Library.db.get(doc_id=bms_index), diff_index)
    old_bg, bg = bg, utils.fit_image_to_screen(
        map_loader.get_background(dp),
        (width, height)
    )


def draw(dt: float):
    screen.blit(bg, (0, 0))
    screen.fill((0, 0, 0))

    lh = bms_card_height // 2
    for card in cards:
        card.draw(lh, screen, 0)
        lh += bms_card_height * 1.01


def setup(_height, _width, _screen: pg.Surface, _bms_index: int, _diff_index: int):
    global height, width, screen, old_bg, old_bms_index, bms_index, diff_index, bg, bms_card_height, cards
    height = _height
    width = _width
    screen = _screen

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
    for _ in range(8):
        d = {'broken': 1}
        while 'broken' in d:
            index = random.randint(0, 999)
            d = Library.db.get(doc_id=index)
        data.append(d)
        cards.append(
            bmc.BeatmapSetCard(
                index, bms_card_height, font,
                height_constant
            )
        )

    change_bms(_bms_index, _diff_index)


def tick(dt: float, events):
    draw(dt)