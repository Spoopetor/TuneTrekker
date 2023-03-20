'''
Connects UI to Database
'''

from datetime import datetime
import psycopg2
from sshtunnel import SSHTunnelForwarder


class Model:

    def __init__(self):
        pass

    loggedInUser = None

    

    def dbConnect():
        with open("credentials.txt") as f:
            creds = [x.split(":")[1].strip() for x in f.readlines()]
            

        username = creds[0]
        password = creds[1]
        dbName = creds[2]

        try:
            with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                    ssh_username=username,
                                    ssh_password=password,
                                    remote_bind_address=('localhost', 5432)) as server:
                server.start()
                print("SSH tunnel established")
                params = {
                    'database': dbName,
                    'user': username,
                    'password': password,
                    'host': 'localhost',
                    'port': server.local_bind_port
                }
    
                return psycopg2.connect(**params)
        except:
            print("Connection failed")


    def checkUser(self, username):
        conn = Model.dbConnect()
        curs = conn.cursor()
        try:
            curs.execute("SELECT * from \"User\" WHERE username = '{}';".format(username))
            found = curs.fetchall() != []
        finally:
                conn.close()
        return found
        

    def createUser(self, username, password, fname, lname, email):
        
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        createUserQuery = "insert into \"User\" values('1000','{}','{}','{}','{}','{}','{}');".format(dt_string, username, password, fname, lname, email)
        conn = Model.dbConnect()
        curs = conn.cursor()
        try:
            curs.execute(createUserQuery)
            curs.commit()
            print("User Successfully Created!")
        except:
            print("Failed to Create User!")
        finally:
            conn.close()

    def login(self, username, password):
        if(not self.checkUser(username)):
            print("Invalid Username!")
            return
        hashword = hash(password)

        conn = self.dbConnect()
        try:
            curs = conn.cursor()
            curs.execute("SELECT password from \"User\" WHERE username = '{}';".format(username))
            userpassword = curs.fetchone()[0]
        finally:
            conn.close()

        if userpassword == hashword:
            self.loggedInUser = username
            print("Logged in as {}".format(username))
            return
        print("Incorrect Password!")
        

