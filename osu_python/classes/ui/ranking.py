import pygame as pg
from osu_python.classes.ui import root
from osu_python.classes import Library, Config


def load_skin():
    global ButtonRetry, ButtonReplay, ButtonBack

    path = Config.base_path + "/skins/" + Config.cfg["skin"]

    ButtonRetry.im = pg.image.load(path + "/pause-retry.png")
    ButtonReplay.im = pg.image.load(path + "/pause-replay.png")
    ButtonBack.im = pg.image.load(path + "/menu-back.png")


class Button(root.UiElement):
    def __init__(self, height: int, width: int):
        super().__init__(True, True)

        self.width, self.height = width, height

        self.y_p = self.height / 10
        self.x_p = self.width / 17.5

        self.clicked = False
    
    def draw(self, screen: pg.Surface, dt: float):
        if self.hover:
            screen.blit(self.im.set_alpha(255), self.rect)
        else:
            screen.blit(self.im, self.rect)
    
    def click(self):
        self.clicked = True
    
    def is_colliding(self, coords: tuple):
        if self.rect.collidepoint(coords):
            return True


class ButtonRetry(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im = pg.transform.scale(
            ButtonRetry.im, (round(self.x_p * 2), round(self.y_p))
        ).convert_alpha()

        self.im.set_alpha(160)

        self.x, self.y = round(self.x_p * 14), round(self.y_p * 7)

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y


class ButtonReplay(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im = pg.transform.scale(
            ButtonReplay.im, (round(self.x_p * 2), round(self.y_p))
        ).convert_alpha()

        self.im.set_alpha(160)

        self.x, self.y = round(self.x_p * 14), round(self.y_p * 8.5)

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y


class ButtonBack(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        w_size = ButtonBack.im.get_height() / (height * (3 / 13)) * ButtonBack.im.get_width()

        self.im = pg.transform.scale(
            ButtonBack.im, (w_size, round(height * (3 / 13)))
        ).convert_alpha()

        self.im.set_alpha(160)

        self.x, self.y = 0, 0

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.bottom = 0, height
