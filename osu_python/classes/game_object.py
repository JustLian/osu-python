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
    try:
        Slider.tick_point_img = pg.image.load(
            path + "/sliderscorepoint.png"
        ).convert_alpha()
    except FileNotFoundError:
        pass
    Slider.slider_follow_circle = pg.image.load(
        path + "/sliderfollowcircle.png"
    ).convert_alpha()

    try:
        frames_amount = Config.skin_ini["[General]"]["SliderBallFrames"]
    except KeyError:
        frames_amount = 60
    frames = []
    for i in range(frames_amount):
        try:
            frames.append(pg.image.load(path + f"/sliderb{i}.png").convert_alpha())
        except FileNotFoundError:
            break
    Slider.slider_ball_frames_img = frames

    try:
        Slider.slider_track_override = Config.skin_ini["[Colours]"][
            "SliderTrackOverride"
        ]
    except KeyError:
        pass

    # spinner images
    Spinner.appr_circle_img = pg.image.load(
        path + "/spinner-approachcircle.png"
    ).convert_alpha()
    Spinner.bottom_img = pg.image.load(path + "/spinner-bottom.png").convert_alpha()
    Spinner.top_img = pg.image.load(path + "/spinner-top.png").convert_alpha()
    Spinner.glow_img = pg.image.load(path + "/spinner-glow.png").convert_alpha()
    Spinner.middle_img = pg.image.load(path + "/spinner-middle.png").convert_alpha()
    Spinner.middle2_img = pg.image.load(path + "/spinner-middle2.png").convert_alpha()
    Spinner.clear_img = pg.image.load(path + "/spinner-clear.png").convert_alpha()
    Spinner.spin_img = pg.image.load(path + "/spinner-spin.png").convert_alpha()

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
    clear_img = None
    spin_img = None

    def __init__(
        self,
        hit_time: int,
        appear_time: int,
        fade_in_time: int,
        end_time: int,
        bottom_top_size: int,
        glow_size: int,
        middle_size: int,
        middle2_size: int,
        spin_size: tuple,
        clear_size: tuple,
        appr_size: int,
        location: tuple,
        sound_types: tuple,
        miss_callback: t.Callable,
        hit_size,
        *group,
    ):
        """Spinner object

        Draws spinner within approach circle, Handles spin events

        Parameters
        ----------
        hit_time : int
            Hit time of circle
        appear_time : int
            Time when circle will start fade_in phase (pre-calculated from AR)
        fade_in_time : int
            Time when hit circle should reach 100% opacity (pre-calculated from AR)
        end_time : int
            Endtime of spinner
        bottom_top_size : int
            Radius of bottom and top in px
        glow_size : int
            Radius of glow in px
        middle_size : int
            Radius of middle in px
        middle2_size : int
            Radius of middle2 in px
        spin_size : tuple
            Width and height of spin in px
        clear_size : tuple
            Width and height of clear in px
        appr_size : int
            Radius of appr_circle in px
        location : tuple
            Location of circle
        sound_types : tuple
            Which sounds should circle emit when clicked
        miss_callback : t.Callable
            Miss callback function
        hit_size
            Uses in drawing score
        """

        super().__init__(*group)

        self.hit_time = hit_time
        self.appear_time = appear_time
        self.fade_in_time = fade_in_time
        self.endtime = end_time + 400

        self.bt_size = bottom_top_size
        self.appr_size = appr_size

        self.bottom = pg.transform.scale(
            Spinner.bottom_img, (bottom_top_size, bottom_top_size)
        )
        self.top = pg.transform.scale(
            Spinner.top_img, (bottom_top_size, bottom_top_size)
        )
        self.glow = pg.transform.scale(Spinner.glow_img, (glow_size, glow_size))
        self.middle = pg.transform.scale(Spinner.middle_img, (middle_size, middle_size))
        self.middle2 = pg.transform.scale(
            Spinner.middle2_img, (middle2_size, middle2_size)
        )
        self.appr_circle = pg.transform.scale(
            Spinner.appr_circle_img, (self.appr_size, self.appr_size)
        )
        self.spin = pg.transform.scale(Spinner.spin_img, spin_size)
        self.clear = pg.transform.scale(Spinner.clear_img, clear_size)

        self.x, self.y = location[0], location[1]

        self.sps = {}
        for part in [self.bottom, self.top, self.middle, self.middle2, self.glow]:
            diff = part.get_size()[0] / 2
            self.sps[part] = (self.x - diff, self.y - diff)

        self.rect = self.top.get_rect()
        self.rect.left, self.rect.top = self.sps[self.top]

        self.sound_types = sound_types

        self.score = None

        self.velocity_r_middle = 255 / (end_time - appear_time)

        self.fade_pms = 255 / (fade_in_time - appear_time)
        self.shrink_pms = (appr_size - bottom_top_size) / (fade_in_time - appear_time)

        self.adding_bonus_points = False

        self.touching = False

        self.spin_coeff0 = 0.2 * self.spin.get_size()[0] / (fade_in_time - appear_time)
        self.spin_coeff1 = 0.2 * self.spin.get_size()[1] / (fade_in_time - appear_time)
        self.spin_fade_pms = 255 / (fade_in_time - appear_time)

        self.clear_coeff0 = 0.2 * self.clear.get_size()[0] / 400
        self.clear_coeff1 = 0.2 * self.clear.get_size()[1] / 400
        self.clear_fade_pms = 255 / 400

        self.last_coords = (0, 0)
        self.angle_mouse = 0
        self.angle_circle = 0

        self.drawing_clear = False
        self.hit_size = hit_size

        self.rnr = 40
        # TODO: calculate required number of rotations

    def draw(self, screen: pg.Surface, time: int):
        """Controls drawing processes"""
        if not (time > self.endtime - 400):
            if self.fade_in_time >= time:
                for part in self.sps:
                    part.set_alpha((time - self.appear_time) * self.fade_pms)

            self.draw_glow(screen, time)
            self.draw_bottom(screen, time)
            self.draw_top(screen, time)
            self.draw_middle2(screen, time)
            self.draw_middle(screen, time)

            if self.fade_in_time > time:
                self.draw_spin(screen, time)
            
            if (self.angle_circle / 360) / self.rnr >= 1:
                self.score = score_300_img
                self.draw_score(screen, time)
                self.drawing_clear = True

            return True

        else:
            if self.drawing_clear:
                self.draw_clear(screen, time)
            else:
                self.get_score()
                self.draw_score(screen, time)
        
        if self.touching:
            self.angle_change()
        
    def draw_glow(self, screen: pg.Surface, time: int):
        """Draws glow"""
        glow = self.glow.copy()

        if not self.adding_bonus_points:
            glow.fill((135, 206, 250), special_flags=3)

        screen.blit(glow, self.sps[self.glow])

    def draw_bottom(self, screen: pg.Surface, time: int):
        """Draw bottom"""
        screen.blit(self.bottom, self.sps[self.bottom])

    def draw_top(self, screen: pg.Surface, time: int):
        """Draws top"""
        screen.blit(self.top, self.sps[self.top])

    def draw_middle2(self, screen: pg.Surface, time: int):
        """Draws middle2"""
        screen.blit(self.middle2, self.sps[self.middle2])

    def draw_middle(self, screen: pg.Surface, time: int):
        """Draws middle"""
        middle = self.middle.copy()

        c = round(255 - self.velocity_r_middle * (time - self.appear_time))
        if c < 0:
            c = 0
        middle.fill((255, c, c), special_flags=3)

        screen.blit(middle, self.sps[self.middle])

    def draw_appr_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle from current time"""
        appr_circle = self.appr_circle.copy()

        if self.fade_in_time >= time >= self.appear_time:
            new_size = self.appr_size - (time - self.appear_time) * self.shrink_pms
            screen.blit(
                pg.transform.scale(appr_circle, (new_size, new_size)),
                (self.x - new_size / 2, self.y - new_size / 2),
            )
        else:
            screen.blit(
                pg.transform.scale(appr_circle, (self.bt_size, self.bt_size)),
                (self.x - self.bt_size / 2, self.y - self.bt_size / 2),
            )

    def draw_spin(self, screen: pg.Surface, time: int):
        """Draws spin"""
        spin = self.spin.copy()
        new_size0 = (
            self.spin.get_size()[0] + (self.fade_in_time - time) * self.spin_coeff0
        )
        new_size1 = (
            self.spin.get_size()[1] + (self.fade_in_time - time) * self.spin_coeff1
        )

        spin.set_alpha(self.spin_fade_pms * (time - self.appear_time))
        spin = pg.transform.scale(spin, (new_size0, new_size1))

        diff = spin.get_size()[0] / 2

        screen.blit(spin, (self.x - diff, self.y + self.bt_size / 2 - diff))

    def draw_clear(self, screen: pg.Surface, time: int):
        """Draws clear"""
        clear = self.clear.copy()
        new_size0 = self.clear.get_size()[0] + (self.endtime - time) * self.clear_coeff0
        new_size1 = self.clear.get_size()[1] + (self.endtime - time) * self.clear_coeff1

        clear.set_alpha(self.clear_fade_pms * (self.endtime - time))
        clear = pg.transform.scale(clear, (new_size0, new_size1))

        diff = clear.get_size()[0] / 2

        screen.blit(clear, (self.x - diff, self.y - diff))
    
    def hit(self, time: int):
        """Controls hit events"""
        self.touching = True
    
    def angle_change(self):
        """Controls angle changes"""
        if self.last_coords != (0, 0):
            x1, y1 = self.last_coords
            x2, y2 = pg.mouse.get_pos()
            self.angle_mouse = atan2((x2 - x1), (y2 - y1))

        self.last_coords = pg.mouse.get_pos()

    def get_score(self):
        """Gets score (used in drawing score)"""
        n = round((self.angle_circle / 360) / self.rnr)
        if n == self.rnr - 1:
            self.score = score_100_img
        elif n >= self.rnr * 0.25:
            self.score = score_50_img
        else:
            self.score = miss_img
    
    def draw_score(self, screen: pg.Surface, time: int):
        """Draws score from current time"""
        w, h = self.score.get_size()
        scale = (self.hit_size / self.score.get_height()) / 2.3
        w *= scale
        h *= scale
        score = pg.transform.scale(self.score, (w, h))

        score.set_alpha(255 - (255 / 400) * (time - self.endtime + 400))

        screen.blit(
            score,
            (
                self.rect.left + round((self.rect.width / 2) - (w / 2)),
                self.rect.top + round((self.rect.height / 2) - (h / 2)),
            ),
        )


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
            self.draw_hit_circle(screen, time)
            self.draw_combo_value(screen, time)
            return True

        else:
            if not self.shortening:
                self.endtime = time + 400
                self.shortening = True
            self.draw_score(screen, time)

    def hit(self, time: int):
        """Controls hit events"""
        if abs(self.hit_time - time) <= self.hit_windows[0]:
            self.score = score_300_img
            return 300
        elif self.hit_windows[1] >= abs(self.hit_time - time):
            self.score = score_100_img
            return 100
        elif (
            self.hit_windows[2] >= abs(self.hit_time - time)
            or -100 < self.hit_time - time < 0
        ):
            self.score = score_50_img
            return 50
        else:
            if self.hit_time - time < 0:
                self.score = miss_img
                return 0
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
        w, h = self.score.get_size()
        scale = (self.hit_size / self.score.get_height()) / 2.3
        w *= scale
        h *= scale
        score = pg.transform.scale(self.score, (w, h))

        score.set_alpha(255 - (255 / 400) * (time - self.endtime + 400))

        screen.blit(
            score,
            (
                self.rect.left + round((self.rect.width / 2) - (w / 2)),
                self.rect.top + round((self.rect.height / 2) - (h / 2)),
            ),
        )

    def draw_combo_value(self, screen: pg.Surface, time: int):
        center = (self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2)
        scale = self.hit_size / 3.5 / combo_numbers["0"].get_height()
        full_width = 0
        for v in str(self.combo_value):
            full_width += combo_numbers[v].get_width()
        x = center[0] - (full_width / 2 * scale)
        y = center[1] - (combo_numbers["0"].get_height() / 2 * scale) + 1

        offset = 0
        if self.count_vibr != 0:
            if self.count_vibr % 2 == 0:
                offset = -3
            else:
                offset = 3

        for v in str(self.combo_value):
            img = pg.transform.scale(
                combo_numbers[v],
                (
                    combo_numbers[v].get_width() * scale,
                    combo_numbers[v].get_height() * scale,
                ),
            )
            img.set_alpha((time - self.appear_time) * self.fade_pms)
            screen.blit(
                img,
                (x - offset, y),
            )
            x += img.get_width() * scale


class Slider(Circle):
    hit_circle_img = None
    hit_circle_overlay_img = None
    appr_circle_img = None
    slider_ball_frames_img = None
    tick_point_img = None
    slider_track_override = None
    slider_follow_circle = None

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
        tick_points: t.List[t.Tuple[int, int, int]],
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
        body : Tuple[Tuple[int, int]]
            Coordinates of points in slider's body
        endtime : int
            Endtime of slider,
        slider_border : Tuple[int, int, int]
            Color of slider border
        tick_points : t.List[t.Tuple[int, int, int]]
            Tick points of slider
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

        self.rect.x, self.rect.y = body[0]
        self.combo_value = combo_value
        self.combo_color = combo_color

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

        self.tick_points = tick_points
        self.last_follow_point = 0
        self.count_passed_points = 0
        self.count_points = len(tick_points)

        self.drawing_score = False
        self.hit_callback = hit_callback

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
        self.slider_offset = (min_x + 1, min_y + 2)
        surface = pg.Surface([width, height], pg.SRCALPHA, 32)
        for point in self.body:
            pg.draw.circle(
                surface,
                self.slider_border,
                (
                    point[0] - min_x + self.hit_size / 2,
                    point[1] - min_y + self.hit_size / 2,
                ),
                round(self.hit_size / 2.17),
            )
        if self.slider_track_override:
            track_color = self.slider_track_override
        else:
            track_color = self.combo_color
        precision = 25
        for iter in range(precision):
            color_addition = min((20 / precision) * (iter * 1.5), 255)
            _color = (
                min(max(track_color[0] + color_addition, 0), 255),
                min(max(track_color[1] + color_addition, 0), 255),
                min(max(track_color[2] + color_addition, 0), 255),
                190,
            )
            _width = (precision - iter) * self.hit_size / precision
            for point in self.body:
                pg.draw.circle(
                    surface,
                    _color,
                    (
                        point[0] - min_x + self.hit_size / 2,
                        point[1] - min_y + self.hit_size / 2,
                    ),
                    round(_width / 2.45),
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
            self.draw_tick_points(screen, time)
        if self.drawing_score == True:
            self.draw_score(screen, time)
        elif time > self.hit_time or self.begin_touch:
            self.draw_tick_points(screen, time)
            self.draw_slider_ball(screen, time)
            if self.touching:
                for point in self.tick_points:
                    if abs(time - point[2]) <= 50:
                        self.hit_callback(10)
                        self.count_passed_points += 1
                        self.tick_points.remove(point)
                        self.last_follow_point = 10
                self.draw_follow_circle(screen, time)
        else:
            self.draw_hit_circle(screen, time)
            self.draw_combo_value(screen, time)
            return True

    def draw_tick_points(self, screen: pg.Surface, time: int):
        if self.tick_point_img == None:
            return
        offset = (
            self.tick_point_img.get_width() / 2,
            self.tick_point_img.get_height() / 2,
        )
        time_offset = 0
        for p in self.tick_points:
            if (
                min(
                    ((p[0] - self.body[-1][0]) ** 2 + (p[1] - self.body[-1][1]) ** 2)
                    ** 0.5,
                    ((p[0] - self.body[0][0]) ** 2 + (p[1] - self.body[0][1]) ** 2)
                    ** 0.5,
                )
                > 35
            ):
                self.tick_point_img.set_alpha(
                    (time - (self.appear_time + time_offset)) * self.fade_pms / 1.3
                )
                time_offset += 300
                screen.blit(
                    self.tick_point_img,
                    (
                        (p[0] - offset[0]) + self.hit_size / 2,
                        (p[1] - offset[1]) + self.hit_size / 2,
                    ),
                )

    def hit(self, time: int):
        """Controls hit events"""
        self.last_follow_point = 10
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

            point_1 = self.body[ind]
            point_2 = self.body[min(ind + 1, len(self.body) - 1)]
            angle = degrees(atan2(point_2[1] - point_1[1], point_2[0] - point_1[0]))

            frame = self.slider_ball_frames[
                (self.slider_ball_frame // 2) % len(self.slider_ball_frames)
            ]
            rotated_frame = pg.transform.rotate(frame, -angle)
            offset = (
                (rotated_frame.get_width() - frame.get_width()) // 2
                - (self.hit_size - self.hit_size / 1.17) / 2,
                (rotated_frame.get_height() - frame.get_height()) // 2
                - (self.hit_size - self.hit_size / 1.17) / 2,
            )
            screen.blit(rotated_frame, (x - offset[0], y - offset[1]))
            self.slider_ball_frame += 1

            if self.current_point_index == 99:
                self.get_score()
                self.drawing_score = True
                self.endtime += 400

    def draw_follow_circle(self, screen: pg.Surface, time: int):
        """Draws approach circle on slider"""
        if self.last_follow_point > 0:
            coeff = 1 + (self.last_follow_point) / 100
            self.last_follow_point -= 1
        else:
            coeff = 1

        new_size = self.appr_size * coeff
        size_diff = (new_size - self.hit_size) / 2
        screen.blit(
            pg.transform.scale(
                self.slider_follow_circle, (new_size, new_size)
            ).convert_alpha(),
            (self.rect.x - size_diff, self.rect.y - size_diff),
        )

    def get_score(self):
        """Gets score (used in drawing score)"""
        try:
            n = self.count_passed_points / self.count_points
        except ZeroDivisionError:
            n = 0
        if n >= 0.9:
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
