from os import path
import logging
import json
from mutagen import flac, mp3

import lyricsgenius


class TrackRefresher:

    mp3 = '.mp3'
    flac = '.flac'

    def __init__(self, token: str):
        self.token = token
        self.api = lyricsgenius.Genius(token)

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
                tag_dict[key] = value

            lyrics = self.get_lyrics(tag_dict['Artist'], tag_dict['Title'])
            if lyrics:
                audio.tags['Lyrics'] = lyrics
                audio.save()

            return True

        except Exception as e:
            logging.warning(f"EXCEPTION: {e}")
            return False


    def mp3_refresh(self, track_path: str) -> bool:
        audio = mp3.MP3(track_path)
        return True


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
