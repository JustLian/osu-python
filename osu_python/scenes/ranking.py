import pygame as pg
from osu_python.classes import Config
from osu_python.classes import ui
from datetime import datetime


all_objects = []


def click(mouse_pos):
    for obj in all_objects:
        if obj.rect.collidepoint(mouse_pos):
            obj.click()


def update(events):
    for event in events:
        if (Config.cfg["mouse_buttons"] and event.type == pg.MOUSEBUTTONDOWN) or (
            event.type == pg.KEYDOWN
            and int(event.key)
            in [Config.cfg["keys"]["key1"], Config.cfg["keys"]["key2"]]
        ):
            click(pg.mouse.get_pos())


def draw(screen):
    draw_background(screen)
    draw_title(screen)
    draw_ranking_panel(screen)


def setup(
    _height,
    _width,
    _screen,
    _name_btm,
    _author,
    _retry_func,
    _rank,
    _draw_bg_func,
    _score,
    _results,
    _combo,
    _accuracy,
):
    global height, width, screen, name_btm, author, retry_func, btm_name, btm_author, btm_player, rank, draw_bg_func, score, results, combo, accuracy, btn_retry, btn_replay, btn_back, mgr_btns, ranking_panel, ranking_title, h_title, h_panel, w_title

    height = _height
    width = _width
    screen = _screen
    retry_func = _retry_func
    rank = _rank
    draw_bg_func = _draw_bg_func
    score = _score
    results = _results
    combo = _combo
    accuracy = _accuracy

    name_btm = _name_btm
    author = _author

    h_title = round(height * (2 / 13))
    h_panel = round(width * (11 / 13))

    w_title = round(width * (12 / 17.5))

    font1 = pg.font.Font("./ui/aller_light.ttf", round(h_title * 0.3))

    font2 = pg.font.Font("./ui/aller_light.ttf", round(h_title * 0.17))

    btm_name = font1.render(name_btm, True, (255, 255, 255))
    btm_author = font2.render("Beatmap by " + author, True, (255, 255, 255))
    btm_player = font2.render(
        "Played by guest on " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        True,
        (255, 255, 255),
    )

    ui.ranking.load_skin()

    btn_retry = ui.ranking.ButtonRetry(height, width)
    btn_replay = ui.ranking.ButtonReplay(height, width)
    btn_back = ui.ranking.ButtonBack(height, width)

    mgr_btns = ui.root.UiManager([btn_retry, btn_replay, btn_back])

    im = pg.image.load(
        Config.base_path + "/skins/" + Config.cfg["skin"] + "/ranking-title.png"
    ).convert_alpha()
    w_size = h_title / im.get_height() * im.get_width()
    ranking_title = pg.transform.scale(im, (w_size, h_title))

    im = pg.image.load(
        Config.base_path + "/skins/" + Config.cfg["skin"] + "/ranking-panel.png"
    ).convert_alpha()
    w_size = h_panel / im.get_height() * im.get_width()
    ranking_panel = pg.transform.scale(im, (w_size, h_title))


def tick(dt, events):
    update(events)
    draw(screen)

    mgr_btns.update(events)
    mgr_btns.draw(screen, dt)


def draw_background(screen):
    # draw_bg_func()
    screen.fill((0, 0, 0))


def draw_title(screen):
    pg.draw.rect(screen, (0, 0, 0), (0, 0, width, h_title))

    screen.blit(ranking_title, (w_title, 0))

    screen.blit(btm_name, (0, 0))
    screen.blit(btm_author, (0, h_title * 0.3))
    screen.blit(btm_player, (0, h_title * 0.45))


def draw_ranking_panel(screen):
    screen.blit(ranking_panel, (0, h_panel))
    # TODO: draw score, results, combo and accuracy
