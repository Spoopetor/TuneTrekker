from model import *

helpMessage = "Commands:\ncreate account - begins account creation process.\n"

print("Welcome to TuneTrekker!!!!\n\tPlease enter a command or enter 'Help' for command list.")

dbm = Model()

while True:
    command = input(">> ").lower()

    match command:
        case "help":
            print(helpMessage)
        
        case "create account":
            while True:
                username = str(input("What would you like your username to be? "))
                if not dbm.checkUser(username):
                    while True:
                        password = str(input("Enter a password (8 character or greater): ")).strip()
                        if len(password) >= 8:
                            break
                        print("Password too short!")
                    fname = str(input("What is your first name? "))
                    lname = str(input("What is your last name? "))
                    while True:
                        email = str(input("What is a good email? "))
                        if "@" in email and "." in email:
                            break
                        print("Invalid email!")

                    dbm.createUser(username, password, fname, lname, email)
                    break
                else:
                    print("Username is taken!")
        case "login":
            username = input("Enter Username: ")
            password = input("Enter Password: ").strip()

            dbm.login(username, password)

        case _:
            print("Unknown Command!")