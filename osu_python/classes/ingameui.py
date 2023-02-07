import pygame as pg
from osu_python import utils

score_imgs = {
    "0": pg.image.load("./skin/score-0.png"),
    "1": pg.image.load("./skin/score-1.png"),
    "2": pg.image.load("./skin/score-2.png"),
    "3": pg.image.load("./skin/score-3.png"),
    "4": pg.image.load("./skin/score-4.png"),
    "5": pg.image.load("./skin/score-5.png"),
    "6": pg.image.load("./skin/score-6.png"),
    "7": pg.image.load("./skin/score-7.png"),
    "8": pg.image.load("./skin/score-8.png"),
    "9": pg.image.load("./skin/score-9.png"),
    ".": pg.image.load("./skin/score-dot.png"),
    "%": pg.image.load("./skin/score-percent.png"),
}


class InGameUI:
    def __init__(
        self,
        difficulty_multiplier : int,
        mod_multiplier : float,
    ) -> None:
        """Class of in game UI
        
        Parameters
        ----------
        difficulty_multiplier : int
            Map's difficulty multiplier
        mod_multiplier : float
            Map's mods score multiplier
        """

        self.score = 0
        self.display_score = 0
        self.combo = 0
        self.accuracy = ""

        self.scores = {"300": 0, "100": 0, "50": 0, "0": 0}

        self.difficulty_multiplier = difficulty_multiplier
        self.mod_multiplier = mod_multiplier

    def hit(self, score: float):
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
