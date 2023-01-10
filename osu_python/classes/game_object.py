import pygame as pg


APPR_SIZE = 150
HIT_SIZE = 50


class Spinner:
    ...


class Circle(pg.sprite.Sprite):
    appr_circle = pg.transform.scale(
        pg.image.load("./skin/approachcircle.png"), (APPR_SIZE, APPR_SIZE)
    )
    hit_circle = pg.transform.scale(
        pg.image.load("./skin/hitcircle.png"), (HIT_SIZE, HIT_SIZE)
    )

    def __init__(
        self,
        timing: int,
        appear_time: int,
        fade_in_time: int,
        location: tuple,
        new_combo: bool,
        sound_types: tuple,
        hit_size: tuple,
        appr_size: tuple,
        *group
    ):
        """Circle object

        Draws hit circle and approach circle, handles circle hit

        Parameters
        ----------
        timing : int
            Hit time of circle
        appear_time : int
            Time when circle will start fade_in phase (pre-calculated from AR)
        fade_in_time : int
            Time when hit circle should reach 100% opacity (pre-calculated from AR)
        location : tuple
            Location of circle
        new_combo : bool
            Should circle start new combo?
        sound_types : tuple:
            Which sounds should circle emit when clicked
        hit_size : tuple:
            Size of hit circle (in px, not osu!pixels!)
        appr_size : tuple:
            Size of approach circle (in px, not osu!pixels!)
        """

        super().__init__(*group)

        self.timing = timing
        self.appear_time = appear_time
        self.fade_in_time = fade_in_time
        self.new_combo = new_combo
        self.sound_types = sound_types

        self.hit_size = hit_size
        self.shrink_pms = (appr_size - hit_size) / (timing - appear_time)
        self.fade_pms = 255 / (timing - fade_in_time)

        self.rect = Circle.hit_circle.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]

    def draw_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle from current time"""
        new_size = (self.timing - time) * self.shrink_pms
        size_diff = (new_size - self.hit_size) / 2
        screen.blit(
            pg.transform.scale(Circle.appr_circle, (new_size, new_size)),
            (self.rect.x - size_diff, self.rect.y - size_diff),
        )

    def draw_hit_circle(self, screen: pg.Surface, time: int):
        """Draws hit circle from current time"""
        circle = Circle.hit_circle.copy()
        circle.set_alpha((time - self.appear_time) * self.fade_pms)
        screen.blit(circle, self.rect)

    def draw(self, screen: pg.Surface, time: int):
        """Draws approach and hit circles from time"""
        self.draw_appr_circle(screen, time)
        self.draw_hit_circle(screen, time)

    def hit(self, time: int, pos: tuple):
        """Called when player clicks circle. Colission should be checked manually

        Parameters
        ----------
        time : int
            Current time
        pos : tuple:
            Position of cursour
        """
        raise NotImplemented


class Slider(Circle):
    ...
