import pygame as pg
from osu_python.classes.ui import root
from osu_python.classes import Library, Config
from osu_python import map_loader, scenes
import typing as t
from random import randint


def load_skin():
    global BeatmapSetCard, DifficultyCard

    path = Config.base_path + "/skins/" + Config.cfg["skin"]
    BeatmapSetCard.bg = pg.image.load(
        path + "/menu-button-background.png"
    ).convert_alpha()


class BeatmapSetCard(root.UiElement):
    bg = None

    def __init__(self, index: int, card_height: int, font: pg.font.Font, const: float):
        self.index = index
        self.data = Library.db.get(doc_id=index)
        self.height = card_height
        self.font = font
        self.const = const

        size = BeatmapSetCard.bg.get_size()
        self.width = round(card_height * size[0] / size[1])
        self.img = pg.transform.scale(BeatmapSetCard.bg, (self.width, self.height))
        self.rect = self.img.get_rect()

        self.thumbnail_width = self.height * 1.6
        bg = map_loader.get_background(Library.path_for_diff(self.data, 0)).convert()
        h = self.height * 0.8537864078
        w = h * bg.get_width() / bg.get_height()
        self.thumbnail = pg.transform.scale(
            bg, (h * bg.get_width() / bg.get_height(), h)
        )

        if w > self.height * 1.5:
            crop = (w - self.height * 1.5) // 2
            self.thumbnail = self.thumbnail.subsurface(
                pg.Rect(crop, 0, self.height * 1.5 - crop, h)
            )

        self.thumbnail_offset = (self.height * 1.5 - w) // 2 + self.width * 0.005

        line_1 = self.font.render(self.data["title"], True, (0, 0, 0))
        line_2 = self.font.render(
            "{} // {}".format(self.data["diffs"][0]["artist"], self.data["creator"]),
            True,
            (0, 0, 0),
        )

        self.line_1 = pg.transform.scale(
            line_1,
            (
                line_1.get_width()
                * (self.height * 0.26766784452 / line_1.get_height()),
                self.height * 0.26766784452,
            ),
        )
        self.line_2 = pg.transform.scale(
            line_2,
            (
                line_2.get_width()
                * (self.height * 0.16766784452 / line_2.get_height()),
                self.height * 0.16766784452,
            ),
        )

    def draw(self, y_pos: int, screen: pg.Surface, dt: float, scroll):
        """
        Returns
        -------
        None: object is on screen
        False: object above screen
        True: object below screen
        """

        img_pos = (
            screen.get_width() - self.width + scroll[0],
            y_pos - self.height // 2 + scroll[1],
        )
        self.rect.x, self.rect.y = img_pos
        s_h = screen.get_height()
        if img_pos[1] > s_h or 0 > (img_pos[1] + self.height):
            return img_pos[1] > s_h

        screen.blit(self.img, img_pos)
        screen.blit(
            self.line_1,
            (
                img_pos[0] + self.width * 0.015 + self.thumbnail_width,
                img_pos[1] + self.height * 0.01 + self.const,
            ),
        )
        screen.blit(
            self.line_2,
            (
                img_pos[0] + self.width * 0.015 + self.thumbnail_width,
                img_pos[1] + self.height * 0.02 + self.line_1.get_height() + self.const,
            ),
        )
        screen.blit(
            self.thumbnail,
            (
                img_pos[0] + self.thumbnail_offset,
                img_pos[1] + self.height * 0.06796116505,
            ),
        )

    def is_colliding(self, pos) -> bool:
        return self.rect.collidepoint(*pos)


class DifficultyCard(root.UiElement):
    def __init__(
        self,
        version: str,
        stars: int,
        func: t.Callable,
        font: pg.font.Font,
        img: pg.Surface,
        dest: t.Tuple[int, int],
        mgr,
    ):
        self.click = func
        self.img = img
        self.mgr = mgr

        h = self.img.get_height()

        hc = h // 3

        line1 = font.render(version, True, (0, 0, 0))
        line1 = pg.transform.scale(
            line1, (hc * line1.get_width() / line1.get_height(), hc)
        )

        line2 = font.render("{} stars".format(round(stars, 2)), True, (0, 0, 0))
        line2 = pg.transform.scale(
            line2, (hc * line2.get_width() / line2.get_height(), hc)
        )

        offset = self.img.get_height() * 0.1
        self.img.blit(line1, (offset, offset))

        self.rect = img.get_rect()
        self.rect.x, self.rect.y = dest

        self.img.blit(line2, (offset, offset + line1.get_height()))

        self.dest = dest

        super().__init__()

    def draw(self, screen: pg.Surface, _):
        screen.blit(
            self.img, (self.dest[0] + self.mgr.x_offset, self.dest[1] + self.mgr.scroll)
        )

    def is_colliding(self, pos) -> bool:
        return self.rect.collidepoint(pos)


class DifficultyManager:
    def __init__(
        self, height: int, func: t.Callable, font: pg.font.Font, mgr: root.UiManager
    ):
        size = BeatmapSetCard.bg.get_size()
        self.height = height
        self.h = height // 8
        self.w = round(self.h * size[0] / size[1])
        self.offset = height * 0.05
        self.el_offset = height * 0.05
        self.img = pg.transform.scale(BeatmapSetCard.bg, (self.w, self.h))
        self.font = font
        self.func = func
        self.mgr = mgr

        self.x_offset_animation = lambda _: [0]

        self.max_scroll = 0

        self.scroll = 0

        self.elements = []

    def update(self, data: dict):
        self.scroll = 0
        self.x_offset = -self.el_offset - self.w * 1.25
        self.x_offset_animation = root.Animation(
            300, (self.x_offset,), (0,), "CubicEaseOut"
        )
        for e in self.elements:
            self.mgr.remove_obj(e)

        self.elements = []
        offset = 0
        bm = randint(1, len(Library.db))
        while "diffs" not in Library.db.get(doc_id=bm):
            bm = randint(1, len(Library.db))
        for d in range(len(data["diffs"])):

            def f(x=d):
                self.func(
                    scenes.std,
                    Library.path_for_diff(data, x),
                    lambda *args: self.func(scenes.std, *args),
                    lambda: self.func(scenes.beatmap_choosing, bm, 0, self.func),
                    lambda *args: self.func(scenes.ranking, *args),
                )

            offset += self.offset
            self.elements.append(
                DifficultyCard(
                    data["diffs"][d]["version"],
                    data["diffs"][d]["stars"],
                    f,
                    self.font,
                    self.img.copy(),
                    (self.el_offset, self.el_offset + offset),
                    self,
                )
            )
            offset += self.h

        m = len(self.elements) * (self.offset + self.h) - self.height
        if m > 0:
            self.max_scroll = -m - self.el_offset
        else:
            self.max_scroll = 0

        for e in self.elements:
            self.mgr.add_obj(e, 0)

    def update_scroll(self, y: float):
        if self.max_scroll <= self.scroll + y * 20 <= 0:
            self.scroll += y * 20

    def update_x_offset(self, dt: float):
        self.x_offset = self.x_offset_animation(dt)[0]
