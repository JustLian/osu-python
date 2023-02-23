import pygame as pg
from osu_python.classes.ui import root
from osu_python.classes import Library, Config


def load_skin():
    global ButtonContinue, ButtonRetry, ButtonBack

    path = Config.base_path + "/skins/" + Config.cfg["skin"]

    ButtonContinue.im = pg.image.load(path + "/pause-continue.png")
    ButtonRetry.im = pg.image.load(path + "/pause-retry.png")
    ButtonBack.im = pg.image.load(path + "/pause-back.png")


class Button(root.UiElement):
    def __init__(self, height: int, width: int):
        super().__init__(True, True)

        self.width, self.height = width, height

        self.y_p = round(self.height / 10)
        self.x_p = round(self.width / 6)

        self.clicked = False
    
    def draw(self, screen: pg.Surface, dt: float):
        screen.blit(self.im, self.rect)
    
    def click(self):
        self.clicked = True
    
    def is_colliding(self, coords: tuple):
        if self.rect.collidepoint(coords):
            return True


class ButtonContinue(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im = pg.transform.scale(
            ButtonContinue.im, (self.x_p * 2, self.y_p * 2)
        ).convert_alpha()

        self.x, self.y = self.x_p * 2, self.y_p

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y


class ButtonRetry(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im = pg.transform.scale(
            ButtonRetry.im, (self.x_p * 2, self.y_p * 2)
        ).convert_alpha()

        self.x, self.y = self.x_p * 2, self.y_p * 4

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y


class ButtonBack(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im = pg.transform.scale(
            ButtonBack.im, (self.x_p * 2, self.y_p * 2)
        ).convert_alpha()

        self.x, self.y = self.x_p * 2, self.y_p * 7

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y
