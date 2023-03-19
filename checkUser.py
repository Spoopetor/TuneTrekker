import psycopg2
from sshtunnel import SSHTunnelForwarder
from datetime import datetime


def checkUser(curs, username):
    curs.execute("SELECT * from \"User\" WHERE username = '%s';"% username)
    return(curs.fetchall() != [])

def createUser(curs, username):
    password = str(input("What would you like your password to be? "))
    fname = str(input("What is your first name? "))
    lname = str(input("What is your last name? "))
    email = str(input("What is a good email? "))
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    createUserQuery = "insert into \"User\" values('1000','" + dt_string + "','" + username + "','" + password \
                      + "','" + fname + "','" + lname + "','" + email + "');"
    print(createUserQuery)
    curs.execute(createUserQuery)







