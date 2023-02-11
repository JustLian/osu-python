import pygame as pg
from osu_python import utils
import typing as t
from osu_python.classes import Config


score_imgs = None


def load_skin():
    global score_imgs
    path = Config.base_path + "/skins/" + Config.cfg["skin"]
    score_path = path + "/" + Config.skin_ini["[Fonts]"]["ScorePrefix"]

    score_imgs = {
        "0": pg.image.load(score_path + "-0.png").convert_alpha(),
        "1": pg.image.load(score_path + "-1.png").convert_alpha(),
        "2": pg.image.load(score_path + "-2.png").convert_alpha(),
        "3": pg.image.load(score_path + "-3.png").convert_alpha(),
        "4": pg.image.load(score_path + "-4.png").convert_alpha(),
        "5": pg.image.load(score_path + "-5.png").convert_alpha(),
        "6": pg.image.load(score_path + "-6.png").convert_alpha(),
        "7": pg.image.load(score_path + "-7.png").convert_alpha(),
        "8": pg.image.load(score_path + "-8.png").convert_alpha(),
        "9": pg.image.load(score_path + "-9.png").convert_alpha(),
        ".": pg.image.load(score_path + "-dot.png").convert_alpha(),
        "%": pg.image.load(score_path + "-percent.png").convert_alpha(),
        "x": pg.image.load(score_path + "-x.png").convert_alpha(),
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
        self.accuracy = 1.00

        self.scores = {"300": 0, "100": 0, "50": 0, "0": 0}

        self.difficulty_multiplier = difficulty_multiplier
        self.mod_multiplier = mod_multiplier

        self.raw_background = self.background_resize(background, monitor_size)
        self.bg_dim = background_dim
        self.background = self.get_dimmed_bg().convert_alpha()

        full_width = 0
        for n in range(10):
            full_width += score_imgs[str(n)].get_width()
        self.num_gap = full_width / 10 + 2

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
        self.accuracy = utils.calculate_accuracy(self.scores.values())

    def draw(self, screen: pg.Surface):
        """Draws score and accuracy on top right side of surface"""
        add_value = round((self.score - self.display_score) * 0.2)
        if add_value > 1:
            self.display_score += add_value
        else:
            self.display_score = self.score

        # Score display
        score = str(round(self.display_score))
        numbers = "0" * (8 - len(score)) + score

        screen_width, screen_height = screen.get_size()
        offset_x = screen_width - 20
        for v in reversed(numbers):
            offset_x -= self.num_gap
            screen.blit(
                score_imgs[v], (offset_x + (20 - score_imgs[v].get_width()) / 2, 10)
            )

        # Accuracy display
        offset_x = screen_width - 20
        accuracy = str(round(self.accuracy * 100, 1)) + "%"
        for v in reversed(accuracy):
            gap = (
                self.num_gap
                if v in [str(n) for n in range(10)]
                else score_imgs[v].get_width()
            )
            offset_x -= gap
            screen.blit(
                score_imgs[v], (offset_x + (gap - score_imgs[v].get_width()) / 2, 80)
            )

        # Combo display
        for i, v in enumerate(str(self.combo) + "x"):
            screen.blit(
                score_imgs[v],
                (
                    i * self.num_gap + (40 - score_imgs[v].get_width()) / 2,
                    screen_height - score_imgs["1"].get_height() - 5,
                ),
            )

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
