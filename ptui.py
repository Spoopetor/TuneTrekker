from model import *

helpMessage = "Commands:\ncreate account - begins account creation process.\n"

print("Welcome to TuneTrekker!!!!\n\tPlease enter a command or enter 'Help' for command list.")

while(True):
    command = input(">> ").lower()

    match command:
        case "help":
            print(helpMessage)
        
        case "create account":
            while(True):
                username = str(input("What would you like your username to be? "))
                if(not checkUser(username)):
                    while(True):
                        password = str(input("Enter a password (8 character or greater): "))
                        if(len(password) >= 8):
                            break
                        print("Password too short!")
                    fname = str(input("What is your first name? "))
                    lname = str(input("What is your last name? "))
                    while(True):
                        email = str(input("What is a good email? "))
                        if(email.contains("@") and email.contains(".")):
                            break
                        print("Invalid email!")

                    createUser(username, password, fname, lname, email)
                    break
                else:
                    print("Username is taken!")
            


        case _:
            print("Unknown Command!")