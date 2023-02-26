import pygame as pg
from osu_python.classes.ui import root
from osu_python.classes import Library, Config


COEFF = 1.1


def load_skin():
    global ButtonContinue, ButtonRetry, ButtonBack

    path = Config.base_path + "/skins/" + Config.cfg["skin"]

    ButtonContinue.im = pg.image.load(path + "/pause-continue.png").convert_alpha()
    ButtonRetry.im = pg.image.load(path + "/pause-retry.png").convert_alpha()
    ButtonBack.im = pg.image.load(path + "/pause-back.png").convert_alpha()


class Button(root.UiElement):
    def __init__(self, height: int, width: int):
        super().__init__(True, True)

        self.width, self.height = width, height

        self.y_p = self.height / 19.5
        self.x_p = self.width / 17

        self.clicked = False

    def draw(self, screen: pg.Surface, dt: float):
        if self.hover:
            screen.blit(
                self.im2,
                (
                    self.x - round((COEFF - 1) * self.x_p * 5 / 2),
                    self.y - round((COEFF - 1) * self.y_p * 5 / 2),
                ),
            )
        else:
            screen.blit(self.im1, self.rect)

    def click(self):
        self.clicked = True

    def is_colliding(self, coords: tuple):
        if self.hover:
            x = self.x - round((COEFF - 1) * self.x_p * 5 / 2)
            y = self.y - round((COEFF - 1) * self.y_p * 5 / 2)
            w, h = self.im2.get_size()
        else:
            x, y = self.x, self.y
            w, h = self.im1.get_size()

        return x <= coords[0] <= x + w and y <= coords[1] <= y + h


class ButtonContinue(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im1 = pg.transform.scale(
            ButtonContinue.im, (round(self.x_p * 5), round(self.y_p * 3))
        ).convert_alpha()

        self.im2 = pg.transform.scale(
            ButtonContinue.im,
            (round(self.x_p * 5 * COEFF), round(self.y_p * 3 * COEFF)),
        ).convert_alpha()

        self.x, self.y = round(self.x_p * 6), round(self.y_p * 3.5)

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y


class ButtonRetry(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im1 = pg.transform.scale(
            ButtonRetry.im, (round(self.x_p * 5), round(self.y_p * 3))
        ).convert_alpha()

        self.im2 = pg.transform.scale(
            ButtonRetry.im, (round(self.x_p * 5 * COEFF), round(self.y_p * 3 * COEFF))
        ).convert_alpha()

        self.x, self.y = round(self.x_p * 6), round(self.y_p * 8.5)

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y


class ButtonBack(Button):
    im = None

    def __init__(self, height: int, width: int):
        super().__init__(height, width)

        self.im1 = pg.transform.scale(
            ButtonBack.im, (round(self.x_p * 5), round(self.y_p * 3))
        ).convert_alpha()

        self.im2 = pg.transform.scale(
            ButtonBack.im, (round(self.x_p * 5 * COEFF), round(self.y_p * 3 * COEFF))
        ).convert_alpha()

        self.x, self.y = round(self.x_p * 6), round(self.y_p * 13.5)

        self.rect = self.im.get_rect()
        self.rect.left, self.rect.top = self.x, self.y
