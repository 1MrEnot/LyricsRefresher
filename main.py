from LyricsMaker import LyricsMaker
from mutagen import flac
from os import path
import asyncio
from FileIter import FileIter, LockedIterator
import json

import logging


worker_amount = 10
token = 'slcoSGPx2vPljso3yHWwGB2uNzQ1rpV9dGqHYzSpWuOlaWXsqYeC1v9IaQvZ3Sta'
config = 'config.json'
default_config_data = '{"done": []}'

music_folder = r"D:\Music"
singles_folder = path.join(music_folder, 'Singles')
albums_folder = path.join(music_folder, 'Albums')

logging.basicConfig(format='[%(asctime)s] %(filename)s     %(message)s', level=logging.INFO)



if __name__ == '__main__':

    if not path.exists(config):
        with open(config, 'w', encoding='utf-8') as file:
            file.write(default_config_data)

    with open(config, encoding='utf-8') as file:
        data = json.load(file)

    iterator = LockedIterator(FileIter(albums_folder, data['done']))
    workers = []

    for i in range(worker_amount):
        maker = LyricsMaker(token, iterator, f"Lyrics Maker #{i}")
        workers.append(maker)

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

    for worker in workers:
        data['done'].extend(worker.done)

    with open(config, 'w', encoding='utf-8') as file:
        json.dump(data, file)

    logging.info(f"done!")
