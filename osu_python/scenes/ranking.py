import pygame as pg
from osu_python.classes import Config
from osu_python.classes import ui
from datetime import datetime
from osu_python import utils


all_objects = []
nums_imgs = None
score_overlap = 0
combo_overlap = 0
score_300_img = None
score_100_img = None
score_50_img = None
miss_img = None
combo_numbers = None
ranking_img = None


def load_numbers_skin():
    global nums_imgs, score_overlap, combo_overlap, score_300_img, score_100_img, score_50_img, miss_img, combo_numbers, ranking_img
    path = Config.base_path + "/skins/" + Config.cfg["skin"]
    score_path = (
        path + "/" + Config.skin_ini["[Fonts]"]["ScorePrefix"].replace("\\", "/")
    )
    combo_path = (
        path + "/" + Config.skin_ini["[Fonts]"]["HitCirclePrefix"].replace("\\", "/")
    )

    nums_imgs = {
        "0": pg.image.load(score_path + "-0.png").convert_alpha(),
        "1": pg.image.load(score_path + "-1.png").convert_alpha(),
        "2": pg.image.load(score_path + "-2.png").convert_alpha(),
        "3": pg.image.load(score_path + "-3.png").convert_alpha(),
        "4": pg.image.load(score_path + "-4.png").convert_alpha(),
        "5": pg.image.load(score_path + "-5.png").convert_alpha(),
        "6": pg.image.load(score_path + "-6.png").convert_alpha(),
        "7": pg.image.load(score_path + "-7.png").convert_alpha(),
        "8": pg.image.load(score_path + "-8.png").convert_alpha(),
        "9": pg.image.load(score_path + "-9.png").convert_alpha(),
        ".": pg.image.load(score_path + "-dot.png").convert_alpha(),
        "%": pg.image.load(score_path + "-percent.png").convert_alpha(),
        "x": pg.image.load(score_path + "-x.png").convert_alpha(),
    }

    try:
        score_overlap = Config.skin_ini["[Fonts]"]["ScoreOverlap"]
    except KeyError:
        pass

    try:
        combo_overlap = Config.skin_ini["[Fonts]"]["ComboOverlap"]
    except KeyError:
        pass

    score_300_img = pg.image.load(path + "/hit300.png").convert_alpha()
    score_100_img = pg.image.load(path + "/hit100.png").convert_alpha()
    score_50_img = pg.image.load(path + "/hit50.png").convert_alpha()
    miss_img = pg.image.load(path + "/hit0.png").convert_alpha()
    combo_numbers = {
        "0": pg.image.load(combo_path + "-0.png").convert_alpha(),
        "1": pg.image.load(combo_path + "-1.png").convert_alpha(),
        "2": pg.image.load(combo_path + "-2.png").convert_alpha(),
        "3": pg.image.load(combo_path + "-3.png").convert_alpha(),
        "4": pg.image.load(combo_path + "-4.png").convert_alpha(),
        "5": pg.image.load(combo_path + "-5.png").convert_alpha(),
        "6": pg.image.load(combo_path + "-6.png").convert_alpha(),
        "7": pg.image.load(combo_path + "-7.png").convert_alpha(),
        "8": pg.image.load(combo_path + "-8.png").convert_alpha(),
        "9": pg.image.load(combo_path + "-9.png").convert_alpha(),
    }
    ranking_img = pg.image.load(path + f"/ranking-{rank}.png").convert_alpha()


def click(mouse_pos):
    for obj in all_objects:
        if obj.rect.collidepoint(mouse_pos):
            obj.click()


def update(events):
    if btn_back.clicked:
        back_to_menu()
    if btn_retry.clicked:
        retry_func()
    for event in events:
        if (Config.cfg["mouse_buttons"] and event.type == pg.MOUSEBUTTONDOWN) or (
            event.type == pg.KEYDOWN
            and int(event.key)
            in [Config.cfg["keys"]["key1"], Config.cfg["keys"]["key2"]]
        ):
            click(pg.mouse.get_pos())


def setup(
    _height,
    _width,
    _screen,
    _name_btm,
    _author,
    _retry_func,
    _back_to_menu,
    _rank,
    _bg,
    _score,
    _results,
    _combo,
    _accuracy,
):
    global height, width, screen, name_btm, author, retry_func, btm_name, btm_author, btm_player, rank, bg, score, results, combo, accuracy, btn_retry, btn_replay, btn_back, mgr_btns, ranking_panel, ranking_title, h_title, h_panel, w_title, back_to_menu

    height = _height
    width = _width
    screen = _screen
    retry_func = _retry_func
    back_to_menu = _back_to_menu
    rank = _rank
    bg = _bg
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

    load_numbers_skin()
    ui.ranking.load_skin()

    btn_retry = ui.ranking.ButtonRetry(height, width)
    btn_back = ui.ranking.ButtonBack(height, width)

    mgr_btns = ui.root.UiManager([btn_retry, btn_back])

    try:
        im = pg.image.load(
            Config.base_path + "/skins/" + Config.cfg["skin"] + "/ranking-title.png"
        ).convert_alpha()
    except FileNotFoundError:
        im = pg.image.load(
            Config.base_path + "/skins/default/ranking-title.png"
        ).convert_alpha()
    w_size = h_title / im.get_height() * im.get_width()
    ranking_title = pg.transform.scale(im, (w_size, h_title))

    im = pg.image.load(
        Config.base_path + "/skins/" + Config.cfg["skin"] + "/ranking-panel.png"
    ).convert_alpha()
    w_size = h_panel / im.get_height() * im.get_width()
    ranking_panel = pg.transform.scale(im, (w_size, h_title))


def draw(screen):
    draw_background(screen)
    draw_title(screen)
    draw_ranking_panel(screen)
    draw_rank(screen)
    draw_accuracy(screen)
    draw_score(screen)
    draw_combo(screen)
    draw_scores(screen)


def draw_rank(screen):
    scaling = (height * 0.6) / ranking_img.get_height()
    img = pg.transform.scale(ranking_img, (ranking_img.get_width() * scaling, ranking_img.get_height() * scaling))
    screen.blit(img, (width * 0.9 - img.get_width(), height * 0.9 - img.get_height()))


def draw_accuracy(screen):
    offset_x = screen.get_width() * 0.4
    _accuracy = str(round(accuracy * 100, 1)) + "%"
    for v in reversed(_accuracy):
        gap = nums_imgs[v].get_width() - score_overlap
        offset_x -= gap
        screen.blit(
            nums_imgs[v], (offset_x + (gap - nums_imgs[v].get_width()) / 2, height * 0.8)
        )


def draw_score(screen):
    _score = str(score)
    numbers = "0" * (8 - len(_score)) + _score

    offset_x = width * 0.3
    for v in reversed(numbers):
        offset_x -= nums_imgs["0"].get_width() - score_overlap
        screen.blit(
            nums_imgs[v], (offset_x + (20 - nums_imgs[v].get_width()) / 2, height * 0.22)
        )


def draw_combo(screen):
    offset_x = screen.get_width() * 0.2
    _combo = str(combo) + "x"
    for v in reversed(_combo):
        gap = nums_imgs[v].get_width() - score_overlap
        offset_x -= gap
        screen.blit(
            nums_imgs[v], (offset_x + (gap - nums_imgs[v].get_width()) / 2, height * 0.8)
        )


def draw_scores(screen):
    img = utils.fit_image_to_screen(score_300_img, [height / 16] * 2)
    screen.blit(img, (width * 0.1, height * 0.32))
    offset_x = width * 0.2
    for v in str(results["300"]):
        offset_x += nums_imgs["0"].get_width() - score_overlap
        screen.blit(
            nums_imgs[v], (offset_x + (20 - nums_imgs[v].get_width()) / 2, height * 0.32 + (img.get_height() - nums_imgs[v].get_height()) / 2)
        )

    img = utils.fit_image_to_screen(score_100_img, [height / 16] * 2)
    screen.blit(img, (width * 0.1, height * 0.42))
    offset_x = width * 0.2
    for v in str(results["100"]):
        offset_x += nums_imgs["0"].get_width() - score_overlap
        screen.blit(
            nums_imgs[v], (offset_x + (20 - nums_imgs[v].get_width()) / 2, height * 0.42 + (img.get_height() - nums_imgs[v].get_height()) / 2)
        )

    img = utils.fit_image_to_screen(score_50_img, [height / 16] * 2)
    screen.blit(img, (width * 0.1, height * 0.52))
    offset_x = width * 0.2
    for v in str(results["50"]):
        offset_x += nums_imgs["0"].get_width() - score_overlap
        screen.blit(
            nums_imgs[v], (offset_x + (20 - nums_imgs[v].get_width()) / 2, height * 0.52 + (img.get_height() - nums_imgs[v].get_height()) / 2)
        )

    img = utils.fit_image_to_screen(miss_img, [height / 16] * 2)
    screen.blit(img, (width * 0.1, height * 0.62))
    offset_x = width * 0.2
    for v in str(results["0"]):
        offset_x += nums_imgs["0"].get_width() - score_overlap
        screen.blit(
            nums_imgs[v], (offset_x + (20 - nums_imgs[v].get_width()) / 2, height * 0.62 + (img.get_height() - nums_imgs[v].get_height()) / 2)
        )


def tick(dt, events):
    mgr_btns.update(events)
    update(events)

    draw(screen)
    mgr_btns.draw(screen, dt)


def draw_background(screen):
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))


def draw_title(screen):
    pg.draw.rect(screen, (0, 0, 0), (0, 0, width, h_title))

    screen.blit(ranking_title, (w_title, 0))

    screen.blit(btm_name, (0, 0))
    screen.blit(btm_author, (0, h_title * 0.3))
    screen.blit(btm_player, (0, h_title * 0.45))


def draw_ranking_panel(screen):
    screen.blit(ranking_panel, (0, h_panel))
    # TODO: draw score, results, combo and accuracy
