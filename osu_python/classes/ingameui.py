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
    "%": pg.image.load("./skin/score-percent.png")
}


class InGameUI():
    """Class of in game UI"""
    def __init__(self, difficulty_multiplier = 1, mod_multiplier = 1) -> None:
        self.score = 0
        self.combo = 1524
        self.accuracy = ""
        self.scores = {
            "300": 0,
            "100": 0,
            "50": 0,
            "0": 0
        }
        self.difficulty_multiplier = difficulty_multiplier
        self.mod_multiplier = mod_multiplier
        
    def hit(self, score):
        self.scores[str(score)] += 1
        if score != 0:
            self.score += score * (1 + (max(self.combo - 1, 0) * self.difficulty_multiplier * self.mod_multiplier / 25))
            self.combo += 1
        else:
            self.combo = 0
        self.accuracy = str(round(utils.calculate_accuracy(self.scores.values()) * 100, 1)) + "%"
    
    def draw_score(self, screen: pg.Surface):
        score = round(self.score)
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

