from threading import Thread
from FileIter import LockedIterator
from TrackRefresher import TrackRefresher
import time
from os import path

import json
import logging


class LyricsMaker(Thread):

    def __init__(self, token: str, file_gen: LockedIterator, done_file: str, name: str = 'Lyrics Maker'):
        super().__init__(name=name)

        self.file_gen = file_gen
        self.refresher = TrackRefresher(token)

        self.done = list()
        self.done_file_path = done_file


    def run(self):

        print(f"STARTED {self.name}")

        for folder, file in self.file_gen:
            track = path.join(folder, file)

            res = self.refresher.track_refresh(track)
            if res:
                self.done.append(track)

        while True:
            try:
                with open(self.done_file_path) as file:
                    json.dump(self.done, file)
                    break

            except:
                time.sleep(2)

        logging.info(f"{self.name} is done")
        self.join()
