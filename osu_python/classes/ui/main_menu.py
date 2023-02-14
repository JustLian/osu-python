import pygame as pg
from osu_python.classes.ui import root
from osu_python import utils


class OsuLogo(root.UiElement):
    logo = pg.image.load('./ui/menu/logo.png').convert_alpha()

    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.stage1_size = (height * .6, height * .6)
        self.stage2_size = (height * .3, height * .3)

        self.stage = 1

        self.original_size = self.stage1_size
        self.current_size = self.original_size
        self.img = pg.transform.scale(
            OsuLogo.logo,
            self.original_size
        )

        self.rect = self.img.get_rect()
        self.rect.x = width // 2
        self.rect.y = height // 2

        self.goal_size = self.rect.height
        self.step = 0

        # logo animations
        self.size = root.Animation(
            1, self.original_size, self.original_size, 'LinearInOut'
        )
        self.offset = root.Animation(
            1, [0, 0], [0, 0], 'LinearInOut'
        )

        # gray line animations
        self.line = root.Animation(
            1, (0, 0, 0), (0, 0, 0), 'LinearInOut'
        )

        super().__init__(True, True)
    
    def toggle_hover(self):
        if not self.hover:
            self.size = root.Animation(
                250, self.original_size,
                (self.original_size[0] * 1.05, self.original_size[0] * 1.05),
                'ElasticEaseOut'
            )
        else:
            self.size = root.Animation(
                250, (self.original_size[0] * 1.05, self.original_size[0] * 1.05),
                self.original_size, 'ElasticEaseOut'
            )

        super().toggle_hover()


    def draw(self, screen: pg.Surface, dt):
        line = self.line(dt)
        if self.stage == 1:
            line[2] = 255 - line[2]
        pg.draw.rect(
            screen, (50, 50, 50, line[2]),
            (0, (self.height - line[1]) // 2, line[0], line[1])
        )

        self.current_size = self.size(dt)
        self.c_offset = self.offset(dt)

        pg.draw.circle(
            screen, (248, 119, 176),
            (self.width // 2 + self.c_offset[0], self.height // 2 + self.c_offset[1]), self.current_size[0] * .465
        )
        screen.blit(pg.transform.scale(self.img, self.current_size), (
            (self.width - self.current_size[0]) // 2 + self.c_offset[0],
            (self.height - self.current_size[1]) // 2 + self.c_offset[1]
        ))
    
    def is_colliding(self, pos) -> bool:
        return utils.inside_a_circle(
            *pos, self.rect.x + self.c_offset[0], self.rect.y + self.c_offset[1], self.current_size[0] / 2
        )
    
    def click(self):
        if self.stage == 1:
            self.stage = 2
            self.original_size = self.stage2_size
            self.size = root.Animation(
                400, self.current_size, self.original_size,
                'QuinticEaseInOut'
            )
            self.offset = root.Animation(
                300, (0, 0), (
                    -self.width * .2, 0
                ), 'QuinticEaseInOut'
            )
            self.line = root.Animation(
                500, (self.width, self.stage2_size[0] * .25, 0), (
                    self.width, self.stage2_size[0] * .5, 255
                ), 'QuinticEaseOut'
            )
        else:
            self.stage = 1
            self.original_size = self.stage1_size
            self.size = root.Animation(
                400, self.current_size, self.original_size,
                'QuinticEaseInOut'
            )
            self.offset = root.Animation(
                300, (-self.width * .2, 0), (
                    0, 0
                ), 'QuinticEaseInOut'
            )
            self.line = root.Animation(
                500, (self.width, self.stage2_size[0] * .5, 0), (
                    self.width, self.stage2_size[0] * .25, 255
                ), 'QuinticEaseOut'
            )