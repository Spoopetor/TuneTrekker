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
        case "follow":
            if(dbm.isLoggedIn()):
                toFollow = input("Enter the email of the account you want to follow: ")
                if(dbm.follow(toFollow)):
                    print("Followed {}!".format(toFollow))
                else:
                    print("Error Following {}!".format(toFollow))
            else:
                print("You must be logged in!")
        case "following":
            following = dbm.listFollowing()
            if following != None and following != []:
                print("{} is Following:".format(dbm.loggedInUser))
                i = 1
                for f in following:
                    print("\t{}. {} - {}".format(i, f[0][0], f[0][1]))
                    i+=1
            else:
                print("\tNot Following Anyone")
        case "unfollow":
            if(dbm.isLoggedIn()):
                toUnfollow = input("Enter the email of the account you want to unfollow: ")
                if(dbm.unfollow(toUnfollow)):
                    print("Unfollowed {}!".format(toUnfollow))
                else:
                    print("Error Unfollowing {}!".format(toUnfollow))
            else:
                print("You must be logged in!")
                
        case "create playlist":
            if(dbm.isLoggedIn()):
                pname = input("Enter a name for your playlist: ")
                if(dbm.createPlaylist(pname)):
                    print("Playlist Successfully Created!")
                else:
                    print("Error Making Playlist!")
            else:
                print("You must be logged in!")

        case _:
            print("Unknown Command!")