'''
Connects UI to Database
'''

from datetime import datetime, timedelta
import psycopg2
from sshtunnel import SSHTunnelForwarder
import hashlib

def tuplistToString(tuplist):
    out = ""
    for x in tuplist:
        out += str(x[0]) + ", "
    return out[:-2]

class Model:

    def __init__(self):
        pass

    loggedInUser = None
    loggedInUID = None

    def isLoggedIn(self):
        return self.loggedInUser != None

    def checkUser(self, username):
        foundlist = dbExecute("SELECT * from \"User\" WHERE username = '{}';".format(username))
        found = foundlist != []
        return found
        

    def createUser(self, username, password, fname, lname, email):

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        createUserQuery = "insert into \"User\" (lastAccessed, username, password, fname, lname, email) values('{}','{}','{}','{}','{}','{}');".format(dt_string, username, hashlib.sha256((password+"BANANAS").encode('utf8')).hexdigest(), fname, lname, email)
        result = dbExecute(createUserQuery)
        if result:
            print("User Successfully Created!")
        else:
            print("Failed to Create User!")

    def login(self, username, password):

        if(not self.checkUser(username)):
                    print("Invalid Username!")
                    return
        hashword = hashlib.sha256((password+"BANANAS").encode('utf8')).hexdigest()

        userpassword = dbExecute("SELECT password from \"User\" WHERE username = '{}';".format(username))

        if userpassword[0][0] == hashword:
            self.loggedInUser = username
            self.loggedInUID = dbExecute("SELECT uid FROM \"User\" WHERE username = '{}';".format(self.loggedInUser))[0][0]
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            dbExecute("UPDATE \"User\" SET lastAccessed = '{}' WHERE uid = {};".format(dt_string, self.loggedInUID))
            print("Logged in as {}!".format(username))
            return
        print("Incorrect Password!")

    def follow(self, toFollow):
        fid = dbExecute("SELECT uid from \"User\" WHERE email = '{}'".format(toFollow))

        if fid == []:
            print("Email does not exist!")
            return False
        
        return dbExecute("INSERT INTO \"Follows\" (follower, following) VALUES ({}, {});".format(self.loggedInUID, fid[0][0]))
    
    def listFollowing(self):
        following = []
        followingIDs = dbExecute("SELECT following FROM \"Follows\" WHERE follower = {};".format(self.loggedInUID))
        for f in followingIDs:
            following.append(dbExecute("SELECT username, email FROM \"User\" WHERE uid = {};".format(f[0])))
        return following
    
    def unfollow(self, toUnfollow):
        fid = dbExecute("SELECT uid from \"User\" WHERE email = '{}'".format(toUnfollow))

        if fid == []:
            print("Email does not exist!")
            return False
        
        return dbExecute("DELETE FROM \"Follows\" WHERE follower = '{}' and following = '{}';".format(self.loggedInUID, fid[0][0]))

    def createPlaylist(self, pName):
        return dbExecute("INSERT INTO \"Playlist\" (name, uid) VALUES ('{}', {});".format(pName, self.loggedInUID))
    
    def listPlaylists(self):
        playlistIDs = []
        playlistIDs = dbExecute("SELECT name, pid FROM \"Playlist\" WHERE uid = {} ORDER BY name ASC;".format(self.loggedInUID))
        playlists = []
        for p in playlistIDs:
            psongs = dbExecute("SELECT sid FROM \"SongPlaylist\" WHERE pid = {}".format(p[1]))
            count = 0
            playtime = 0
            for s in psongs:
                count += 1
                playtime += int(dbExecute("SELECT length FROM \"Song\" WHERE sid = {}".format(s[0]))[0][0])
            playlists.append((p[0], count, playtime, p[1]))

        return playlists
    
    def renamePlaylist(self, pid, newName):
        return dbExecute("UPDATE \"Playlist\" SET name = '{}' WHERE pid = {};".format(newName, pid))

    def deletePlaylist(self, pid):
        return dbExecute("DELETE FROM \"SongPlaylist\" WHERE pid = {};".format(pid)) and dbExecute("DELETE FROM \"Playlist\" WHERE pid = {};".format(pid))
    
    def removeSong(self, pid, sid):
        return dbExecute("DELETE FROM \"SongPlaylist\" WHERE (sid = {} AND pid = {});".format(sid, pid))
    
    def listSongs(self, pid):
        songIDs = []
        songIDs = dbExecute("SELECT sid FROM \"SongPlaylist\" WHERE pid = {};".format(pid))
        if songIDs == [] or songIDs == None:
            return False
        songs = []
        for p in songIDs:
            song = dbExecute("SELECT title, sid FROM \"Song\" WHERE sid = {};".format(p[0]))
            
            
            songs.append(song[0])

        return songs

    def addSong(self, pid, sidList):
        inList = dbExecute("SELECT sid from \"SongPlaylist\" where pid = {};".format(pid))
        for x in inList:
            if x[0] in sidList:
                sidList.remove(x[0])
        for i in sidList:
            if dbExecute("INSERT INTO \"SongPlaylist\" (sid, pid) values ({}, {});".format(i, pid)):
                continue
            else:
                return False
        return True

    def deleteAlbum(self, pid, sidList):
        inList = dbExecute("SELECT sid from \"SongPlaylist\" where pid = {};".format(pid))
        remList = []
        for x in inList:
            if x[0] in sidList:
                remList.append(x[0])
        for i in remList:
            if dbExecute("DELETE FROM \"SongPlaylist\" where (sid = {} and  pid = {});".format(i, pid)):
                continue
            else:
                return False
        return True


    def searchSongName(self, title):
        songlist = dbExecute("SELECT sid, title, length, listenCount FROM \"Song\" WHERE title LIKE '%{}%' ORDER BY title ASC;".format(title))
        songinfo = []
        for s in songlist:
            artists = dbExecute("SELECT name FROM \"Artist\" WHERE artistid = (SELECT artistid FROM \"SongArtist\" WHERE sid = {});".format(s[0]))
            albums = dbExecute("SELECT name FROM \"Album\" WHERE albumid = (SELECT albumid FROM \"SongAlbum\" WHERE sid = {});".format(s[0]))
            songinfo.append((s[0], s[1], artists, albums, s[2], s[3]))
        return songinfo

    def searchSongArtist(self, name):
        artistidlist = dbExecute("SELECT artistid FROM \"Artist\" WHERE name LIKE '%{}%';".format(name))
        artistidtup = tuplistToString(artistidlist)
        artistidstring = '(' + artistidtup + ')'
        sidlist = dbExecute("SELECT sid FROM \"SongArtist\" WHERE artistid IN {};".format(artistidstring))
        sidtup = tuplistToString(sidlist)
        sidstring = "(" + sidtup + ")"
        songlist = dbExecute("SELECT sid, title, length, listenCount FROM \"Song\" WHERE sid IN {} ORDER BY title ASC;".format(sidstring))
        songinfo = []
        for s in songlist:
            artists = dbExecute("SELECT name FROM \"Artist\" WHERE artistid = (SELECT artistid FROM \"SongArtist\" WHERE sid = {});".format(s[0]))
            albums = dbExecute("SELECT name FROM \"Album\" WHERE albumid = (SELECT albumid FROM \"SongAlbum\" WHERE sid = {});".format(s[0]))
            songinfo.append((s[0], s[1], artists, albums, s[2], s[3]))
        return songinfo

    def searchAlbumName(self, name):
        albumidlist = dbExecute("SELECT albumid FROM \"Album\" WHERE name LIKE '%{}%';".format(name))
        albumidtup = tuplistToString(albumidlist)
        albumidstring = '(' + albumidtup + ')'
        sidlist = dbExecute("SELECT sid FROM \"SongAlbum\" WHERE albumid IN {};".format(albumidstring))
        sidtup = tuplistToString(sidlist)
        sidstring = "(" + sidtup + ")"
        songlist = dbExecute("SELECT sid, title, length, listenCount FROM \"Song\" WHERE sid IN {} ORDER BY title ASC;".format(sidstring))
        songinfo = []
        for s in songlist:
            artists = dbExecute("SELECT name FROM \"Artist\" WHERE artistid = (SELECT artistid FROM \"SongArtist\" WHERE sid = {});".format(s[0]))
            albums = dbExecute("SELECT name FROM \"Album\" WHERE albumid = (SELECT albumid FROM \"SongAlbum\" WHERE sid = {});".format(s[0]))
            songinfo.append((s[0], s[1], artists, albums, s[2], s[3]))
        return songinfo

    def searchGenreType(self, genre):
        gidlist = dbExecute("SELECT gid FROM \"Genre\" WHERE name LIKE '%{}%';".format(genre))
        gidtup = tuplistToString(gidlist)
        gidstring = '(' + gidtup + ')'
        sidlist = dbExecute("SELECT sid FROM \"SongGenre\" WHERE gid IN {};".format(gidstring))
        sidtup = tuplistToString(sidlist)
        sidstring = "(" + sidtup + ")"
        songlist = dbExecute("SELECT sid, title, length, listenCount FROM \"Song\" WHERE sid IN {} ORDER BY title ASC;".format(sidstring))
        songinfo = []
        for s in songlist:
            artists = dbExecute("SELECT name FROM \"Artist\" WHERE artistid = (SELECT artistid FROM \"SongArtist\" WHERE sid = {});".format(s[0]))
            albums = dbExecute("SELECT name FROM \"Album\" WHERE albumid = (SELECT albumid FROM \"SongAlbum\" WHERE sid = {});".format(s[0]))
            songinfo.append((s[0], s[1], artists, albums, s[2], s[3]))
        return songinfo

    def findAlbums(self, name):
        return dbExecute("SELECT name, albumid FROM \"Album\" WHERE name  LIKE '%{}%';".format(name))

    def getSongsFromAlbum(self, albumid):
        return dbExecute("SELECT sid FROM \"SongAlbum\" WHERE albumid = {};".format(albumid))

    def playSong(self, sid):
        now = datetime.now()
        datetime_string = now.strftime("%Y-%m-%d %H:%M:%S")
        dbExecute("INSERT INTO \"Listens\" (uid, sid, lastlistened, listencount) values ({}, {}, '{}', {}) ON CONFLICT (uid, sid) DO UPDATE SET lastlistened = '{}', listencount = \"Listens\".listencount + 1;".format(self.loggedInUID, sid, datetime_string, 1, datetime_string))
        dbExecute("UPDATE \"Song\" SET listencount = \"Song\".listencount + 1 WHERE sid = {}".format(sid))

    def playPlaylist(self, pid):
        sidlist = dbExecute("SELECT sid FROM \"SongPlaylist\" WHERE pid = {};".format(pid))
        for x in sidlist:
            now = datetime.now()
            datetime_string = now.strftime("%Y-%m-%d %H:%M:%S")
            dbExecute("INSERT INTO \"Listens\" (uid, sid, lastlistened, listencount) values ({}, {}, '{}', {}) ON CONFLICT (uid, sid) DO UPDATE SET lastlistened = '{}', listencount = \"Listens\".listencount + 1;".format(self.loggedInUID, x[0], datetime_string, 1, datetime_string))
            dbExecute("UPDATE \"Song\" SET listencount = \"Song\".listencount + 1 WHERE sid = {};".format(x[0]))

    def countPlaylists(self):
        return dbExecute("SELECT COUNT(uid) FROM \"Playlist\" WHERE uid = {};".format(self.loggedInUID))
    
    def countFollowers(self):
        return dbExecute("SELECT COUNT(follower) FROM \"Follows\" WHERE following = {};".format(self.loggedInUID))

    def countFollowing(self):
        return dbExecute("SELECT COUNT(following) FROM \"Follows\" WHERE follower = {};".format(self.loggedInUID))
    
    def topArtists(self):
        artistlist = dbExecute("SELECT a.artistid, SUM(l.listencount) AS totalListens FROM \"Listens\" l INNER JOIN \"SongArtist\" a ON l.sid = a.sid WHERE l.uid = {} GROUP BY a.artistid ORDER BY SUM(l.listencount) DESC LIMIT 10;".format(self.loggedInUID))
        artists = []
        for a in artistlist:
            name = (dbExecute("SELECT name FROM \"Artist\" WHERE artistid = {};".format(a[0])))
            artists.append((name, a[1]))
        return artists
    
    def mostPopularThirty(self):
        thirtyDaysAgo = datetime.now() - timedelta(days = 30)
        return dbExecute("SELECT DISTINCT(s.title), s.listencount as count FROM \"Song\" AS s INNER JOIN \"Listens\" as l ON l.sid = s.sid WHERE l.lastlistened >= '{}' ORDER BY count DESC LIMIT 50;".format(thirtyDaysAgo))
    
    def mostPopularFriends(self):
        return dbExecute("SELECT s.title, SUM(l.listencount) as count FROM \"Song\" AS s INNER JOIN \"Listens\" as l ON l.sid = s.sid INNER JOIN \"Follows\" as f ON f.following = l.uid WHERE f.follower = '{}' GROUP BY s.title ORDER BY count DESC LIMIT 50;".format(self.loggedInUID))
    
    def topGenres(self):
        today = datetime.today()
        monthStart = datetime(today.year, today.month, 1)
        return dbExecute("SELECT g.name, SUM(l.listencount) as count FROM \"Genre\" as g INNER JOIN \"SongGenre\" as sg ON g.gid = sg.gid INNER JOIN \"Listens\" as l ON l.sid = sg.sid WHERE l.lastlistened >= '{}' GROUP BY g.name ORDER BY count DESC LIMIT 5;".format(monthStart))
    
    def recommendPlayHistory(self):
        return dbExecute("SELECT s.title, SUM(l.listencount) as count FROM \"Song\" AS s INNER JOIN \"Listens\" AS l ON l.sid = s.sid INNER JOIN \"SongArtist\" AS sa ON sa.sid = s.sid INNER JOIN \"SongGenre\" AS sg ON sg.sid = s.sid WHERE l.sid NOT IN (SELECT DISTINCT(l.sid) FROM \"Listens\" AS l WHERE l.uid = '{}') AND (sa.artistid IN (SELECT DISTINCT(a.artistid) FROM \"SongArtist\" AS a INNER JOIN \"Listens\" AS l ON l.sid = a.sid WHERE l.uid = '{}') OR sg.gid IN (SELECT DISTINCT(g.gid) FROM \"SongGenre\" AS g INNER JOIN \"Listens\" AS l ON l.sid = g.sid WHERE l.uid = '{}') OR l.uid IN (SELECT f.following FROM \"Follows\" AS f WHERE f.follower = '{}')) GROUP BY s.title ORDER BY count DESC LIMIT 25;".format(self.loggedInUID, self.loggedInUID, self.loggedInUID, self.loggedInUID))



def dbExecute(query):

    with open("credentials.txt") as f:
        creds = [x.split(":")[1].strip() for x in f.readlines()]
            
        sshuser = creds[0]
        sshpass = creds[1]
        dbName = creds[2]

        if sshuser == "" or sshpass == "" or dbName == "":
            print("Invalid DB Credentials!\nPlease Enter Credentials in credentials.txt!")
            exit(1)

        try:
            with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                    ssh_username=sshuser,
                                    ssh_password=sshpass,
                                    remote_bind_address=('localhost', 5432)) as server:
                server.start()
                params = {
                    'database': dbName,
                    'user': sshuser,
                    'password': sshpass,
                    'host': 'localhost',
                    'port': server.local_bind_port
                }

                
                try:
                    conn = psycopg2.connect(**params)
                    curs = conn.cursor()
                    curs.execute(query)
                    if("select" in query.lower()):
                        result = curs.fetchall()
                    conn.commit()
                finally:
                    conn.close()
                if("select" in query.lower()):
                    return result
                return True
                
        except:
            print("Connection failed")
            print(result)
            return False
        
        

