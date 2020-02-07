from LyricsMaker import LyricsMaker
from mutagen import flac
from os import path
import asyncio
from FileIter import FileIter, LockedIterator

import logging


worker_amount = 5
token = 'slcoSGPx2vPljso3yHWwGB2uNzQ1rpV9dGqHYzSpWuOlaWXsqYeC1v9IaQvZ3Sta'
music_folder = r"D:\test"
singles_folder = path.join(music_folder, 'Singles')
albums_folder = path.join(music_folder, 'Albums')
done_file = 'done.json'

logging.basicConfig(format='[%(asctime)s] %(filename)s     %(message)s', level=logging.INFO)


if __name__ == '__main__':


    iterator = LockedIterator(FileIter(music_folder, done_file))
    workers = []

    for i in range(worker_amount):
        name = f"Lyrics Maker #{i}"
        maker = LyricsMaker(token, iterator, done_file, name)
        workers.append(maker)

    for worker in workers:
        worker.start()


    while True:
        stopped = True
        for worker in workers:
            stopped = stopped and not worker.is_alive()

        if stopped:
            break

    logging.info(f"done!")
    print(f"I AM DONE!!!")
