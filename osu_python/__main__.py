import pygame as pg
import sys
from osu_python import classes, utils, map_loader
from screeninfo import get_monitors
import logging
from datetime import datetime


Config = classes.Config

# Settings up logger
formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(name)s]  %(message)s")
root = logging.getLogger()

log_path = '{}/logs/{}.log'.format(
    Config.base_path,
    datetime.now().strftime('%Y-%m-%d %H.%M.%S')
)
open(log_path, 'w').close()
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
    global c
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN or (
            event.type == pg.KEYDOWN
            and int(event.key)
            in [Config.cfg["keys"]["key1"], Config.cfg["keys"]["key2"]]
        ):
            for obj in all_objects:
                if current_time < obj.appear_time:
                    break

                elif obj.appear_time < current_time:
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
                            obj.hit(current_time)
                            break


def draw(screen: pg.Surface, cursor):
    global focused
    screen.fill((0, 0, 0))

    pg.draw.rect(screen, "red", ((add_x, add_y), (m, n)), width=2)

    tmp = []
    for obj in all_objects:
        if current_time < obj.appear_time:
            break

        elif current_time > obj.endtime:
            tmp.append(obj)

        elif obj.appear_time < current_time:
            obj.draw(screen, current_time)

    cursor.draw(screen, pg.mouse.get_pos())

    # removing objects
    [all_objects.remove(obj) for obj in tmp]

    pg.display.flip()


def run():
    global current_time, circle, scores, add_x, add_y, m, n, focused
    pg.init()
    pg.mixer.init()

    music_offset = 0
    current_time = 0
    fps = 60.0
    fps_clock = pg.time.Clock()
    focused = False

    for m in get_monitors():
        if m.is_primary:
            width, height = m.width, m.height

    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("osu!python")

    m, n = utils.playfield_size(height)
    add_x = (width - m) / 2
    add_y = height * 0.02

    scale = utils.osu_scale(n)

    queue, audio, bg = map_loader.load_map("./osu_python/map.osu", scale, add_x, add_y)
    all_objects.extend(queue)

    music = pg.mixer.music
    music.load(audio)
    music.play()

    cursor = classes.Cursor()

    dt = 1 / fps
    while True:
        current_time += dt
        if abs(music.get_pos() - current_time - music_offset) > 500:
            music.rewind()
            music.set_pos(current_time / 1000)
            music_offset = music.get_pos() - current_time
        focus_check()
        update()
        draw(screen, cursor)

        dt = fps_clock.tick(fps)


if __name__ == "__main__":
    run()
