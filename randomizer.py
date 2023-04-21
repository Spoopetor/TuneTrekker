import random
from datetime import datetime
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
        print("success")

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
        print("success")

def randomFollowing():
    follower = []
    following = []
    for i in range(1,251):
        follower.append(i)
        following.append(i+250)
        i += 1
    random.shuffle(following)
    for j in range(250):
        if j % 3 == 0:
            model.dbExecute("insert into \"Follows\" (follower, following) values ({}, {});".format(follower[j], following[j]))
            print("success")
        else:
            model.dbExecute("insert into \"Follows\" (follower, following) values ({}, {});".format(follower[j], following[j]))
            print("success")
            model.dbExecute("insert into \"Follows\" (follower, following) values ({}, {});".format(following[j], follower[j]))
            print("success")


def randomRatingListens():
    for x in range(1,501):
        listencount = random.randint(0,10000)
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        rating = random.randint(1,5)
        sid = random.randint(1,500)
        model.dbExecute("insert into \"Listens\" (uid, sid, lastlistened, listencount) values ({}, {}, '{}', {});".format(x, sid, dt_string, listencount))
        model.dbExecute("insert into \"Rating\" (uid, sid, rating) values ({}, {}, {});".format(x, sid, rating))
        model.dbExecute("update \"Song\" set listencount = listencount + {} where sid = {};".format(listencount, sid))
        print("success")

def assignAlbumArtist():
    for x in range(1,501):
        ids = model.dbExecute("select a1.albumid, a2.artistid from \"SongAlbum\" a1, \"SongArtist\" a2 where a1.sid = {} and (a2.sid = {});".format(x, x))
        model.dbExecute("insert into \"AlbumArtist\" (albumid, artistid) values ({}, {});".format(ids[0][0], ids[0][1]))
        print("success")

def assignSongGenre():
    for x in range(1,501):
        ids = model.dbExecute("select a1.sid, a2.gid from \"SongAlbum\" a1, \"AlbumGenre\" a2 where a1.albumid = {} and (a2.albumid = {});".format(x, x))
        for y in range(len(ids)):
            model.dbExecute("insert into \"SongGenre\" (sid, gid) values ({}, {});".format(ids[y][0], ids[y][1]))
            print("success")

def randomSongPlaylist():
    for x in range(101,104):
        number = random.randint(1, 3)
        if number == 1:
            songs = random.sample(range(1, 501), 1)
            model.dbExecute("insert into \"SongPlaylist\" (sid, pid) values ({}, {});".format(songs[0], x))
            print("success")
        elif number == 2:
            songs = random.sample(range(1, 501), 2)
            model.dbExecute("insert into \"SongPlaylist\" (sid, pid) values ({}, {});".format(songs[0], x))
            model.dbExecute("insert into \"SongPlaylist\" (sid, pid) values ({}, {});".format(songs[1], x))
            print("success")
        else:
            songs = random.sample(range(1, 501), 3)
            model.dbExecute("insert into \"SongPlaylist\" (sid, pid) values ({}, {});".format(songs[0], x))
            model.dbExecute("insert into \"SongPlaylist\" (sid, pid) values ({}, {});".format(songs[1], x))
            model.dbExecute("insert into \"SongPlaylist\" (sid, pid) values ({}, {});".format(songs[2], x))
            print("success")

randomSongPlaylist()