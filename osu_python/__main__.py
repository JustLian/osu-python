import pygame as pg
import sys
from screeninfo import get_monitors
import logging
from datetime import datetime
import typing as t


# Initializing display before loading game objects
for m in get_monitors():
    if m.is_primary:
        width, height = m.width, m.height
pg.display.init()
screen = pg.display.set_mode((width, height), flags=pg.FULLSCREEN | pg.DOUBLEBUF)


from osu_python import classes, utils, map_loader


Config = classes.Config

# Settings up logger
formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(name)s]  %(message)s")
root = logging.getLogger()

log_path = "{}/logs/{}.log".format(
    Config.base_path, datetime.now().strftime("%Y-%m-%d %H.%M.%S")
)
open(log_path, "w").close()
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
root.addHandler(file_handler)

terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(formatter)
root.addHandler(terminal_handler)

root.setLevel(logging.DEBUG)

# Data from osu-map parser goes here
all_objects = []

Lib = classes.Library
Lib.update()


def miss_callback():
    ui.hit(0)


def click(mouse_pos: t.Tuple[int, int]):
    active_object = None
    for obj in all_objects:
        if current_time < obj.appear_time:
            break

        elif current_time > obj.endtime:
            continue

        elif obj.appear_time < current_time and obj.score == None:
            if active_object == None:
                active_object = obj

            mouse_pos = pg.mouse.get_pos()
            if obj.rect.collidepoint(mouse_pos) and isinstance(
                obj, classes.game_object.Circle
            ):
                obj_pos = obj.rect
                obj_center = (
                    obj_pos[0] + obj_pos[2] / 2,
                    obj_pos[1] + obj_pos[3] / 2,
                )
                if (
                    (mouse_pos[0] - obj_center[0]) ** 2
                    + (mouse_pos[1] - obj_center[1]) ** 2
                ) ** 0.5 <= (obj_pos[2] / 2) * 0.757:
                    if obj == active_object:
                        score = obj.hit(current_time)
                        if score:
                            ui.hit(score)
                    else:
                        obj.count_vibr = 20
                    break


def focus_check():
    global focused
    _focus = pg.mouse.get_focused()
    if not focused and _focus:
        focused = True
        pg.mouse.set_visible(False)

    if focused and not _focus:
        focused = False
        pg.mouse.set_visible(True)


def update():
    global c, ui
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN or (
            event.type == pg.KEYDOWN
            and int(event.key)
            in [Config.cfg["keys"]["key1"], Config.cfg["keys"]["key2"]]
        ):
            click(pg.mouse.get_pos())
            # for obj in all_objects:
            #     if current_time < obj.appear_time:
            #         break

            #     elif obj.appear_time < current_time:
            #         mouse_pos = pg.mouse.get_pos()
            #         if obj.rect.collidepoint(mouse_pos) and isinstance(
            #             obj, classes.game_object.Circle
            #         ):
            #             obj_pos = obj.rect
            #             obj_center = (
            #                 obj_pos[0] + obj_pos[2] / 2,
            #                 obj_pos[1] + obj_pos[3] / 2,
            #             )
            #             if (
            #                 (mouse_pos[0] - obj_center[0]) ** 2
            #                 + (mouse_pos[1] - obj_center[1]) ** 2
            #             ) ** 0.5 <= (obj_pos[2] / 2) * 0.757:
            #                 score = obj.hit(current_time)
            #                 if score:
            #                     ui.hit(score)
            #                 break

        if event.type == pg.MOUSEBUTTONUP or (
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
                        ) ** 0.5 <= (obj_pos[2] / 2) * 0.757:
                            obj.touching = False
                            break


def draw(screen: pg.Surface, cursor):
    global focused, ui, fps_clock, font
    screen.fill((0, 0, 0))

    ui.draw_background(screen)
    pg.draw.rect(screen, "red", ((add_x, add_y), (m, n)), width=2)

    tmp = []
    for obj in reversed(all_objects):
        if current_time < obj.appear_time:
            continue

        elif current_time > obj.endtime:
            tmp.append(obj)
            break

        elif obj.appear_time < current_time:
            obj.draw(screen, current_time)

    # removing objects
    [all_objects.remove(obj) for obj in tmp]

    ui.draw_score(screen)
    cursor.draw(screen, pg.mouse.get_pos())

    fps = font.render(str(round(fps_clock.get_fps())), False, (255, 255, 255))
    screen_size = screen.get_size()
    screen.blit(fps, (screen_size[0] - 40, screen_size[1] - 20))

    pg.display.flip()


def run():
    global current_time, circle, scores, add_x, add_y, m, n, focused, ui, fps_clock, font, screen
    pg.init()
    pg.mixer.init()

    music_offset = 0
    current_time = 0
    fps = 60.0
    fps_clock = pg.time.Clock()
    focused = False

    pg.display.set_caption("osu!python")
    font = pg.font.SysFont(None, 28)

    m, n = utils.playfield_size(height)
    add_x = (width - m) / 2
    add_y = height * 0.02

    scale = utils.osu_scale(n)

    diff_path = "./osu_python/map.osu"
    queue, audio, bg, map = map_loader.load_map(
        diff_path, scale, add_x, add_y, miss_callback
    )
    all_objects.extend(queue)

    cursor = classes.Cursor()
    drain_time = (all_objects[-1].appear_time - all_objects[0].appear_time) / 1000
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
    ui = classes.InGameUI(diff_multiplier, 1, bg, 0.8, (width, height))

    music = pg.mixer.music
    music.load(audio)
    music.play()

    dt = 1 / fps
    while True:
        current_time += dt
        if abs(music.get_pos() - current_time - music_offset) > 500:
            music.rewind()
            music.set_pos(current_time / 1000)
            music_offset = music.get_pos() - current_time
        focus_check()
        update()
        draw(
            screen,
            cursor,
        )

        dt = fps_clock.tick(fps)


if __name__ == "__main__":
    run()
