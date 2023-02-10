import pygame as pg
import typing as t

cursor_img = pg.image.load("./skin/cursor.png").convert_alpha()
trail_img = pg.image.load("./skin/cursortrail.png").convert_alpha()


class Cursor:
    """
    osu!python cursor class
    """

    def __init__(self, scale) -> None:
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
        self.trail = []

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
                self.trail.append([*pos, 25])
        else:
            self.trail.append([*pos, 25])
        for t in self.trail:
            trail = self.trail_img.copy()
            trail.set_alpha(t[2] * 6)
            screen.blit(
                trail, (t[0] - self.trail_sizes[0] / 2, t[1] - self.trail_sizes[1] / 2)
            )
        screen.blit(
            self.cursor_img, (pos[0] - self.sizes[0] / 2, pos[1] - self.sizes[1] / 2)
        )

    def set_cursor_scale(self, float):
        pass
