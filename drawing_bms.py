import random
import pygame as pg
from screeninfo import get_monitors
from tinydb import TinyDB
import typing as t


db = TinyDB("C:\\osu-python\\db\\lib.json")
pg.display.init()
for m in get_monitors():
    if m.is_primary:
        width, height = m.width, m.height
screen = pg.display.set_mode((width, height), flags=pg.FULLSCREEN | pg.DOUBLEBUF)


class BeatmapSetCard:
    bg = pg.image.load(
        "C:\\Users\\Иван\\AppData\\Local\\osu!\\Skins\\»multiberry«\\menu-button-background.png"
    ).convert_alpha()

    def __init__(
        self,
        index: int,
        card_height: int,
        font: pg.font.Font,
        const: float
    ):
        self.index = index
        self.data = db.get(doc_id=index)
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


def draw(screen: pg.Surface):
    screen.fill((0, 0, 0))

    lh = bms_card_height // 2
    for card in cards:
        card.draw(lh, screen, 0)
        lh += bms_card_height * 1.01

    pg.display.flip()


def main():
    global data, cards, bms_card_height
    pg.init()
    fps = 60
    clock = pg.time.Clock()


    data = []
    cards = []
    bms_card_height = height // 8
    height_constant = bms_card_height * 0.035
    font = pg.font.Font('./ui/aller_light.ttf', round(bms_card_height * .5))
    for _ in range(8):
        d = {'broken': 1}
        while 'broken' in d:
            index = random.randint(0, 999)
            d = db.get(doc_id=index)
        data.append(d)
        cards.append(
            BeatmapSetCard(
                index, bms_card_height, font,
                height_constant
            )
        )

    dt = 1 / fps
    while True:
        draw(screen)

        dt = clock.tick(fps)


main()