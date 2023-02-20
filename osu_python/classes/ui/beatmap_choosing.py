import pygame as pg
from osu_python.classes.ui import root
from osu_python.classes import Library, Config


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
    
    def draw(self, y_pos: int, screen: pg.Surface, dt: float):
        img_pos = (screen.get_width() - self.width, y_pos - self.height // 2)
        screen.blit(
            self.img, img_pos
        )
        screen.blit(
            self.line_1,
            (
                img_pos[0] + self.width * .015,
                img_pos[1] + self.height * .01 + self.const
            )
        )
        screen.blit(
            self.line_2,
            (
                img_pos[0] + self.width * .015,
                img_pos[1] + self.height * .02 + self.line_1.get_height() + self.const
            )
        )