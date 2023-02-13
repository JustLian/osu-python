import pygame as pg
import typing as t
from screeninfo import get_monitors
from osu_python.classes import Config, cursor, ingameui
from logging import getLogger
from os.path import isdir
from math import degrees, atan2


log = getLogger("game_object")

score_300_img = None
score_100_img = None
score_50_img = None
miss_img = None
combo_numbers = None


def load_skin():
    global score_300_img, score_100_img, score_50_img, miss_img, combo_numbers, Circle, Slider

    log.info("Reloading skin")
    Config.load_skin_ini()
    path = Config.base_path + "/skins/" + Config.cfg["skin"]

    if not isdir(path):
        log.info("Chosen skin doesn't exists. Switching to default skin.")
        Config.cfg["skin"] = "default"
        Config.dump()

    path = Config.base_path + "/skins/" + Config.cfg["skin"]
    combo_path = (
        path + "/" + Config.skin_ini["[Fonts]"]["HitCirclePrefix"].replace("\\", "/")
    )

    # global images
    score_300_img = pg.image.load(path + "/hit300.png").convert_alpha()
    score_100_img = pg.image.load(path + "/hit100.png").convert_alpha()
    score_50_img = pg.image.load(path + "/hit50.png").convert_alpha()
    miss_img = pg.image.load(path + "/hit0.png").convert_alpha()
    combo_numbers = {
        "0": pg.image.load(combo_path + "-0.png").convert_alpha(),
        "1": pg.image.load(combo_path + "-1.png").convert_alpha(),
        "2": pg.image.load(combo_path + "-2.png").convert_alpha(),
        "3": pg.image.load(combo_path + "-3.png").convert_alpha(),
        "4": pg.image.load(combo_path + "-4.png").convert_alpha(),
        "5": pg.image.load(combo_path + "-5.png").convert_alpha(),
        "6": pg.image.load(combo_path + "-6.png").convert_alpha(),
        "7": pg.image.load(combo_path + "-7.png").convert_alpha(),
        "8": pg.image.load(combo_path + "-8.png").convert_alpha(),
        "9": pg.image.load(combo_path + "-9.png").convert_alpha(),
    }
    # circle images
    Circle.hit_circle_img = pg.image.load(path + "/hitcircle.png").convert_alpha()
    Circle.hit_circle_overlay_img = pg.image.load(
        path + "/hitcircleoverlay.png"
    ).convert_alpha()
    Circle.appr_circle_img = pg.image.load(path + "/approachcircle.png").convert_alpha()

    # slider images
    Slider.hit_circle_img = pg.image.load(path + "/hitcircle.png").convert_alpha()
    Slider.hit_circle_overlay_img = pg.image.load(
        path + "/hitcircleoverlay.png"
    ).convert_alpha()
    Slider.appr_circle_img = pg.image.load(path + "/approachcircle.png").convert_alpha()
    frames_amount = Config.skin_ini["[General]"]["SliderBallFrames"]
    frames = []
    for i in range(frames_amount):
        try:
            frames.append(pg.image.load(path + f"/sliderb{i}.png").convert_alpha())
        except FileNotFoundError:
            break
    Slider.slider_ball_frames_img = frames

    # spinner images
    Spinner.appr_circle_img = pg.image.load(
        path + "/spinner-approachcircle.png"
    ).convert_alpha()
    Spinner.bottom_img = pg.image.load(path + "/spinner-bottom.png").convert_alpha()
    Spinner.top_img = pg.image.load(path + "/spinner-top.png").convert_alpha()
    Spinner.glow_img = pg.image.load(path + "/spinner-glow.png").convert_alpha()
    Spinner.middle_img = pg.image.load(path + "/spinner-middle.png").convert_alpha()
    Spinner.middle2_img = pg.image.load(path + "/spinner-middle2.png").convert_alpha()

    # cursor images
    cursor.load_skin()

    # ingameui images
    ingameui.load_skin()

    log.info("Skin reloaded")


class Spinner(pg.sprite.Sprite):
    appr_circle_img = None
    bottom_img = None
    top_img = None
    glow_img = None
    middle_img = None
    middle2_img = None

    def __init__(
        self,
        hit_time: int,
        appear_time: int,
        fade_in_time: int,
        location: tuple,
        sound_types: tuple,
        hit_size: int,
        appr_size: int,
        miss_callback: t.Callable,
        end_time: int,
        *group,
    ):
        """Spinner object

        Draws spinner within approach circle, handles spin events

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
        end_time : int
            Endtime of spinner
        """

        super().__init__(*group)

        self.hit_size = hit_size
        self.appr_size = appr_size

        self.circles_adding()

        self.score = None

        self.hit_time = hit_time
        self.appear_time = appear_time
        self.fade_in_time = fade_in_time
        self.endtime = end_time

        self.sound_types = sound_types

        self.rect = self.bottom.get_rect()
        self.rect.x, self.rect.y = location[0], location[1]

    def circles_adding(self):
        coeff = self.hit_size / (Spinner.bottom_img.get_size()[0])

        bottom_size = self.hit_size
        top_size = Spinner.top_img.get_size()[0] * coeff
        glow_size = Spinner.glow_img.get_size()[0] * coeff
        middle_size = Spinner.middle_img.get_size()[0] * coeff
        middle2_size = Spinner.middle2_img.get_size()[0] * coeff

        self.bottom = pg.transform.scale(
            Spinner.bottom_img, (bottom_size, bottom_size)
        ).convert_alpha()

        self.top = pg.transform.scale(
            Spinner.top_img, (top_size, top_size)
        ).convert_alpha()

        self.glow = pg.transform.scale(
            Spinner.glow_img, (glow_size, glow_size)
        ).convert_alpha()

        self.middle = pg.transform.scale(
            Spinner.middle_img, (middle_size, middle_size)
        ).convert_alpha()

        self.middle2 = pg.transform.scale(
            Spinner.middle2_img, (middle2_size, middle2_size)
        ).convert_alpha()

        self.appr_circle = pg.transform.scale(
            Spinner.appr_circle_img, (self.appr_size, self.appr_size)
        ).convert_alpha()
    
    def draw(self, screen: pg.Surface, time: int):
        """Controls drawing processes"""
        self.draw_glow(screen, time)
        self.draw_bottom(screen, time)
        self.draw_top(screen, time)
        self.draw_middle2(screen, time)
        self.draw_middle(screen, time)
        self.draw_appr_circle(screen, time)

    def draw_glow(self, screen: pg.Surface, time: int):
        """Draws glow"""
        diff = self.glow.get_size()[0] / 2

        screen.blit(self.glow, (self.rect.x - diff, self.rect.y - diff))

    def draw_bottom(self, screen: pg.Surface, time: int):
        """Draw bottom"""
        screen.blit(self.bottom, (self.rect.x, self.rect.y))

    def draw_top(self, screen: pg.Surface, time: int):
        """Draws top"""
        diff = self.top.get_size()[0] / 2

        screen.blit(self.top, (self.rect.x - diff, self.rect.y - diff))

    def draw_middle2(self, screen: pg.Surface, time: int):
        """Draws middle2"""
        diff = self.middle2.get_size()[0] / 2

        screen.blit(self.middle2, (self.rect.x - diff, self.rect.y - diff))

    def draw_middle(self, screen: pg.Surface, time: int):
        """Draws middle"""
        diff = self.middle.get_size()[0] / 2

        screen.blit(self.middle, (self.rect.x - diff, self.rect.y - diff))

    def draw_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle from current time"""
        diff = self.appr_circle.get_size()[0] / 2

        screen.blit(self.appr_circle, (self.rect.x - diff, self.rect.y - diff))


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
        hit_callback: t.Callable,
        *group,
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
        end_time : int
            Endtime of circle
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

        self.hit_callback = hit_callback

    def draw(self, screen: pg.Surface, time: int):
        """Controls drawing processes"""
        if self.score is None and time > self.endtime - 400:
            self.shortening = True
            if self.score != miss_img:
                self.score = miss_img
                self.hit_callback(0)
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
    slider_ball_frames_img = None

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
        hit_callback: t.Callable,
        body: t.Tuple[t.Tuple[int, int]],
        endtime: int,
        slider_border: t.Tuple[int, int, int],
        *group,
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
            Endtime of slider,
        slider_border : Tuple[int, int, int]
            Color of slider border
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
            hit_callback,
        )

        self.body = body
        self.edges = self.calc_slider_edges(self.body)

        self.slider_border = slider_border
        self.slider_offset = (hit_size / 2, hit_size / 2)
        self.surface = self.create_slider_surface().convert_alpha()
        self.begin_touch = False
        self.current_point_index = 0
        self.slider_ball_frame = 0

        self.endtime = endtime

        self.slider_ball_frames = []
        for frame in self.slider_ball_frames_img:
            self.slider_ball_frames.append(
                pg.transform.scale(
                    frame, (self.hit_size / 1.15, self.hit_size / 1.15)
                ).convert_alpha()
            )

        self.begin_touch = False
        self.touching = False

        self.current_point_index = 0
        self.velocity = len(self.body) / (self.endtime - self.hit_time)

        self.count_passed_points = 0
        self.count_points = 0

        self.drawing_score = False
        self.hit_callback = hit_callback

        self.combo_value = combo_value

    def calc_slider_edges(self, slider: list):
        """Calculates list of slider edges"""
        x = [p[0] for p in slider]
        y = [p[1] for p in slider]
        _min = [
            min(x),
            min(y),
        ]
        _max = [
            max(x),
            max(y),
        ]

        radius = round(self.hit_size // 2)
        _min[0] -= radius
        _min[1] -= radius
        _max[0] += radius
        _max[1] += radius

        return _min + _max

    def create_slider_surface(self):
        """Creates slider surfaces"""
        x = [v[0] for v in self.body]
        min_x = min(x)
        width = max(x) - min_x + self.hit_size
        y = [v[1] for v in self.body]
        min_y = min(y)
        height = max(y) - min_y + self.hit_size
        self.slider_offset = (min_x, min_y)
        surface = pg.Surface([width, height], pg.SRCALPHA, 32)
        for point in self.body:
            pg.draw.circle(
                surface,
                self.slider_border,
                (
                    point[0] - min_x + self.hit_size / 2,
                    point[1] - min_y + self.hit_size / 2,
                ),
                round(self.hit_size / 2.3),
            )
        precision = 25
        for iter in range(precision):
            _color = [iter * (60 / precision)] * 3
            _width = (precision - iter) * self.hit_size / precision
            for point in self.body:
                pg.draw.circle(
                    surface,
                    _color,
                    (
                        point[0] - min_x + self.hit_size / 2,
                        point[1] - min_y + self.hit_size / 2,
                    ),
                    round(_width / 2.6),
                )
        return surface

    def draw_body(self, screen: pg.Surface, time: int):
        """Draws slider's body for passed time"""
        body = self.surface.copy()
        body.set_alpha((time - self.appear_time) * self.fade_pms)
        screen.blit(body, self.slider_offset)

    def draw(self, screen: pg.Surface, time: int):
        """Draws slider for passed time"""
        if not self.drawing_score:
            self.draw_body(screen, time)
        if self.drawing_score == True:
            self.draw_score(screen, time)
        elif time > self.hit_time or self.begin_touch:
            self.draw_slider_ball(screen, time)
            self.count_points += 1
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

    def draw_slider_ball(self, screen: pg.Surface, time: int):
        """Draws slider ball on slider"""
        if round(self.velocity * (time - self.hit_time)) >= 1:
            ind = round(self.velocity * (time - self.hit_time)) - 1
            self.current_point_index = ind
            x, y = self.body[ind]
            self.rect.left, self.rect.top = x, y

            point_1 = self.body[min(ind, len(self.body) - 11)]
            point_2 = self.body[min(ind + 10, len(self.body) - 1)]
            angle = degrees(atan2(point_2[1] - point_1[1], point_2[0] - point_1[0]))

            frame = self.slider_ball_frames[self.slider_ball_frame]
            rotated_frame = pg.transform.rotate(frame, -angle)
            offset = (
                (rotated_frame.get_width() - frame.get_width()) // 2
                - (self.hit_size - self.hit_size / 1.15) / 2,
                (rotated_frame.get_height() - frame.get_height()) // 2
                - (self.hit_size - self.hit_size / 1.15) / 2,
            )
            screen.blit(rotated_frame, (x - offset[0], y - offset[1]))
            self.slider_ball_frame = (self.slider_ball_frame + 1) % len(
                self.slider_ball_frames
            )

            if self.current_point_index == 99:
                self.get_score()
                self.drawing_score = True
                self.endtime += 400

    def draw_body_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle on slider"""
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
        n = self.count_passed_points / self.count_points
        if n == 1.0:
            self.score = score_300_img
            self.hit_callback(300)
        elif n >= 0.5:
            self.score = score_100_img
            self.hit_callback(100)
        elif n >= 0.25:
            self.score = score_50_img
            self.hit_callback(50)
        else:
            self.score = miss_img
            self.hit_callback(0)
