import pygame as pg
from osu_python import __main__


class Spinner:
    ...


class Circle(pg.sprite.Sprite):
    def __init__(
        self,
        hit_time: int,
        appear_time: int,
        fade_in_time: int,
        location: tuple,
        new_combo: bool,
        sound_types: tuple,
        hit_size: int,
        appr_size: int,
        *group
    ):
        """Circle object

        Draws hit circle and approach circle, handles circle hit

        Parameters
        ----------
        hit_time : int
            Hit time of circle
        appear_time : int
            Time when circle will start fade_in phase (pre-calculated from AR)
        fade_in_time : int
            Time when hit circle should reach 100% opacity (pre-calculated from AR)
        location : tuple
            Location of circle
        new_combo : bool
            Should circle start new combo?
        sound_types : tuple
            Which sounds should circle emit when clicked
        hit_size : int
            Radius of hit circle (in px, not osu!pixels!)
        appr_size : int
            Radius of approach circle (in px, not osu!pixels!)
        """

        super().__init__(*group)

        self.hit_size = hit_size
        self.appr_size = appr_size

        self.hit_circle = pg.transform.scale(
            pg.image.load("./skin/hitcircle.png"), (self.hit_size, self.hit_size)
        )

        self.appr_circle = pg.transform.scale(
            pg.image.load("./skin/approachcircle.png"), (self.appr_size, self.appr_size)
        )

        self.hit_time = hit_time
        self.appear_time = appear_time
        self.fade_in_time = fade_in_time

        self.new_combo = new_combo
        self.sound_types = sound_types

        self.shrink_pms = (appr_size - hit_size) / (self.hit_time - fade_in_time)
        self.fade_pms = 255 / (self.hit_time - fade_in_time)

        self.rect = self.hit_circle.get_rect()
        self.rect.x, self.rect.y = location[0], location[1]

        self.is_hit = False
        self.vibration = 0
        self.no_hit_before = True
    
    def draw(self, screen: pg.Surface, time: int):
        """Draws approach, hit circles and score from time"""
        if self.is_hit and self.no_hit_before:
            if abs(self.hit_time - time) <= round(__main__.scores[0] / 2):
                score_image = pg.image.load('./skin/300score.png')
                self.no_hit_before = False
            elif (round(__main__.scores[0] / 2) + __main__.scores[1] >=
             abs(self.hit_time - time) > round(__main__.scores[0] / 2)):
                score_image = pg.image.load('./skin/100score.png')
                self.no_hit_before = False
            elif (round(__main__.scores[0] / 2) + __main__.scores[1] + __main__.scores[2] >=
             abs(self.hit_time - time) > round(__main__.scores[0] / 2) + __main__.scores[1]):
                score_image = pg.image.load('./skin/50score.png')
                self.no_hit_before = False
            elif self.hit_time - time > 0:
                score_image = pg.image.load('./skin/miss_score.png')
                self.no_hit_before = False
            elif self.hit_time - time < 0:
                self.vibration = 8

            screen.blit(score_image, (self.rect.x, self.rect.y))
        else:
            self.draw_appr_circle(screen, time)
            self.draw_hit_circle(screen, time)

    def draw_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle from current time"""
        new_size = self.appr_size - (time - self.fade_in_time) * self.shrink_pms
        if new_size != self.hit_size:
            size_diff = (new_size - self.hit_size) / 2
            screen.blit(
                pg.transform.scale(self.appr_circle, (new_size, new_size)),
                (self.rect.x - size_diff, self.rect.y - size_diff),
            )

    def draw_hit_circle(self, screen: pg.Surface, time: int):
        """Draws hit circle from current time"""
        circle = self.hit_circle.copy()
        circle.set_alpha((time - self.appear_time) * self.fade_pms)
        if self.vibration != 0:
            self.rect = self.rect.move(2 if self.vibration % 2 == 0 else -2, 0)
            self.vibration -= 1
        screen.blit(circle, self.rect)


class Slider(Circle):
    ...