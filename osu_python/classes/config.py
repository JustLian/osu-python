import json
import os
from osu_python.utils import parse_ini


class Config:
    """
    osu!python config class
    use Config.obj object to access config

    ```json
    'songs-folders': [
        'list of abs paths to songs folders'
    ],
    'keys': {
        'key1': 1st keyboard key,
        'key2': 2nd keyboard key
    }
    ```
    """

    base_path = "/osu-python"
    cfg = {}
    skin_ini = {}
    path_sep = '/' if os.name == 'posix' else '\\'

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
            with open(
                "{}/config.json".format(cls.base_path), "w", encoding="utf8"
            ) as f:
                json.dump(
                    {
                        "songs-folders": [
                            os.path.abspath("{}/songs".format(cls.base_path))
                        ],
                        "keys": {"key1": 120, "key2": 122},
                        "skin": "default",
                        "fps": 60,
                        "mouse_buttons": True
                    },
                    f,
                )

    @classmethod
    def load(cls):
        """Load configuration file to Config.obj"""
        cls.check_cfg()
        with open("{}/config.json".format(Config.base_path), "r", encoding="utf8") as f:
            cls.cfg = json.load(f)

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
