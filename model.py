'''
Connects UI to Database
'''

from datetime import datetime
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
        createUserQuery = "insert into \"User\" (lastAccessed, username, password, fname, lname, email) values('{}','{}','{}','{}','{}','{}');".format(dt_string, username, hashlib.sha256(password.encode('utf8')).hexdigest(), fname, lname, email)
        result = dbExecute(createUserQuery)
        if result:
            print("User Successfully Created!")
        else:
            print("Failed to Create User!")

    def login(self, username, password):

        if(not self.checkUser(username)):
                    print("Invalid Username!")
                    return
        hashword = hashlib.sha256(password.encode('utf8')).hexdigest()

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
        for x in sidList:
            if x in inList[0:len(inList)][0]:
                continue
            else:
                sidList.remove(x)
        print(sidList)
        for i in sidList:
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
        pass

    def searchAlbumName(self, name):
        sidlist = dbExecute("SELECT sid FROM \"SongAlbum\" WHERE albumid = (SELECT albumid FROM \"Album\" WHERE name LIKE '%{}%');".format(name))
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

def dbExecute(query):

    with open("credentials.txt") as f:
        creds = [x.split(":")[1].strip() for x in f.readlines()]
            
        sshuser = creds[0]
        sshpass = creds[1]
        dbName = creds[2]

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
            return False
        
        

