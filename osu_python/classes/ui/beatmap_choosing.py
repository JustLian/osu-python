import pygame as pg
from osu_python.classes.ui import root
from osu_python.classes import Library, Config
from osu_python import utils, map_loader


def load_skin():
    global BeatmapSetCard

    path = Config.base_path + "/skins/" + Config.cfg["skin"]
    BeatmapSetCard.bg = pg.image.load(path + "/menu-button-background.png").convert_alpha()


class BeatmapSetCard(root.UiElement):
    bg = None

    def __init__(
        self,
        index: int,
        card_height: int,
        font: pg.font.Font,
        const: float
    ):
        self.index = index
        self.data = Library.db.get(doc_id=index)
        self.height = card_height
        self.font = font
        self.const = const

        size = BeatmapSetCard.bg.get_size()
        self.width = round(card_height * size[0] / size[1])
        self.img = pg.transform.scale(
            BeatmapSetCard.bg,
            (self.width, self.height)
        )

        self.thumbnail_width = self.height * 1.6
        bg = map_loader.get_background(
            Library.path_for_diff(self.data, 0)
        ).convert()
        h = self.height * 0.8537864078
        w = h * bg.get_width() / bg.get_height()
        self.thumbnail = pg.transform.scale(
            bg, (h * bg.get_width() / bg.get_height(), h)
        )

        if w > self.height * 1.5:
            crop = (w - self.height * 1.5) // 2
            self.thumbnail = self.thumbnail.subsurface(
                pg.Rect(
                    crop, 0, 
                    self.height * 1.5 - crop, h
                )
            )

        # self.thumbnail_offset = w // 2 - ts // 2
        self.thumbnail_offset = (self.height * 1.5 - w) // 2 + self.width * .005

        line_1 = self.font.render(
            self.data['title'],
            True, (0, 0, 0)
        )
        line_2 = self.font.render("{} // {}".format(
            self.data['diffs'][0]['artist'],
            self.data['creator']
        ), True, (0, 0, 0))

        self.line_1 = pg.transform.scale(
            line_1, (line_1.get_width() * (self.height * .26766784452 / line_1.get_height()), self.height * .26766784452)
        )
        self.line_2 = pg.transform.scale(
            line_2, (line_2.get_width() * (self.height * .16766784452 / line_2.get_height()), self.height * .16766784452)
        )
    
    def draw(self, y_pos: int, screen: pg.Surface, dt: float, scroll):
        img_pos = (screen.get_width() - self.width + scroll[0], y_pos - self.height // 2 + scroll[1])
        screen.blit(
            self.img, img_pos
        )
        screen.blit(
            self.line_1,
            (
                img_pos[0] + self.width * .015 + self.thumbnail_width,
                img_pos[1] + self.height * .01 + self.const
            )
        )
        screen.blit(
            self.line_2,
            (
                img_pos[0] + self.width * .015 + self.thumbnail_width,
                img_pos[1] + self.height * .02 + self.line_1.get_height() + self.const
            )
        )
        screen.blit(
            self.thumbnail, (
                img_pos[0] + self.thumbnail_offset,
                img_pos[1] + self.height * 0.06796116505
            )
        )
