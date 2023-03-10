import pygame as pg
import sys
from screeninfo import get_monitors
import logging
from datetime import datetime
import typing as t


TIME_GO_IN = 0


# Initializing display before loading game objects
for m in get_monitors():
    if m.is_primary:
        width, height = m.width, m.height
pg.display.init()
screen = pg.display.set_mode((width, height), flags=pg.FULLSCREEN | pg.DOUBLEBUF)


from osu_python import classes, scenes, map_loader


Config = classes.Config

# Settings up logger
formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(name)s]  %(message)s")
root = logging.getLogger()

if not root.handlers:
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

Lib = classes.Library

scene = None


def run_bm(path):
    change_scene(scenes.std, path, run_bm)


def change_scene(new_scene, *args):
    """Changes current scene"""
    global scene

    root.info("Switching scene {} to {}".format(scene, new_scene))

    map_loader.update()
    Lib.update()

    scene = new_scene
    scene.setup(height, width, screen, *args)

    root.info("Switched scenes.")


def focus_check():
    global focused
    _focus = pg.mouse.get_focused()
    if not focused and _focus:
        focused = True
        pg.mouse.set_visible(False)

    if focused and not _focus:
        focused = False
        pg.mouse.set_visible(True)


def update(events):
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


def draw(screen: pg.Surface, cursor):
    global focused, fps_clock, font
    cursor.draw(screen, pg.mouse.get_pos())

    fps = font.render(str(round(fps_clock.get_fps())), False, (255, 255, 255))
    screen_size = screen.get_size()
    screen.blit(fps, (screen_size[0] - 40, screen_size[1] - 20))

    pg.display.flip()


def run():
    global focused, fps_clock, screen, scene, width, height, font
    pg.init()

    fps = Config.cfg["fps"]
    fps_clock = pg.time.Clock()

    root.info("Running osu!python at {} fps".format(fps))

    focused = False

    pg.display.set_caption("osu!python")
    font = pg.font.SysFont(None, 28)

    change_scene(scenes.loading, lambda *args: change_scene(*args))

    cursor = classes.Cursor(1.5)

    dt = 1 / fps

    while True:
        focus_check()

        events = pg.event.get()

        # Updating scene
        scene.tick(dt, events)

        # Executing global updates
        update(events)
        draw(
            screen,
            cursor,
        )

        dt = fps_clock.tick(fps)


if __name__ == "__main__":
    run()
