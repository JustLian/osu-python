import pygame as pg
import typing as t
from screeninfo import get_monitors

score_300_img = pg.image.load("./skin/300score.png")
score_100_img = pg.image.load("./skin/100score.png")
score_50_img = pg.image.load("./skin/50score.png")
miss_img = pg.image.load("./skin/miss_score.png")
num = 1

class Spinner:
    ...


class Circle(pg.sprite.Sprite):
    hit_circle_img = pg.image.load("./skin/hitcircle.png")
    appr_circle_img = pg.image.load("./skin/approachcircle.png")

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
        hit_windows: t.Tuple[int, int, int],
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
        hit_windows : Tuple[int, int, int]
            Hit windows for 300, 100 and 50
        """

        super().__init__(*group)

        self.hit_size = hit_size
        self.appr_size = appr_size

        self.hit_windows = hit_windows

        self.hit_circle = pg.transform.scale(
            Circle.hit_circle_img, (self.hit_size, self.hit_size)
        )

        self.appr_circle = pg.transform.scale(
            Circle.appr_circle_img, (self.appr_size, self.appr_size)
        )

        self.score = None

        self.hit_time = hit_time
        self.appear_time = appear_time
        self.fade_in_time = fade_in_time
        self.endtime = (
            hit_time + hit_windows[0] / 2 + hit_windows[1] + hit_windows[2] + 400
        )

        self.new_combo = new_combo
        self.sound_types = sound_types

        self.shrink_pms = (appr_size - hit_size) / (self.hit_time - fade_in_time)
        self.fade_pms = 255 / (self.hit_time - fade_in_time)

        self.rect = self.hit_circle.get_rect()
        self.rect.x, self.rect.y = location[0], location[1]

        self.shortening = False

    def draw(self, screen: pg.Surface, time: int):
        """Controls drawing processes"""
        if self.score is None and time > self.endtime - 400:
            self.shortening = True
            self.score = miss_img
            self.draw_score(screen, time)

        elif self.score is None:
            self.draw_appr_circle(screen, time)
            self.draw_hit_circle(screen, time)

        else:
            if not self.shortening:
                self.endtime = time + 400
                self.shortening = True
            self.draw_score(screen, time)

    def hit(self, time: int):
        """Controls hit events"""
        if time <= self.endtime - 400:
            if abs(self.hit_time - time) <= round(self.hit_windows[0] / 2):
                self.score = score_300_img
            elif (
                round(self.hit_windows[0] / 2) + self.hit_windows[1]
                >= abs(self.hit_time - time)
                > round(self.hit_windows[0] / 2)
            ):
                self.score = score_100_img
            elif (
                round(self.hit_windows[0] / 2)
                + self.hit_windows[1]
                + self.hit_windows[2]
                >= abs(self.hit_time - time)
                > round(self.hit_windows[0] / 2) + self.hit_windows[1]
            ):
                self.score = score_50_img

        # not vibration working properly

    def draw_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle from current time"""
        if time <= self.hit_time:
            new_size = self.appr_size - (time - self.fade_in_time) * self.shrink_pms
            size_diff = (new_size - self.hit_size) / 2
            screen.blit(
                pg.transform.scale(self.appr_circle, (new_size, new_size)),
                (self.rect.x - size_diff, self.rect.y - size_diff),
            )

    def draw_hit_circle(self, screen: pg.Surface, time: int):
        """Draws hit circle from current time"""
        if self.fade_in_time > time >= self.appear_time:
            circle = self.hit_circle.copy()
            circle.set_alpha((time - self.appear_time) * self.fade_pms)
            screen.blit(circle, self.rect)
        else:
            screen.blit(self.hit_circle, self.rect)

    def draw_score(self, screen: pg.Surface, time: int):
        """Draws score from current time"""
        need = (time - self.hit_time + 400) // 100
        score = self.score.copy()
        w, h = score.get_size()

        score.set_alpha(255 - (255 / 400) * (time - self.endtime + 400))
        score = pg.transform.scale(score, (w + need, h + need))

        screen.blit(
            score,
            (
                self.rect.left + round((self.rect.width / 2) - (w / 2)),
                self.rect.top + round((self.rect.height / 2) - (h / 2)),
            ),
        )


class Slider(Circle):
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
        hit_windows: t.Tuple[int, int, int],
        body: t.Tuple[t.Tuple[int, int]],
        *group
    ):
        """Slider object

        Draws slider body, approach circle and handles hit event

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
        hit_windows : Tuple[int, int, int]
            Hit windows for 300, 100 and 50
        body : Tuple[Tuple[int, int]]:
            Coordinates of points in slider's body
        """

        super().__init__(
            hit_time,
            appear_time,
            fade_in_time,
            location,
            new_combo,
            sound_types,
            hit_size,
            appr_size,
            hit_windows,
        )

        self.body = body
        self.surface = self.create_slider_surface()
        global num
        print(f'slider #{num}')
        num += 1
    
    def distance_to_point(self, point: tuple, point_2: tuple):
        """Calculates distance between two points""" 
        x1, y1 = point
        x2, y2 = point_2
        dist = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        return dist


    def calc_slider_edges(self, slider: list):
        """Calculates list of slider edges"""
        _min = [10000, 10000]
        _max = [0, 0]
        for point in slider:
            if point[0] < _min[0]:
                _min[0] = int(point[0])
            if point[1] < _min[1]:
                _min[1] = int(point[1])
            if point[0] > _max[0]:
                _max[0] = int(point[0])
            if point[1] > _max[1]:
                _max[1] = int(point[1])
        
        radius = round(self.hit_size // 2)
        _min[0] -= radius
        _min[1] -= radius
        _max[0] += radius
        _max[1] += radius
        
        return _min + _max


    def create_slider_surface(self):
        edges = self.calc_slider_edges(self.body)
        slider_width = edges[2] - edges[0]
        slider_height = edges[3] - edges[1]
        print(edges, slider_width, slider_height)

        # TODO: бро умри и оптимизуй
        for m in get_monitors():
            if m.is_primary:
                width, height = m.width, m.height

        surface = pg.Surface([width, height], pg.SRCALPHA, 32)
        for x in range(edges[0], slider_width + edges[0]):
            for y in range(edges[1], slider_height + edges[1]):
                dist = min(
                    [self.distance_to_point((x, y), d) for d in self.body]
                    ) / self.hit_size * 145
                if dist > 255:
                    continue
                surface.set_at((x, y), (dist, dist, dist))
        return surface


    def draw_body(self, screen: pg.Surface, time: int):
        """Draws slider's body for passed time"""
        screen.blit(self.surface, [0, 0])


    def draw(self, screen: pg.Surface, time: int):
        """Draws slider for passed time"""
        self.draw_body(screen, time)
        # self.draw_appr_circle(screen, time)
