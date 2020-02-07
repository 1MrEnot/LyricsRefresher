import json
import os
import threading


class LockedIterator:
    def __init__(self, it):
        self.lock = threading.Lock()
        self.it = it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        self.lock.acquire()
        try:
            return self.it.__next__()
        finally:
            self.lock.release()


class FileIter:

    def __init__(self, folder: str, done_path: str):

        with open(done_path, encoding='utf-8') as done_file:
            self.done = set(json.load(done_file))
        self.files = os.walk(folder)


    def __iter__(self):
        for folder, sub_folders, files in self.files:
            files = [file for file in files if file not in self.done]

            if len(files) == 0:
                continue

            for file in files:
                yield folder, file

