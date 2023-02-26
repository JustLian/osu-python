import json
import os
from osu_python.utils import parse_ini
from logging import getLogger


log = getLogger('config')


class Config:
    """
    osu!python config class
    use Config.obj object to access config
    """

    base_path = "/osu-python"
    cfg = {}
    skin_ini = {}
    path_sep = "/" if os.name == "posix" else "\\"
    default = {
        "songs-folders": [
            os.path.abspath("{}/songs".format(base_path))
        ],
        "keys": {"key1": 120, "key2": 122},
        "skin": "default",
        "fps": 60,
        "mouse_buttons": True,
        "bg_dim": 0.8
    }

    @classmethod
    def init(cls):
        """Method for initializing config"""
        cls.check_cfg()
        cls.load()

        if not os.path.isdir("{}/songs".format(Config.base_path)):
            os.mkdir("{}/songs".format(Config.base_path))
        if not os.path.isdir("{}/db".format(Config.base_path)):
            os.mkdir("{}/db".format(Config.base_path))
        if not os.path.isdir("{}/logs".format(Config.base_path)):
            os.mkdir("{}/logs".format(Config.base_path))
        if not os.path.isdir("{}/skins".format(Config.base_path)):
            os.mkdir("{}/skins".format(Config.base_path))

    @classmethod
    def check_cfg(cls):
        if not os.path.isdir(cls.base_path):
            os.mkdir(cls.base_path)

        if not os.path.isfile("{}/config.json".format(cls.base_path)):
            log.info('Creating configuration file')
            with open(
                "{}/config.json".format(cls.base_path), "w", encoding="utf8"
            ) as f:
                json.dump(cls.default, f)
        

    @classmethod
    def load(cls):
        """Load configuration file to Config.obj"""
        cls.check_cfg()
        with open("{}/config.json".format(Config.base_path), "r", encoding="utf8") as f:
            cls.cfg = json.load(f)
        
        # check for unset keys
        for key in cls.default.keys():
            if key not in cls.cfg:
                log.warning('Creating {} key in config.'.format(key))
                cls.cfg[key] = cls.default[key]
        cls.dump()

    @classmethod
    def dump(cls):
        """Dump configuration file from Config.obj"""
        cls.check_cfg()
        with open("{}/config.json".format(Config.base_path), "w", encoding="utf8") as f:
            json.dump(cls.cfg, f)

    @classmethod
    def load_skin_ini(cls):
        """Load skin configuration"""
        skin_path = Config.base_path + "/skins/" + Config.cfg["skin"]
        cls.skin_ini = parse_ini(skin_path + "/skin.ini")
