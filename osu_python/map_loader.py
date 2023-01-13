import slider
import os
from osu_python.classes import game_object
from osu_python import utils


def load_map(path: os.PathLike, v_scale, h_scale):
    mp = slider.Beatmap.from_path(path)
    preempt = utils.calculate_preemt(mp.ar())
    fade_in = utils.calculate_fade_in(mp.ar())
    hit_size = utils.calculate_hit_r(mp.cs())
    appr_size = utils.calculate_appr_r(mp.cs())
    
    queue = []
    for obj in mp.hit_objects():
        if isinstance(
            obj, slider.beatmap.Circle
        ):
            time = obj.time.total_seconds()
            queue.append(game_object.Circle(
                time, time - preempt, time - preempt + fade_in,
                (obj.position.x * h_scale, obj.position.y * v_scale),
                False, (), hit_size, appr_size
            ))
    return queue