import pygame as pg
from osu_python.classes import Library


class Startup:
    def __init__(self):
        self.state = 'library_update'
        self.font = pg.font.Font('./font/Aller_Lt.ttf', 20)
    
    def drawn_lib_update(self, screen: pg.Surface):
        img = self.font.render(
            'Updating library:\n{}/{}'.format(
                Library.update_progress, Library.update_total
            ), True, (255, 255, 255)
        )
        rect = img.get_rect()
        size = screen.get_size()

        screen.blit(img, (size[0] // 2, size[1] // 2))
        pg.draw.rect(
            screen, (255, 116, 159),
            (
                rect.x - 20, rect.y - 20,
                rect.w + 20, rect.h + 20
            ), width=5, border_radius=20
        )
    
    def draw(self, screen: pg.Surface):
        self.drawn_lib_update(screen)