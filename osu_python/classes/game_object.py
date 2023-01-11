import pygame as pg


class Spinner:
    ...


class Circle(pg.sprite.Sprite):
    def __init__(
        self,
        timing: int,
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

        self.timing = timing
        self.appear_time = appear_time
        self.fade_in_time = fade_in_time
        self.new_combo = new_combo
        self.sound_types = sound_types

        self.shrink_pms = (appr_size - hit_size) / (timing - appear_time)
        self.fade_pms = 255 / (timing - fade_in_time)

        self.rect = self.hit_circle.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]

    def draw_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle from current time"""
        new_size = abs(self.timing - time) * self.shrink_pms
        size_diff = (new_size - self.hit_size) / 2
        screen.blit(
            pg.transform.scale(self.appr_circle, (new_size, new_size)),
            (self.rect.x - size_diff, self.rect.y - size_diff),
        )

    def draw_hit_circle(self, screen: pg.Surface, time: int):
        """Draws hit circle from current time"""
        circle = self.hit_circle.copy()
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
