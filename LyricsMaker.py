from threading import Thread
from FileIter import LockedIterator
from TrackRefresher import TrackRefresher
from os import path
import logging


class LyricsMaker(Thread):

    def __init__(self, token: str, file_gen: LockedIterator, name: str = 'Lyrics Maker'):
        super().__init__(name=name)

        self.file_gen = file_gen
        self.refresher = TrackRefresher(token)

        self.done = list()


    def run(self):
        for folder, file in self.file_gen:
            track = path.join(folder, file)

            res = self.refresher.track_refresh(track)
            if res:
                self.done.append(track)

        logging.info(f"{self.name} is done!")
