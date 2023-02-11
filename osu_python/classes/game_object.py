import pygame as pg
import typing as t
from screeninfo import get_monitors
from osu_python.classes import Config, cursor, ingameui
from logging import getLogger
from os.path import isdir


log = getLogger("game_object")

score_300_img = None
score_100_img = None
score_50_img = None
miss_img = None
combo_numbers = None


def load_skin():
    global score_300_img, score_100_img, score_50_img, miss_img, combo_numbers, Circle, Slider

    log.info("Reloading skin")
    path = Config.base_path + "/skins/" + Config.cfg["skin"]

    if not isdir(path):
        log.info("Chosen skin doesn't exists. Switching to default skin.")
        Config.cfg['skin'] = 'default'
        Config.dump()
    
    path = Config.base_path + "/skins/default"

    # global images
    score_300_img = pg.image.load(path + "/hit300.png").convert_alpha()
    score_100_img = pg.image.load(path + "/hit100.png").convert_alpha()
    score_50_img = pg.image.load(path + "/hit50.png").convert_alpha()
    miss_img = pg.image.load(path + "/hit0.png").convert_alpha()
    combo_numbers = {
        "0": pg.image.load(path + "/default-0.png").convert_alpha(),
        "1": pg.image.load(path + "/default-1.png").convert_alpha(),
        "2": pg.image.load(path + "/default-2.png").convert_alpha(),
        "3": pg.image.load(path + "/default-3.png").convert_alpha(),
        "4": pg.image.load(path + "/default-4.png").convert_alpha(),
        "5": pg.image.load(path + "/default-5.png").convert_alpha(),
        "6": pg.image.load(path + "/default-6.png").convert_alpha(),
        "7": pg.image.load(path + "/default-7.png").convert_alpha(),
        "8": pg.image.load(path + "/default-8.png").convert_alpha(),
        "9": pg.image.load(path + "/default-9.png").convert_alpha(),
    }
    # circle images
    Circle.hit_circle_img = pg.image.load(path + "/hitcircle.png").convert_alpha()
    Circle.hit_circle_overlay_img = pg.image.load(path + "/hitcircleoverlay.png").convert_alpha()
    Circle.appr_circle_img = pg.image.load(path + "/approachcircle.png").convert_alpha()

    # slider images
    Slider.hit_circle_img = pg.image.load(path + "/hitcircle.png").convert_alpha()
    Slider.hit_circle_overlay_img = pg.image.load(path + "/hitcircleoverlay.png").convert_alpha()
    Slider.appr_circle_img = pg.image.load(path + "/approachcircle.png").convert_alpha()

    # cursor images
    cursor.load_skin()

    # ingameui images
    ingameui.load_skin()

    log.info("Skin reloaded")


class Spinner:
    ...


class Circle(pg.sprite.Sprite):
    hit_circle_img = None
    hit_circle_overlay_img = None
    appr_circle_img = None

    def __init__(
        self,
        hit_time: int,
        appear_time: int,
        fade_in_time: int,
        location: tuple,
        combo_value: int,
        combo_color: t.Tuple[int, int, int],
        sound_types: tuple,
        hit_size: int,
        appr_size: int,
        hit_windows: t.Tuple[int, int, int],
        miss_callback: t.Callable,
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
        combo_value : int
            Combo value of circle
        combo_color : Tuple[int, int, int]
            Color of circle
        sound_types : tuple
            Which sounds should circle emit when clicked
        hit_size : int
            Radius of hit circle (in px, not osu!pixels!)
        appr_size : int
            Radius of approach circle (in px, not osu!pixels!)
        hit_windows : Tuple[int, int, int]
            Hit windows for 300, 100 and 50
        miss_callback : t.Callable
            Miss callback function
        """

        super().__init__(*group)

        self.hit_size = hit_size
        self.appr_size = appr_size

        self.hit_windows = hit_windows

        self.hit_circle = pg.transform.scale(
            Circle.hit_circle_img, (self.hit_size, self.hit_size)
        ).convert_alpha()

        self.hit_circle_overlay = pg.transform.scale(
            Circle.hit_circle_overlay_img, (self.hit_size, self.hit_size)
        ).convert_alpha()

        self.appr_circle = pg.transform.scale(
            Circle.appr_circle_img, (self.appr_size, self.appr_size)
        ).convert_alpha()

        self.score = None

        self.hit_time = hit_time
        self.appear_time = appear_time
        self.fade_in_time = fade_in_time
        self.endtime = (
            hit_time + hit_windows[0] / 2 + hit_windows[1] + hit_windows[2] + 400
        )

        self.combo_value = combo_value
        self.color = combo_color
        self.sound_types = sound_types

        self.shrink_pms = (appr_size - hit_size) / (self.hit_time - fade_in_time)
        self.fade_pms = 255 / (self.hit_time - fade_in_time)

        self.rect = self.hit_circle.get_rect()
        self.rect.x, self.rect.y = location[0], location[1]

        self.shortening = False
        self.count_vibr = 0

        self.miss_callback = miss_callback

    def draw(self, screen: pg.Surface, time: int):
        """Controls drawing processes"""
        if self.score is None and time > self.endtime - 400:
            self.shortening = True
            if self.score != miss_img:
                self.score = miss_img
                self.miss_callback()
            self.draw_score(screen, time)

        elif self.score is None:
            self.draw_appr_circle(screen, time)
            self.draw_hit_circle(screen, time)
            self.draw_combo_value(screen, time)

        else:
            if not self.shortening:
                self.endtime = time + 400
                self.shortening = True
            self.draw_score(screen, time)

    def hit(self, time: int):
        """Controls hit events"""
        if time <= self.endtime - 400:
            if abs(self.hit_time - time) <= self.hit_windows[0]:
                self.score = score_300_img
                return 300
            elif self.hit_windows[1] >= abs(self.hit_time - time) > self.hit_windows[0]:
                self.score = score_100_img
                return 100
            elif self.hit_windows[2] >= abs(self.hit_time - time) > self.hit_windows[1]:
                self.score = score_50_img
                return 50
            elif self.hit_time - time > 0:
                self.count_vibr = 20

    def draw_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle from current time"""
        if self.fade_in_time > time >= self.appear_time:
            appr_circle = self.appr_circle.copy()
            appr_circle.fill(self.color, special_flags=3)
            appr_circle.set_alpha((time - self.appear_time) * self.fade_pms / 2)
        else:
            appr_circle = self.appr_circle.copy()
            appr_circle.fill(self.color, special_flags=3)
        if time <= self.hit_time:
            new_size = self.appr_size - (time - self.fade_in_time) * self.shrink_pms
            size_diff = (new_size - self.hit_size) / 2
            screen.blit(
                pg.transform.scale(appr_circle, (new_size, new_size)),
                (self.rect.x - size_diff, self.rect.y - size_diff),
            )

    def draw_hit_circle(self, screen: pg.Surface, time: int):
        """Draws hit circle from current time"""
        if self.fade_in_time > time >= self.appear_time:
            circle = self.hit_circle.copy()
            circle.fill(self.color, special_flags=3)
            circle.blit(self.hit_circle_overlay, (0, 0))
            circle.set_alpha((time - self.appear_time) * self.fade_pms)
        else:
            circle = self.hit_circle.copy()
            circle.fill(self.color, special_flags=3)
            circle.blit(self.hit_circle_overlay, (0, 0))

        offset = 0
        if self.count_vibr != 0:
            if self.count_vibr % 2 == 0:
                offset = -3
            else:
                offset = 3
            self.count_vibr -= 1

        screen.blit(circle, (self.rect[0] + offset, self.rect[1]))

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

    def draw_combo_value(self, screen: pg.Surface, time: int):
        center = (self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2)
        full_width = 0
        for v in str(self.combo_value):
            full_width += combo_numbers[v].get_width()
        x = center[0] - full_width / 2
        y = center[1] - (combo_numbers["0"].get_height() / 2) + 1

        offset = 0
        if self.count_vibr != 0:
            if self.count_vibr % 2 == 0:
                offset = -3
            else:
                offset = 3

        for v in str(self.combo_value):
            img = combo_numbers[v].copy()
            img.set_alpha((time - self.appear_time) * self.fade_pms)
            screen.blit(
                img,
                (x - offset, y),
            )
            x += img.get_width()


class Slider(Circle):
    hit_circle_img = None
    hit_circle_overlay_img = None
    appr_circle_img = None

    def __init__(
        self,
        hit_time: int,
        appear_time: int,
        fade_in_time: int,
        location: tuple,
        combo_value: int,
        combo_color: t.Tuple[int, int, int],
        sound_types: tuple,
        hit_size: int,
        appr_size: int,
        hit_windows: t.Tuple[int, int, int],
        miss_callback: t.Callable,
        body: t.Tuple[t.Tuple[int, int]],
        endtime: int,
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
        combo_value : int
            Combo value of circle
        sound_types : tuple
            Which sounds should circle emit when clicked
        hit_size : int
            Radius of hit circle (in px, not osu!pixels!)
        appr_size : int
            Radius of approach circle (in px, not osu!pixels!)
        hit_windows : Tuple[int, int, int]
            Hit windows for 300, 100 and 50
        miss_callback : t.Callable
            Miss callback function
        body : Tuple[Tuple[int, int]]:
            Coordinates of points in slider's body
        endtime : int
            Endtime of slider
        """

        super().__init__(
            hit_time,
            appear_time,
            fade_in_time,
            location,
            combo_value,
            combo_color,
            sound_types,
            hit_size,
            appr_size,
            hit_windows,
            miss_callback,
        )

        self.body = body
        self.edges = self.calc_slider_edges(self.body)

        self.surface = self.create_slider_surface().convert_alpha()
        self.begin_touch = False
        self.current_point_index = 0

        self.endtime = endtime

        self.begin_touch = False
        self.touching = False

        self.current_point_index = 0
        self.velocity = len(self.body) / (self.endtime - self.hit_time)
        self.count_passed_points = 0

        self.drawing_score = False

        self.combo_value = combo_value

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
        """Creates slider surfaces"""
        for m in get_monitors():
            if m.is_primary:
                width, height = m.width, m.height
        surface = pg.Surface([width, height], pg.SRCALPHA, 32)
        precision = 50
        for iter in range(precision):
            _color = [255 - iter * (255 / precision)] * 3
            _width = (precision - iter) * self.hit_size / precision
            for point in self.body:
                pg.draw.circle(surface, _color, (point[0], point[1]), round(_width / 2.5))
        return surface

    def draw_body(self, screen: pg.Surface, time: int):
        """Draws slider's body for passed time"""
        body = self.surface.copy()
        body.set_alpha((time - self.appear_time) * self.fade_pms)
        screen.blit(body, [self.hit_size / 2, self.hit_size / 2])

    def draw(self, screen: pg.Surface, time: int):
        """Draws slider for passed time"""
        self.draw_body(screen, time)
        if self.drawing_score == True:
            self.draw_score(screen, time)
        elif time > self.hit_time or self.begin_touch:
            self.draw_slider_circle(screen, time)
            if self.touching:
                self.draw_body_appr_circle(screen, time)
                self.count_passed_points += 1
        else:
            self.draw_appr_circle(screen, time)
            self.draw_hit_circle(screen, time)
            self.draw_combo_value(screen, time)

    def hit(self, time: int):
        """Controls hit events"""
        if time > self.hit_time:
            self.touching = True
        else:
            if self.hit_time - time <= self.hit_windows[2]:
                self.begin_touch = True
                self.touching = True

    def draw_slider_circle(self, screen: pg.Surface, time: int):
        """Draws hit circle on slider"""
        if round(self.velocity * (time - self.hit_time)) >= 1:
            self.current_point_index = round(self.velocity * (time - self.hit_time)) - 1
            x, y = self.body[self.current_point_index]
            self.rect.left, self.rect.top = x, y
            screen.blit(self.hit_circle, (x, y))

            if self.current_point_index == 99:
                self.get_score()
                self.drawing_score = True
                self.endtime += 400

    def draw_body_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle on slider, not working properly"""
        if (time - self.hit_time) // 250 % 2 == 0:
            coeff = 0.9
        else:
            coeff = 1

        new_size = self.appr_size * coeff
        size_diff = (new_size - self.hit_size) / 2
        screen.blit(
            pg.transform.scale(self.appr_circle, (new_size, new_size)).convert_alpha(),
            (self.rect.x - size_diff, self.rect.y - size_diff),
        )

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

    def get_score(self):
        """Gets score (used in drawing score)"""
        n = self.count_passed_points / len(self.body)
        if n == 1.0:
            self.score = score_300_img
        elif n >= 0.5:
            self.score = score_100_img
        elif n >= 0.25:
            self.score = score_50_img
        else:
            self.score = miss_img
