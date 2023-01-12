import pygame as pg
import sys
from osu_python import classes, utils


def update(dt):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if circle.rect.collidepoint(pg.mouse.get_pos()):
                circle.is_hit = True


def draw(screen: pg.Surface):
    screen.fill((0, 0, 0))

    if 2800 <= current_time <= 4000:
        circle.draw(screen, current_time)

    pg.display.flip()


def run():
    global current_time, circle
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
    
    cs = 0
    hit_r = utils.calculate_hit_r(cs)
    appr_r = utils.calculate_appr_r(cs)

    circle = classes.game_object.Circle(
        3000, 1800, 2600, (500, 500), False, (), hit_r, appr_r
    )

    dt = 1 / fps
    while True:
        current_time += dt
        update(dt)
        draw(screen)

        dt = fps_clock.tick(fps)


if __name__ == "__main__":
    run()
