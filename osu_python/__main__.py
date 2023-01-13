import pygame as pg
import sys
from osu_python import classes, utils, map_loader


# Data from osu-map parser goes here
all_objects = []

OD = 8
CS = 1
AR = 8.5
scores = utils.calculate_hit_windows(OD)


def update(dt):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if all_objects[0].rect.collidepoint(pg.mouse.get_pos()):
                all_objects[0].is_hit = True


def draw(screen: pg.Surface):
    screen.fill((0, 0, 0))

    pg.draw.rect(
        screen, 'red', (
            (add_x, 0),
            (m, n)
        ), width=2
    )

    for obj in all_objects:
        if current_time < obj.appear_time:
            break
        
        elif current_time > obj.hit_time:
            all_objects.remove(obj)

        elif obj.appear_time < current_time:
            obj.draw(screen, current_time)

    pg.display.flip()


def run():
    global current_time, circle, scores, add_x, m, n
    pg.init()

    current_time = 0
    fps = 60.0
    fps_clock = pg.time.Clock()

    width, height = 1280, 720
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("osu!python")

    m, n = utils.playfield_size(height)
    h_scale = utils.pixel_horizontal_scaling(m)
    v_scale = utils.pixel_vertical_scaling(n)
    add_x = (width - m) / 2
    
    all_objects.extend(map_loader.load_map('./osu_python/map.osu', v_scale, h_scale, add_x))

    dt = 1 / fps
    while True:
        current_time += dt
        update(dt)
        draw(screen)

        dt = fps_clock.tick(fps)


if __name__ == "__main__":
    run()
