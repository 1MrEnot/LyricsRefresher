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

    def __init__(self, folder: str, done: list):
        self.done = done
        self.files = os.walk(folder)

    def __iter__(self):
        for folder, sub_folders, files in self.files:
            for file in files:
                if os.path.join(folder, file) not in self.done:
                    yield folder, file
