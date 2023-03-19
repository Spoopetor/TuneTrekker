'''
Connects UI to Database
'''

import psycopg2
from sshtunnel import SSHTunnelForwarder

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


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")
        conn.close()
except:
    print("Connection failed")
