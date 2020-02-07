import lyricsgenius





token = 'slcoSGPx2vPljso3yHWwGB2uNzQ1rpV9dGqHYzSpWuOlaWXsqYeC1v9IaQvZ3Sta'

song_id = 1912895

genius = lyricsgenius.Genius(token)
song = genius.search_song("Frame of mind", "Tristam")

print(song.lyrics)
