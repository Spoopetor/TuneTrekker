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

def randomSongAlbum():
    album = []
    song = []
    i = 1
    while (i <= 500):
        album.append(i)
        song.append(i)
        i += 1
    random.shuffle(song)
    for x in range(500):
        model.dbExecute("insert into \"SongAlbum\" (sid, albumid, trackid) values ({}, {}, {});".format(song[x], album[x], 1))

def randomFollowing():
    follower = []
    following = []
    for i in range(1,250):
        follower.append(i)
        following.append(i+249)
        i += 1
    random.shuffle(following)
    for j in range(250):
        if j % 3 == 0:
            model.dbExecute("insert into \"follows\" (follower, following) values ({}, {});".format(follower[j], following[j]))
        else:
            model.dbExecute("insert into \"follows\" (follower, following) values ({}, {});".format(follower[j], following[j]))
            model.dbExecute("insert into \"follows\" (follower, following) values ({}, {});".format(following[j], follower[j]))

randomSongAlbum()