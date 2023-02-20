import pygame as pg
from osu_python.classes.ui import root
from osu_python.classes import Library, Config


def load_skin():
    global ButtonContinue, ButtonRetry, ButtonBack

    path = Config.base_path + "/skins/" + Config.cfg["skin"]

    ButtonContinue.im = pg.image.load(path + "/pause-continue.png")
    ButtonRetry.im = pg.image.load(path + "/pause-retry.png")
    ButtonBack.im = pg.image.load(path + "/pause-back.png")


class ButtonContinue(root.UiElement):
    im = None

    def __init__(self, height: int, width: int):
        super().init(True, True)

        self.width, self.height = width, height

        self.y_p = round(self.height / 10)
        self.x_p = round(self.width / 6)

        ButtonContinue.im = pg.transform.scale(
            ButtonContinue.im, (self.x_p * 2, self.y_p * 2)
        ).convert_alpha()

        self.x, self.y = self.x_p * 2, self.y
    
    def draw(self, screen: pg.Surface):
        screen.blit(ButtonContinue.im, (self.x, self.y))


class ButtonRetry(root.UiElement):
    im = None

    def __init__(self, height: int, width: int):
        super().init(True, True)

        self.width, self.height = width, height

        self.y_p = round(self.height / 10)
        self.x_p = round(self.width / 6)

        ButtonRetry.im = pg.transform.scale(
            ButtonRetry.im, (self.x_p * 2, self.y_p * 2)
        ).convert_alpha()

        self.x, self.y = self.x_p * 2, self.y
    
    def draw(self, screen: pg.Surface):
        screen.blit(ButtonRetry.im, (self.x, self.y))


class ButtonBack(root.UiElement):
    im = None

    def __init__(self, height: int, width: int):
        super().init(True, True)

        self.width, self.height = width, height

        self.y_p = round(self.height / 10)
        self.x_p = round(self.width / 6)

        ButtonBack.im = pg.transform.scale(
            ButtonBack.im, (self.x_p * 2, self.y_p * 2)
        ).convert_alpha()

        self.x, self.y = self.x_p * 2, self.y
    
    def draw(self, screen: pg.Surface):
        screen.blit(ButtonBack.im, (self.x, self.y))
