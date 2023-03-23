import random

def randomSongArtist():
    artist = []
    song = []
    i=1
    while(i<=500):
        artist.append(i)
        song.append(i)
        i += 1
    random.shuffle(song)

