import pygame as pg
import sys
from osu_python import classes, utils, map_loader
from screeninfo import get_monitors
from multiprocessing import Process

# Data from osu-map parser goes here
all_objects = []


Config = classes.Config
Lib = classes.Library
proc = Process(target=Lib.update)
proc.start()


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
            print(Lib.update_progress, '/', Lib.update_total)
            for obj in all_objects:
                if current_time < obj.appear_time:
                    break

                elif obj.appear_time < current_time:
                    if obj.rect.collidepoint(pg.mouse.get_pos()) and isinstance(
                        obj, classes.game_object.Circle
                    ):
                        obj.hit(current_time)
                        break


def draw(screen: pg.Surface):
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

    # removing objects
    [all_objects.remove(obj) for obj in tmp]

    pg.display.flip()


def run():
    global current_time, circle, scores, add_x, add_y, m, n
    pg.init()

    current_time = 0
    fps = 60.0
    fps_clock = pg.time.Clock()

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
    # from pprint import pprint
    # from time import time
    # s = time()
    # pprint(Lib.search('clover'))
    # print(time() - s)

    dt = 1 / fps
    while True:
        current_time += dt
        update()
        draw(screen)

        dt = fps_clock.tick(fps)


if __name__ == "__main__":
    run()
