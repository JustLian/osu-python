import os
import slider
from osu_python.classes import Config
from tinydb import TinyDB
from glob import glob


Config.init()


class Library:
    """
    Class for interacting with local songs library
    """

    db = TinyDB('{}/db/lib.json'.format(Config.base_path))
    update_progress = 0
    update_total = 0

    @classmethod
    def update(cls):
        """
        Method for updating library database.

        Should be called after new maps installation
        and game start
        """

        def broken_bms(bid):
            cls.db.insert({'id': bid, 'broken': 1})

        existing_ids = [
            b['id'] for b in cls.db
        ]
        Config.load()
        for folder in Config.cfg['songs-folders']:
            bms_paths = glob(folder + '/*')
            cls.update_total += len(bms_paths)
            for bms_path in bms_paths:
                cls.update_progress += 1
                # Skipping files
                if not os.path.isdir(bms_path):
                    continue
                
                # Beatmap set id verification
                bms_id = bms_path.replace('\\', '/').split('/')[-1].split()[0]

                try:
                    bms_id = int(bms_id)
                except:
                    continue

                if bms_id in existing_ids:
                    continue

                # Saving beatmapset info
                diffs = []

                bm_paths = [bms_path + '/' + x for x in os.listdir(bms_path) if x.endswith('.osu')]
                if bm_paths == []:
                    broken_bms(bms_id)
                    continue
                last = bm_paths[-1]
                skip = False
                for bm_path in bm_paths:
                    try:
                        bm = slider.Beatmap.from_path(bm_path)
                    except Exception as e:
                        print('Unexpected error ocurred: {}. Skipping beatmap set'.format(e))
                        broken_bms(bms_id)
                        skip = True
                        break
                    try:
                        diffs.append({
                            'id': bm.beatmap_id,
                            'stars': bm.stars(),
                            'version': bm.version,
                            'artist': bm.artist
                        })
                    except Exception as e:
                        print('Unexpected error ocurred: {}. Skipping beatmap set'.format(e))
                        broken_bms(bms_id)
                        skip = True
                if skip:
                    continue
                
                bm = slider.Beatmap.from_path(last)
                cls.db.insert({
                    'id': bm.beatmap_set_id,
                    'title': bm.title,
                    'creator': bm.creator,
                    "diffs": diffs
                })
    
    @classmethod
    def search(cls, query: str) -> list:
        """
        This method lets you search library.
        Fields that will be tested:
          * Beatmap set's title and creator
          * Difficulty's version
          * Difficulty's artist

        Parameters
        ----------
        query : str
            Search query
        
        Returns
        -------
        List of beatmap sets data from db
        """
        result = []
        for s in cls.db:
            if 'broken' not in s and (
                # Check beatmaps set's title and creator
                query in s['title'].lower()
                or
                query in s['creator'].lower()
                or
                # Check all of difficulties
                any([(
                        query in d['version'].lower()
                        or
                        query in d['artist'].lower()
                    ) for d in s['diffs']
                ])
            ):
                result.append(s)
        
        return result