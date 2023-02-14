import pygame as pg
from osu_python.classes.ui import root
from osu_python import utils


class OsuLogo(root.UiElement):
    logo = pg.image.load('./ui/menu/logo.png').convert_alpha()

    def __init__(self, width: int, height: int):
        self.original_size = height * .8
        self.current_size = height * .8
        self.img = pg.transform.scale(
            OsuLogo.logo,
            (height * .8, height * .8)
        )

        self.rect = self.img.get_rect()
        self.rect.x = width // 2
        self.rect.y = height // 2

        self.goal_size = self.rect.height
        self.step = 0

        super().__init__(True, True)
    
    def toggle_hover(self):
        if not self.hover:
            self.goal_size = round(self.original_size * 1.05)
        else:
            self.goal_size = self.original_size
        
        self.step = (self.goal_size - self.current_size) / 5

        super().toggle_hover()


    def draw(self, screen: pg.Surface):
        if self.goal_size != self.current_size:
            self.current_size += self.step
            if (self.step > 0 and self.current_size > self.goal_size) or (self.step < 0 and self.current_size < self.goal_size):
                self.current_size = self.goal_size

        x = self.rect.x - self.current_size // 2
        y = self.rect.y - self.current_size // 2
        pg.draw.circle(
            screen, (255, 125, 183),
            (self.rect.x, self.rect.y), self.current_size * .45
        )
        screen.blit(pg.transform.scale(self.img, (self.current_size, self.current_size)), (x, y))
    
    def is_colliding(self, pos) -> bool:
        return utils.inside_a_circle(
            *pos, self.rect.x, self.rect.y, self.current_size / 2
        )
    
    def click(self):
        ...