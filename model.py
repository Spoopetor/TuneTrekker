'''
Connects UI to Database
'''

from datetime import datetime
import psycopg2
from sshtunnel import SSHTunnelForwarder
import hashlib


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
            print("Logged in as {}!".format(username))
            return
        print("Incorrect Password!")

    def follow(self, toFollow):
        fid = dbExecute("SELECT uid from \"User\" WHERE email = '{}'".format(toFollow))

        if fid == []:
            print("Email does not exist!")
            return
        
        return dbExecute("INSERT INTO \"Follows\" (follower, following) VALUES ({}, {});".format(self.loggedInUID, fid[0][0]))
    
    def listFollowing(self):
        following = []
        followingIDs = dbExecute("SELECT following FROM \"Follows\" WHERE follower = {};".format(self.loggedInUID))
        for f in followingIDs:
            following.append(dbExecute("SELECT username, email FROM \"User\" WHERE uid = {};".format(f[0])))
        return following


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
        
        

