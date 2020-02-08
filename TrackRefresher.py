from os import path
import logging
import json
from mutagen import flac, mp3
from mutagen.id3 import ID3, USLT

from functools import lru_cache
import re

import lyricsgenius


def title_prettify(title):
    table = {'[': '(',
             ']': ')'}
    title = title.lower()

    if 'remix' in title:
        title = title[:title.rfind('(')]

    title = title.translate(table).strip()

    return title


class TrackRefresher:

    mp3 = '.mp3'
    flac = '.flac'

    def __init__(self, token: str):
        self.token = token
        self.api = lyricsgenius.Genius(token)

    @lru_cache()
    def get_lyrics(self, authors: str, title: str):
        song = self.api.search_song(title, authors)
        if song and song.lyrics:
            return song.lyrics
        return ''

    def flac_refresh(self, track_path: str) -> bool:

        try:
            audio = flac.FLAC(track_path)
            tag_dict = {}

            for key, value in audio.tags:
                tag_dict[key.lower()] = value

            artist, title = tag_dict['artist'], tag_dict['title']
            title = title_prettify(title)

            lyrics = self.get_lyrics(artist, title)
            if lyrics:
                audio.tags['Lyrics'] = lyrics
                audio.save()
            return True

        except Exception as e:
            logging.warning(f"EXCEPTION at {track_path}: {e}")
            return False


    def mp3_refresh(self, track_path: str) -> bool:

        try:
            audio = mp3.EasyMP3(track_path)
            tag_dict = {}

            for key in audio.tags:
                tag_dict[key] = audio.tags[key][0]

            artist, title = tag_dict['artist'], tag_dict['title']
            title = title_prettify(title)

            lyrics = self.get_lyrics(artist, title)

            if lyrics:
                tags = ID3(track_path)
                uslt_output = USLT(text=lyrics)
                tags["USLT::'eng'"] = uslt_output
                tags.save(track_path)

            return True

        except Exception as e:
            logging.warning(f"EXCEPTION at {track_path}: {e}")
            return False


    def track_refresh(self, track_path: str):

        head, ext = path.splitext(track_path)

        res = False

        if ext == self.mp3:
            res = self.mp3_refresh(track_path)
        elif ext == self.flac:
            res = self.flac_refresh(track_path)
        else:
            logging.info(f"Unknown extention: {ext}")

        return res


def add_details(file_name, lyrics=""):
    '''
    Adds the details to song
    '''

    audio = mp3.EasyMP3(file_name)


    tag_dict = {}
    for key in audio.tags:
        tag_dict[key] = audio.tags[key][0]


    tags = ID3(file_name)
    uslt_output = USLT(text=lyrics)
    tags["USLT::'eng'"] = uslt_output
    tags.save(file_name)
