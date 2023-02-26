from time import sleep
import pygame as pg
import typing as t
import os
from osu_python import classes, utils, map_loader
from osu_python.classes import Config, game_object
from osu_python.classes import ui as cui
from osu_python import utils


def click(mouse_pos: t.Tuple[int, int]):
    for index, obj in enumerate(all_objects):
        if current_time < obj.appear_time:
            break

        elif current_time > obj.endtime:
            continue

        elif obj.appear_time < current_time and obj.score == None:
            mouse_pos = pg.mouse.get_pos()
            if obj.rect.collidepoint(mouse_pos) and isinstance(
                obj, classes.game_object.Spinner
            ):
                obj.hit(current_time)
                break
            obj_pos = obj.rect
            obj_center = (
                obj_pos[0] + obj_pos[2] / 2,
                obj_pos[1] + obj_pos[3] / 2,
            )
            if (
                (mouse_pos[0] - obj_center[0]) ** 2
                + (mouse_pos[1] - obj_center[1]) ** 2
            ) ** 0.5 <= (obj_pos[2] / 2):
                if index != 0:
                    prev = all_objects[index - 1]
                    if isinstance(prev, classes.game_object.Circle):
                        if (
                            prev.score == None
                            and abs(prev.hit_time - obj.hit_time) < 100
                        ):
                            obj.count_vibr = 20
                            break
                score = obj.hit(current_time)
                if score:
                    ui.hit(score)
                break


def update(events):
    global c, ui, PAUSED, FAILED
    ui.drain_hp(current_time)
    if ui.hp <= 0:
        PAUSED = True
        FAILED = True
        btn_play.toggle_show()
    for event in events:
        if (
            (not PAUSED or FAILED)
            and event.type == pg.KEYDOWN
            and event.key == pg.K_ESCAPE
        ):
            PAUSED = True

        if (
            Config.cfg["mouse_buttons"]
            and event.type == pg.MOUSEBUTTONDOWN
            and event.button in [1, 3]
        ) or (
            event.type == pg.KEYDOWN
            and int(event.key)
            in [Config.cfg["keys"]["key1"], Config.cfg["keys"]["key2"]]
        ):
            click(pg.mouse.get_pos())

        if (Config.cfg["mouse_buttons"] and event.type == pg.MOUSEBUTTONUP) or (
            event.type == pg.KEYUP
            and int(event.key)
            in [Config.cfg["keys"]["key1"], Config.cfg["keys"]["key2"]]
        ):
            for obj in all_objects:
                if current_time < obj.appear_time:
                    break

                elif obj.appear_time < current_time:
                    mouse_pos = pg.mouse.get_pos()
                    if obj.rect.collidepoint(mouse_pos) and isinstance(
                        obj, classes.game_object.Slider
                    ):
                        obj_pos = obj.rect
                        obj_center = (
                            obj_pos[0] + obj_pos[2] / 2,
                            obj_pos[1] + obj_pos[3] / 2,
                        )
                        if (
                            (mouse_pos[0] - obj_center[0]) ** 2
                            + (mouse_pos[1] - obj_center[1]) ** 2
                        ) ** 0.5 <= (obj_pos[2] / 2):
                            obj.touching = False
                            break
                    if obj.rect.collidepoint(mouse_pos) and isinstance(
                        obj, classes.game_object.Spinner
                    ):
                        obj.touching = False


def draw(screen: pg.Surface):
    global ui
    screen.fill((0, 0, 0))

    ui.draw_background(screen)

    tmp = []
    dac = []

    for obj in reversed(all_objects):
        if type(obj) == game_object.Slider:
            if current_time > obj.endtime and not obj.drawing_score:
                obj.get_score()
                obj.drawing_score = True
                obj.endtime += 400

        if current_time < obj.appear_time:
            continue

        elif current_time > obj.endtime:
            tmp.append(obj)
            break

        elif obj.appear_time < current_time:
            if obj.draw(screen, current_time):
                dac.append(obj)

    for obj in dac:
        obj.draw_appr_circle(screen, current_time)

    # removing objects
    [all_objects.remove(obj) for obj in tmp]

    ui.draw(screen)
    if len(all_objects) == 0:
        music.stop()
        ranking(
            bm_name,
            author,
            retry_func,
            back_to_menu,
            utils.calculate_rank(ui.accuracy),
            bg,
            ui.score,
            ui.scores,
            ui.max_combo,
            ui.accuracy,
        )


def setup(_height, _width, _screen, _diff_path, _switch, _back_to_menu, _ranking):
    global current_time, circle, scores, add_x, add_y, m, n, focused, ui, fps_clock, screen, height, width, music, screen, music_offset, btn_play, btn_retry, btn_back, mgr, diff_path, PAUSED, FAILED, IS_FALL, retry_func, all_objects, pause_overlay, fail_overlay, DRAW_PO, back_to_menu, ranking, author, bm_name, bg, STARTED, wait_time

    all_objects = []

    height = _height
    width = _width
    screen = _screen

    back_to_menu = _back_to_menu
    ranking = _ranking

    diff_path = _diff_path

    pg.mixer.init()

    music_offset = 0
    current_time = 0

    m, n = utils.playfield_size(height)
    add_x = (width - m) / 2
    add_y = height * 0.02

    scale = utils.osu_scale(n)

    def hit_callback(score: int):
        ui.hit(score)

    queue, audio, bg, map = map_loader.load_map(
        diff_path, scale, add_x, add_y, hit_callback
    )
    all_objects.extend(queue)
    author = map.artist
    bm_name = map.display_name

    drain_time = (all_objects[-1].endtime - all_objects[0].appear_time) / 1000
    # TODO: break time should not be in drain_time
    diff_multiplier = round(
        (
            map.hp()
            + map.cs()
            + map.od()
            + min(max(len(all_objects) / drain_time * 8, 0), 16)
        )
        / 38
        * 5
    )
    ui = classes.InGameUI(
        diff_multiplier,
        1,
        bg,
        Config.cfg["bg_dim"],
        (width, height),
        map.hp(),
        current_time,
    )

    music = pg.mixer.music
    music.load(audio)

    cui.pause.load_skin()
    btn_play = cui.pause.ButtonContinue(height, width)
    btn_retry = cui.pause.ButtonRetry(height, width)
    btn_back = cui.pause.ButtonBack(height, width)
    mgr = cui.root.UiManager([btn_play, btn_retry, btn_back])

    PAUSED = False
    FAILED = False
    IS_FALL = False
    STARTED = False
    wait_time = 0

    try:
        fail_overlay = utils.fit_image_to_screen(
            pg.image.load(
                Config.base_path
                + "/skins/"
                + Config.cfg["skin"]
                + "/fail-background.png"
            ).convert_alpha(),
            screen.get_size(),
        )
    except FileNotFoundError:
        fail_overlay = None

    try:
        pause_overlay = utils.fit_image_to_screen(
            pg.image.load(
                Config.base_path + "/skins/" + Config.cfg["skin"] + "/pause-overlay.png"
            ).convert_alpha(),
            screen.get_size(),
        )
    except FileNotFoundError:
        pause_overlay = None

    def retry_func() -> None:
        _switch(_diff_path, _switch, _back_to_menu, _ranking)

    return tick


def tick(dt, events):
    global PAUSED, FAILED, STARTED, pause_overlay, fail_overlay, wait_time

    if not STARTED and wait_time < 3000:
        wait_time += dt
        screen.fill((0, 0, 0))
        ui.draw_background(screen)
        return
    elif not STARTED:
        STARTED = True
        music.play()

    if PAUSED or FAILED:
        music.pause()

        if IS_FALL:
            btn_play.toggle_click()
            btn_play.toggle_hover()

        mgr.update(events)

        if btn_play.clicked:
            PAUSED = False
            btn_play.clicked = False

            music.unpause()

        elif btn_retry.clicked:
            retry_func()

        elif btn_back.clicked:
            back_to_menu()

        else:
            if FAILED:
                screen.blit(fail_overlay, (0, 0))
            else:
                screen.blit(pause_overlay, (0, 0))
            mgr.draw(screen, dt)

    else:
        global music_offset, current_time

        current_time += dt
        if abs(music.get_pos() - current_time - music_offset) > 500:
            music.rewind()
            music.set_pos(current_time / 1000)
            music_offset = music.get_pos() - current_time
        update(events)
        draw(screen)

        if PAUSED and not pause_overlay:
            screen.set_alpha(75)
            pause_overlay = pg.Surface(screen.get_size())
            pause_overlay.blit(screen, (0, 0))
            screen.set_alpha(255)

        if FAILED and not fail_overlay:
            screen.set_alpha(75)
            fail_overlay = pg.Surface(screen.get_size())
            fail_overlay.blit(screen, (0, 0))
            screen.set_alpha(255)
