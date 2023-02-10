import pygame as pg
from osu_python.classes import Library, Config, game_object
from osu_python import map_loader
from threading import Thread
import os
from logging import getLogger
import requests, zipfile, io


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

        r = requests.get("https://files.catbox.moe/jnqebl.zip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        log.info("Extracting default skin")
        z.extractall(Config.base_path + "/skins/default")
        z.close()
        log.info("Default skin downloaded")

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

    # Done
    phase = 3


def setup(_height, _width, _screen, _next_scene):
    global success_screen, height, width, screen, next_scene
    height = _height
    width = _width
    screen = _screen
    next_scene = _next_scene

    success_screen = 0
    Thread(target=init_thread).start()


def tick(dt: float, events):
    global success_screen

    if phase != 3:
        screen.fill((119, 3, 252))
    else:
        success_screen += dt
        screen.fill((221, 133, 230))
        if success_screen > 1000:
            next_scene()
