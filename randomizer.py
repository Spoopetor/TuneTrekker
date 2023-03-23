import random

import model


def randomSongArtist():
    artist = []
    song = []
    i = 1
    while(i <= 500):
        artist.append(i)
        song.append(i)
        i += 1
    random.shuffle(song)
    for x in range(500):
        model.dbExecute("insert into \"SongArtist\" (sid, artistid) values ({}, {});".format(song[x], artist[x]))

randomSongArtist()