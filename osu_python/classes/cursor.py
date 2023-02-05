import pygame as pg
import typing as t

cursor_img = pg.image.load("./skin/cursor.png")
trail_img = pg.image.load("./skin/cursortrail.png")

class Cursor:
    """
    osu!python cursor class
    """
    def __init__(self) -> None:
        self.sizes = cursor_img.get_rect()[2:]

        self.trail_sizes = trail_img.get_rect()[2:]
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
            dist = ((pos[0] - self.trail[-1][0])**2 + (pos[1] - self.trail[-1][1])**2)**0.5
            if dist > 10:
                self.trail.append([*pos, 25])
        else:
            self.trail.append([*pos, 25])
        for t in self.trail:
            trail = trail_img.copy()
            trail.set_alpha(t[2] * 6)
            screen.blit(
                trail, (t[0] - self.trail_sizes[0] / 2, t[1] - self.trail_sizes[1] / 2)
            )
        screen.blit(
            cursor_img, (pos[0] - self.sizes[0] / 2, pos[1] - self.sizes[1] / 2)
        )
