import pygame as pg
from osu_python.classes.ui import root
from osu_python import utils


class OsuLogo(root.UiElement):
    logo = pg.image.load('./ui/menu/logo.png').convert_alpha()

    def __init__(self, width: int, height: int):
        self.original_size = (height * .8, height * .8)
        self.current_size = (height * .8, height * .8)
        self.img = pg.transform.scale(
            OsuLogo.logo,
            self.original_size
        )

        self.rect = self.img.get_rect()
        self.rect.x = width // 2
        self.rect.y = height // 2

        self.goal_size = self.rect.height
        self.step = 0

        self.size = root.Animation(
            1, self.original_size, self.original_size, 'LinearInOut'
        )

        super().__init__(True, True)
    
    def toggle_hover(self):
        if not self.hover:
            self.size = root.Animation(
                300, self.original_size,
                (self.original_size[0] * 1.05, self.original_size[0] * 1.05),
                'ElasticEaseOut'
            )
        else:
            self.size = root.Animation(
                300, (self.original_size[0] * 1.05, self.original_size[0] * 1.05),
                self.original_size, 'ElasticEaseOut'
            )

        super().toggle_hover()


    def draw(self, screen: pg.Surface, dt):
        self.current_size = self.size(dt)
        screen.blit(pg.transform.scale(self.img, self.current_size), (
            (screen.get_width() - self.current_size[0]) // 2,
            (screen.get_height() - self.current_size[1]) // 2
        ))
    
    def is_colliding(self, pos) -> bool:
        return utils.inside_a_circle(
            *pos, self.rect.x, self.rect.y, self.current_size[0] / 2
        )
    
    def click(self):
        ...