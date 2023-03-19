'''
Connects UI to Database
'''

from datetime import datetime
import psycopg2
from sshtunnel import SSHTunnelForwarder

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


def checkUser(username):
    conn = dbConnect()
    curs = conn.cursor()
    curs.execute("SELECT * from \"User\" WHERE username = '{}';".format(username))
    conn.close()
    return(curs.fetchall() != [])
    

def createUser(username, password, fname, lname, email):
    
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    createUserQuery = "insert into \"User\" values('1000','{}','{}','{}','{}','{}','{}');".format(dt_string, username, password, fname, lname, email)
    conn = dbConnect()
    curs = conn.cursor()
    try:
        curs.execute(createUserQuery)
        curs.commit()
        print("User Successfully Created!")
    except:
        print("Failed to Create User!")
    finally:
        conn.close()
    
