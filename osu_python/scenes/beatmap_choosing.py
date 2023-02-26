import pygame as pg
from osu_python.classes import Library
from osu_python.classes.ui import beatmap_choosing as bmc
from osu_python.classes.ui import root
from osu_python.classes.ui.ranking import ButtonBack, load_skin
from osu_python import map_loader, utils, scenes


BUFFER_CARDS = 3


def change_bms(new_bms_index, new_diff_index):
    global bms_index, diff_index, old_bg, old_bms_index, bg

    old_bms_index, bms_index = bms_index, new_bms_index
    diff_index = new_diff_index
    dp = Library.path_for_diff(Library.db.get(doc_id=bms_index), diff_index)
    old_bg, bg = (
        bg,
        utils.fit_image_to_screen(
            map_loader.get_background(dp), (width, height)
        ).convert_alpha(),
    )
    bg.set_alpha(120)


def update(events, dt):
    global scroll, lock_above, lock_below

    mgr.update(events)
    diff_mgr.update_x_offset(dt)
    if btn_back.clicked:
        func2(scenes.main_menu, func2)

    mouse = pg.mouse.get_pos()
    for event in events:
        if event.type == pg.MOUSEWHEEL:
            if mouse[0] <= diff_mgr.el_offset + diff_mgr.w:
                diff_mgr.update_scroll(event.y)
            else:
                scroll[2] += event.y * 10
                scroll[0] += abs(event.y * 10)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            m = pg.mouse.get_pos()
            for c in cards:
                if c.is_colliding(m):
                    diff_mgr.update(c.data)
                    break

    if not lock_above and cards_above < BUFFER_CARDS and BUFFER_CARDS - cards_above < 3:
        if add_card_above():
            cards.pop(-1)
            lock_below = False
        else:
            lock_above = True

    if not lock_below and cards_below < BUFFER_CARDS and BUFFER_CARDS - cards_below < 3:
        if add_card_below():
            cards.pop(0)
            lock_above = False
        else:
            lock_below = True


def add_card_above():
    _last_index = cards[0].index
    _cur, _lim = 1, BUFFER_CARDS - cards_above
    while _cur <= _lim:
        d = Library.db.get(doc_id=_last_index + _cur)
        _exit = False
        while d is None or "diffs" not in d or d["diffs"] == []:
            _cur += 1
            _lim += 1
            if _cur >= len(Library.db):
                _exit = True
                break
            d = Library.db.get(doc_id=_last_index + _cur)
        if _exit:
            return 0

        cards.insert(
            0,
            bmc.BeatmapSetCard(
                _last_index + _cur, bms_card_height, font, height_constant
            ),
        )
        _cur += 1
        scroll[1] -= bms_card_height
        return 1


def add_card_below():
    _last_index = cards[-1].index
    _cur, _lim = -1, -BUFFER_CARDS + cards_below
    while _cur >= _lim:
        d = Library.db.get(doc_id=_last_index + _cur)
        _exit = False
        while d is None or "diffs" not in d or d["diffs"] == []:
            _cur -= 1
            _lim -= 1
            if _last_index + _cur < 0:
                _exit = True
                break
            d = Library.db.get(doc_id=_last_index + _cur)
        if _exit:
            return 0

        cards.append(
            bmc.BeatmapSetCard(
                _last_index + _cur, bms_card_height, font, height_constant
            )
        )
        _cur -= 1
        scroll[1] += bms_card_height
        return 1


def draw(dt: float):
    global scroll, cards_above, cards_below
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    mgr.draw(screen, dt)

    lh = bms_card_height // 2
    scroll[1] = max(
        min(scroll[2] + scroll[1], bms_card_height * 3.7),
        -bms_card_height * len(cards) + bms_card_height * 3.7,
    )
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


def setup(
    _height, _width, _screen: pg.Surface, _bms_index: int, _diff_index: int, func
):
    global height, width, screen, old_bg, old_bms_index, bms_index, diff_index, bg, bms_card_height, cards, scroll, cards_above, cards_below, font, data, height_constant, lock_above, lock_below, diff_mgr, mgr, btn_back, func2
    height = _height
    width = _width
    screen = _screen
    func2 = func

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
    # x, y, y_xeleration
    scroll = [0, bms_card_height * -4, 0]
    lock_below = False
    lock_above = False
    font = pg.font.Font("./ui/aller_light.ttf", round(bms_card_height * 0.5))
    _cur, _lim = -BUFFER_CARDS - 4, BUFFER_CARDS + 4
    while _cur <= _lim:
        d = Library.db.get(doc_id=bms_index + _cur)
        while d is None or "diffs" not in d or d["diffs"] == []:
            _cur += 1
            _lim += 1
            d = Library.db.get(doc_id=bms_index + _cur)

        data.append(d)
        cards.append(
            bmc.BeatmapSetCard(bms_index + _cur, bms_card_height, font, height_constant)
        )
        _cur += 1

    load_skin()
    btn_back = ButtonBack(height, width)
    mgr = root.UiManager([btn_back])
    diff_mgr = bmc.DifficultyManager(height, func, font, mgr)
    change_bms(_bms_index, _diff_index)


def tick(dt: float, events):
    draw(dt)
    update(events, dt)
