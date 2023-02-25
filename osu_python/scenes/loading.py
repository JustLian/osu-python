from osu_python.classes import Library, Config, game_object
from threading import Thread
import os
from logging import getLogger
import requests, zipfile, io
from osu_python import map_loader
from osu_python import scenes
import pygame as pg


log = getLogger("scenes/loading")


def init_thread():
    global phase

    # Library initialization
    phase = 0
    Library.update()

    # Game files checking
    if not os.path.isdir(Config.base_path + "/skins/default"):
        # Downloading default skin
        phase = 1
        log.info("Downloading default skin")

        os.mkdir(Config.base_path + "/skins/default")

        try:
            r = requests.get("https://files.catbox.moe/jnqebl.zip")
        except requests.exceptions.ConnectionError:
            log.warn("Internet connection error. Check your internet connection")
            return init_thread()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        log.info("Extracting default skin")
        z.extractall(Config.base_path + "/skins/default")
        z.close()
        log.info("Default skin downloaded")

    phase = 4
    game_object.load_skin()

    if len(os.listdir(Config.base_path + "/songs")) == 0:
        # Downloading Hikari E
        phase = 2
        log.info("Downloading default beatmapset")

        r = requests.get("https://files.catbox.moe/lec8ap.zip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        log.info("Extracting default beatmapset")
        z.extractall(Config.base_path + "/loading_temp")
        z.close()
        log.info("Adding map to library")

        from glob import glob

        mp = glob(Config.base_path + "/loading_temp/*")[0]
        map_loader.unpack(mp)

        os.remove(mp)
        os.rmdir(Config.base_path + "/loading_temp")

        Library.update()
    
    if os.path.isdir(Config.base_path + '/bmi'):
        arr = os.listdir(Config.base_path + '/bmi')
        if arr == []:
            os.remove(Config.base_path + '/bmi')
        else:
            phase = 5
            log.info("Unpacking beatmapsets pack")
            
            for f in arr:
                log.info('Extracting {}'.format(f))
                z = zipfile.ZipFile(Config.base_path + '/bmi/' + f)
                z.extractall(Config.base_path + '/songs')
                z.close()
            
            log.info("Beatmapsets pack extracted. Updating library")
            Library.update()

    # Done
    phase = 3


def setup(_height, _width, _screen, _next_scene):
    global success_screen, height, width, screen, next_scene, phases
    height = _height
    width = _width
    screen = _screen
    next_scene = _next_scene

    font = pg.font.Font("./ui/aller_bold.ttf", round(height * 0.1))

    phases = [
        font.render("Updating library", True, (255, 255, 255)),
        font.render("Downloading default skin", True, (255, 255, 255)),
        font.render("Downloading default beatmapset", True, (255, 255, 255)),
        font.render("Loading...", True, (255, 255, 255)),
        font.render("Loading skin", True, (255, 255, 255)),
        font.render("Unpacking beatmapsets", True, (255, 255, 255))
    ]

    success_screen = 0
    Thread(target=init_thread).start()


def tick(dt: float, events):
    global success_screen

    screen.fill((0, 0, 0))
    screen.blit(
        phases[phase],
        (
            (width - phases[phase].get_width()) // 2,
            (height - phases[phase].get_height()) // 2,
        ),
    )

    if phase == 3:
        success_screen += dt
        if success_screen >= 1000:
            next_scene(scenes.main_menu, next_scene)
