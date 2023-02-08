import pygame as pg
from osu_python import utils
import typing as t

score_imgs = {
    "0": pg.image.load("./skin/score-0.png").convert_alpha(),
    "1": pg.image.load("./skin/score-1.png").convert_alpha(),
    "2": pg.image.load("./skin/score-2.png").convert_alpha(),
    "3": pg.image.load("./skin/score-3.png").convert_alpha(),
    "4": pg.image.load("./skin/score-4.png").convert_alpha(),
    "5": pg.image.load("./skin/score-5.png").convert_alpha(),
    "6": pg.image.load("./skin/score-6.png").convert_alpha(),
    "7": pg.image.load("./skin/score-7.png").convert_alpha(),
    "8": pg.image.load("./skin/score-8.png").convert_alpha(),
    "9": pg.image.load("./skin/score-9.png").convert_alpha(),
    ".": pg.image.load("./skin/score-dot.png").convert_alpha(),
    "%": pg.image.load("./skin/score-percent.png").convert_alpha(),
}


class InGameUI:
    def __init__(
        self,
        difficulty_multiplier: int,
        mod_multiplier: float,
        background: pg.Surface,
        background_dim: float,
        monitor_size: t.Tuple[int, int],
    ) -> None:
        """Class of in game UI

        Parameters
        ----------
        difficulty_multiplier : int
            Map's difficulty multiplier
        mod_multiplier : float
            Map's mods score multiplier
        background : pg.Surface
            Background of the map
        background_dim : float
            Background dim. Can be changed using set_background_dim()
        monitor_size : t.Tuple[int, int]
            Sizes of monitor in pixels. (x, y)
        """

        self.score = 0
        self.display_score = 0
        self.combo = 0
        self.accuracy = ""

        self.scores = {"300": 0, "100": 0, "50": 0, "0": 0}

        self.difficulty_multiplier = difficulty_multiplier
        self.mod_multiplier = mod_multiplier

        self.raw_background = self.background_resize(background, monitor_size)
        self.bg_dim = background_dim
        self.background = self.get_dimmed_bg().convert()

    def hit(self, score: int):
        """Updates score with hit score"""
        self.scores[str(score)] += 1
        if score != 0:
            self.score += score * (
                1
                + (
                    max(self.combo - 1, 0)
                    * self.difficulty_multiplier
                    * self.mod_multiplier
                    / 25
                )
            )
            self.combo += 1
        else:
            self.combo = 0
        self.accuracy = (
            str(round(utils.calculate_accuracy(self.scores.values()) * 100, 1)) + "%"
        )

    def draw_score(self, screen: pg.Surface):
        """Draws score and accuracy on top right side of surface"""
        add_value = round((self.score - self.display_score) * 0.2)
        if add_value > 1:
            self.display_score += add_value
        else:
            self.display_score = self.score
        score = round(self.display_score)
        score_length = len(str(score))
        numbers = ["0"] * max(score_length, 8)
        for i, v in enumerate(str(score)):
            numbers[(score_length - i) * (-1)] = v
        screen_width = screen.get_size()[0]
        draw_point = screen_width - len(numbers) * 25 - 10
        for i, v in enumerate(numbers):
            screen.blit(score_imgs[v], (draw_point + i * 25, 10))
        draw_point = screen_width - len(self.accuracy) * 25 + 10
        for i, v in enumerate(self.accuracy):
            screen.blit(score_imgs[v], (draw_point + i * 20, 50))

    def draw_background(self, screen: pg.Surface):
        """Draws background"""
        if self.bg_dim < 1:
            screen.blit(self.background, (0, 0))

    def get_dimmed_bg(self):
        """Returns dimmed background, uses self.raw_background and self.bg_dim"""
        bg = self.raw_background.copy()
        bg.set_alpha(255 - self.bg_dim * 255)
        return bg.convert_alpha()

    def set_background_dim(self, dim: float):
        """Sets background dim"""
        self.bg_dim = dim
        self.background = self.get_dimmed_bg()

    def background_resize(self, background: pg.Surface, size: t.Tuple[int, int]):
        """Sets sizes of background image and keeping aspect ratio"""
        WIDTH = 0
        HEIGHT = 1
        bg = background.get_size()
        smaller_side = WIDTH if bg[WIDTH] < bg[HEIGHT] else HEIGHT
        scale = size[smaller_side] / bg[smaller_side]
        return pg.transform.scale(background, (bg[WIDTH] * scale, bg[HEIGHT] * scale))
