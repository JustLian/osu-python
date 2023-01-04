import pygame as pg
import sys


def update(dt):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


def draw(screen: pg.Surface):
    screen.fill((255, 255, 255))

    pg.display.flip()


def run():
    pg.init()
    
    fps = 60.0
    fpsClock = pg.time.Clock()

    width, height = 1280, 720
    screen = pg.display.set_mode((width, height))

    dt = 1 / fps
    while True:
        update(dt)
        draw(screen)
        
        dt = fpsClock.tick(fps)


if __name__ == '__main__':
    run()