import slider
import os
from osu_python.classes import game_object
from osu_python import utils


def load_map(path: os.PathLike, scale, add_x, add_y):
    mp = slider.Beatmap.from_path(path)
    preempt = utils.calculate_preemt(mp.ar())
    fade_in = utils.calculate_fade_in(mp.ar())
    hit_size = utils.calculate_hit_r(mp.cs()) * scale
    appr_size = utils.calculate_appr_r(mp.cs()) * scale
    hit_windows = utils.calculate_hit_windows(mp.od())

    queue = []
    for obj in mp.hit_objects():
        if isinstance(obj, slider.beatmap.Circle):
            time = obj.time.total_seconds() * 1000
            queue.append(
                game_object.Circle(
                    time,
                    time - preempt,
                    time - preempt + fade_in,
                    (add_x + obj.position.x * scale, add_y + obj.position.y * scale),
                    False,
                    (),
                    hit_size,
                    appr_size,
                    hit_windows,
                )
            )

        if isinstance(obj, slider.beatmap.Slider):
            time = obj.time.total_seconds() * 1000

            body = []
            for n in range(100):
                c = obj.curve(n / 100)
                body.append((add_x + c.x * scale, add_y + c.y * scale))

            queue.append(
                game_object.Slider(
                    time,
                    time - preempt,
                    time - preempt + fade_in,
                    (add_x + obj.position.x * scale, add_y + obj.position.y * scale),
                    False,
                    (),
                    hit_size,
                    appr_size,
                    hit_windows,
                    body,
                )
            )
    return queue
