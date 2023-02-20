import pygame as pg
from osu_python.classes import Config
from os.path import isdir


cursor_img = None
trail_img = None
cursor_middle_img = None


def load_skin():
    global cursor_img, trail_img, cursor_middle_img
    try:
        path = Config.base_path + "/skins/" + Config.cfg["skin"]
        # Fallback skin
        if not isdir(path):
            path = "./skin"
    except KeyError:
        path = "./skin"

    cursor_img = pg.image.load(path + "/cursor.png").convert_alpha()
    trail_img = pg.image.load(path + "/cursortrail.png").convert_alpha()
    try:
        cursor_middle_img = pg.image.load(path + "/cursormiddle.png").convert_alpha()
    except FileNotFoundError:
        pass

    try:
        Cursor.rotation = Config.skin_ini["[General]"]["CursorRotate"]
    except KeyError:
        pass


class Cursor:
    """
    osu!python cursor class
    """
    
    rotation = 0

    def __init__(self, scale) -> None:
        load_skin()

        self.sizes = (
            cursor_img.get_width() * scale,
            cursor_img.get_height() * scale,
        )
        self.cursor_img = pg.transform.scale(cursor_img, self.sizes)

        self.trail_sizes = (
            trail_img.get_width() * scale,
            trail_img.get_height() * scale,
        )
        self.trail_img = pg.transform.scale(trail_img, self.trail_sizes)

        self.cursor_middle_img = None
        if cursor_middle_img:
            self.cursor_middle_sizes = (
                cursor_middle_img.get_width() * scale,
                cursor_middle_img.get_height() * scale,
            )
            self.cursor_middle_img = pg.transform.scale(
                cursor_middle_img, self.cursor_middle_sizes
            )

        self.trail = []
        self.angle = 0

    def trail_tick(self):
        """Updates cursor trail"""
        for i, v in enumerate(self.trail):
            v[2] -= 1
            if v[2] <= 0:
                self.trail.pop(i)

    def draw(self, screen, pos):
        """Draws cursor and cursor trail on screen

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the cursor and cursor trail is getting drawn
        pos : Tuple[int, int]
            Position where cursor is drawn
        """
        self.trail_tick()
        if len(self.trail) > 0:
            dist = (
                (pos[0] - self.trail[-1][0]) ** 2 + (pos[1] - self.trail[-1][1]) ** 2
            ) ** 0.5
            if dist > 10:
                self.trail.append([*pos, 8])
        else:
            self.trail.append([*pos, 8])
        for t in self.trail:
            trail = self.trail_img.copy()
            trail.set_alpha(t[2] * 32)
            screen.blit(
                trail, (t[0] - self.trail_sizes[0] / 2, t[1] - self.trail_sizes[1] / 2)
            )

        if self.rotation:
            self.angle += 1
            rotated_frame = pg.transform.rotate(self.cursor_img, self.angle)
            offset = (
                (rotated_frame.get_width() - self.cursor_img.get_width()) // 2 + self.cursor_img.get_width() // 2,
                (rotated_frame.get_height() - self.cursor_img.get_height()) // 2 + self.cursor_img.get_height() // 2,
            )
            screen.blit(
                rotated_frame, (pos[0] - offset[0], pos[1] - offset[1])
            )
        else:
            screen.blit(
                self.cursor_img, (pos[0] - self.sizes[0] / 2, pos[1] - self.sizes[1] / 2)
            )

        if self.cursor_middle_img:
            screen.blit(
                self.cursor_middle_img,
                (
                    pos[0] - self.cursor_middle_sizes[0] / 2,
                    pos[1] - self.cursor_middle_sizes[1] / 2,
                ),
            )
