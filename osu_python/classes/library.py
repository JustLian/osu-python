import os
import slider
from osu_python.classes import Config
from osu_python import utils
from tinydb import TinyDB
from glob import glob
import logging
from pathvalidate import sanitize_filepath
from threading import Thread
from time import sleep


log = logging.getLogger("library")
Config.init()


class Library:
    """
    Class for interacting with local songs library
    """

    db = TinyDB("{}/db/lib.json".format(Config.base_path))
    update_progress = 0
    update_total = 0

    @classmethod
    def update(cls):
        """
        Method for updating library database.

        Should be called after new maps installation
        and game start
        """
        log.info("updating library")

        def broken_bms(bid, bms_path, results):
            results.append({"id": bid, "path": bms_path, "broken": 1})

        existing_paths = [b["path"] for b in cls.db]
        Config.load()
        bms_paths = []
        for folder in Config.cfg["songs-folders"]:
            bms_paths.extend(glob(folder + "/*"))

        if len(existing_paths) != 0:
            bms_paths = set(bms_paths).symmetric_difference(set(existing_paths))
        cls.update_total = len(bms_paths)
        log.info("found {} new beatmap sets".format(cls.update_total))

        results = []

        def update_thread(chunk: list, results: list, nthread: int) -> None:
            log.info("Library update Thread #{} started".format(nthread))
            for bms_path in chunk:
                cls.update_progress += 1
                # Skipping files
                if not os.path.isdir(bms_path):
                    continue

                # Beatmap set id verification
                bms_id = bms_path.replace("\\", "/").split("/")[-1].split()[0]

                try:
                    bms_id = int(bms_id)
                except ValueError:
                    broken_bms(None, bms_path, results)
                    continue

                # Saving beatmapset info
                diffs = []

                bm_paths = [
                    bms_path + "/" + x
                    for x in os.listdir(bms_path)
                    if x.endswith(".osu")
                ]
                if bm_paths == []:
                    broken_bms(bms_id, bms_path, results)
                    continue
                last = bm_paths[-1]
                skip = False
                for bm_path in bm_paths:
                    try:
                        bm = slider.Beatmap.from_path(bm_path)
                    except Exception as e:
                        log.error(
                            "Unexpected error ocurred: {}. Skipping beatmap set".format(
                                e
                            )
                        )
                        broken_bms(bms_id, bms_path, results)
                        skip = True
                        break
                    try:
                        diffs.append(
                            {
                                "id": bm.beatmap_id,
                                "stars": bm.stars(),
                                "version": bm.version,
                                "artist": bm.artist,
                            }
                        )
                    except Exception as e:
                        log.error(
                            "Unexpected error ocurred: {}. Skipping beatmap set".format(
                                e
                            )
                        )
                        broken_bms(bms_id, bms_path, results)
                        skip = True
                if skip:
                    continue

                bm = slider.Beatmap.from_path(last)
                results.append(
                    {
                        "id": bm.beatmap_set_id,
                        "title": bm.title,
                        "creator": bm.creator,
                        "diffs": diffs,
                        "path": bms_path,
                    }
                )
            log.info("Library update Thread #{} exited".format(nthread))

        if len(bms_paths) != 0:
            threads = []
            for nthread, paths_chunk in enumerate(utils.chunks(list(bms_paths), 3)):
                th = Thread(target=update_thread, args=(paths_chunk, results, nthread))
                threads.append(th)
                th.start()

            while any([th.is_alive() for th in threads]):
                sleep(1)

            log.info("All threads exited. Updating DB")

            cls.db.insert_multiple(results)

        log.info("library updated")

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

        def contains(q, s) -> bool:
            ss = "".join([x for x in s if x.isalnum()]).lower().split()
            sq = "".join([x for x in q if x.isalnum()]).lower().split()
            for p in sq:
                if p not in ss:
                    return False
            return True

        for s in cls.db:
            if "broken" not in s and (
                # Check beatmaps set's title and creator
                contains(query, s["title"])
                or contains(query, s["creator"])
                or
                # Check all of difficulties
                any(
                    [
                        (contains(query, d["version"]) or contains(query, d["artist"]))
                        for d in s["diffs"]
                    ]
                )
            ):
                result.append(s)

        return result

    @classmethod
    def path_for_diff(cls, mp: dict, diff_index: int) -> str:
        """
        Generates path to .osu file from library entry
        and difficulty's index

        Parameters
        ----------
        mp : dict
            Entry from Library
        diff_index : int
            Index of difficulty in mp['diffs']
        """
        diff = mp["diffs"][diff_index]
        diff_path = "{}\\{} - {} ({}) [{}].osu".format(
            mp["path"], diff["artist"], mp["title"], mp["creator"], diff["version"]
        )
        return sanitize_filepath(diff_path, platform="auto")
