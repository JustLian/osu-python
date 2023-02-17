import pygame as pg
from osu_python.classes.ui import root
from osu_python import utils


class OsuLogo(root.UiElement):
    logo = pg.image.load('./ui/menu/logo.png').convert_alpha()

    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.stage1_size = (height * .6, height * .6)
        self.stage2_size = (height * .3, height * .3)
        self.right_border = 0
        self.line_height = 0

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
            1, (0, 0, 0, 0), (0, 0, 0, 0), 'LinearInOut'
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
        self.line_height = line[1]

        dim = pg.Surface((self.width, self.height))
        dim.fill((0, 0, 0))
        dim.set_alpha(line[3])
        screen.blit(dim, (0, 0))

        line_s = pg.Surface((line[0], line[1]))
        line_s.set_alpha(line[2])
        line_s.fill((50, 50, 50))
        screen.blit(line_s, (0, (self.height - line[1]) // 2))

        self.current_size = self.size(dt)
        self.c_offset = self.offset(dt)

        
        x_pos = (self.width - self.current_size[0]) // 2 + self.c_offset[0]
        draw_logo = (lambda:
            pg.draw.circle(
                screen, (248, 119, 176),
                (self.width // 2 + self.c_offset[0], self.height // 2 + self.c_offset[1]), self.current_size[0] * .465
            )
            and
            screen.blit(pg.transform.scale(self.img, self.current_size), (
                x_pos,
                (self.height - self.current_size[1]) // 2 + self.c_offset[1]
            ))
        )

        self.right_border = x_pos + self.current_size[0]
        return draw_logo
    
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
                500, (self.width, self.stage2_size[0] * .25, 0, 0), (
                    self.width, self.stage2_size[0] * .5, 255, 50
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
                500, (self.width, self.stage2_size[0] * .5, 255, 50), (
                    self.width, self.stage2_size[0] * .25, 0, 0
                ), 'QuinticEaseOut'
            )


class Button(root.UiElement):
    def __init__(
        self,
        first_button: bool,
        left_obj: root.UiElement,
        osu_logo: OsuLogo,
        icon: pg.Surface,
        text: str, color: tuple,
        width: int, height: int,
        font: pg.font.Font
    ):
        self.width, self.height = width, height
        self.left_obj = left_obj
        self.color = color
        self.logo = osu_logo
        self.img = icon
        self.right_border = 0
        self.text = font.render(
            text, True, (255, 255, 255)
        )
        self.fb = first_button

        if self.fb:
            self.left_offset = -width * .028
            self.size = root.Animation(
                1, (width * .1,), (width * .1,), 'LinearInOut'
            )
        else:
            self.left_offset = 0
            self.size = root.Animation(
                1, (width * .128,), (width * .128,), 'LinearInOut'
            )

        self.offset = width * .015

        super().__init__()
    
    def draw(self, screen: pg.Surface, dt) -> None:
        if self.logo.stage != 2:
            return
        
        w = self.size(dt)[0]
        h = self.logo.line_height
        top = (self.height - h) // 2
        bottom = (self.height + h) // 2

        self.right_border = self.left_obj.right_border + w

        pg.draw.polygon(
            screen, self.color,
            (
                (self.left_obj.right_border + self.left_offset, bottom),
                (self.left_obj.right_border + self.offset + self.left_offset, top),
                (self.left_obj.right_border + w + self.offset, top),
                (self.left_obj.right_border + w, bottom)
            )
        )

        middle = (
            self.left_obj.right_border + (w + self.offset + self.left_offset) // 2,
            self.height // 2
        )

        img = pg.transform.scale(
            self.img, (self.logo.line_height * .3, self.logo.line_height * .3)
        )
        img_height = img.get_height()
        screen.blit(
            img, (
                middle[0] - img.get_width() // 2,
                middle[1] - img_height // 2
            )
        )
        screen.blit(
            self.text, (
                middle[0] - self.text.get_height(),
                self.height // 2 + h * .3
            )
        )
    
    def click(self):
        ...