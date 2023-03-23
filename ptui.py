from model import *
import math

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
        case "list following":
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

        case "list playlists":
            if(dbm.isLoggedIn()):
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1], math.ceil(p[2]/60)))
                        i+=1
                else:
                    print("\tNo Playlists!")
            else:
                print("You must be logged in!")

        case "rename playlist":
            if(dbm.isLoggedIn()):
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1], math.ceil(p[2]/60)))
                        i+=1
                    
                    while True:
                        selection = input("Select Playlist ID to edit: ")
                        if selection.isnumeric():
                            if (int(selection) - 1) in range(len(playlists)):
                                break
                        else:
                            print("Invalid Selection (must be a number)")
                    selectedIndex = int(selection) - 1
                    newName = input("Enter a new name for \"{}\": ".format(playlists[selectedIndex][0]))
                    if dbm.renamePlaylist(playlists[selectedIndex][3], newName):
                        print("Renamed playlist to \"{}\"".format(newName))
                    else:
                        print("Error renaming playlist")
                    
                else:
                    print("\tNo Playlists!")
                    continue
            else:
                print("You must be logged in!")

        case "delete playlist":
            if(dbm.isLoggedIn()):
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1], math.ceil(p[2]/60)))
                        i+=1
                    
                    while True:
                        selection = input("Select Playlist ID to delete: ")
                        if selection.isnumeric():
                            if (int(selection) - 1) in range(len(playlists)):
                                break
                        else:
                            print("Invalid Selection (must be a number)")
                    selectedIndex = int(selection) - 1
                    certain = ["y", "n"]
                    while True:
                        forActual = input("Are you sure you want to DELETE \"{}\"!? (y/n): ".format(playlists[selectedIndex][0]))
                        if(forActual.lower()[0] in certain):
                            break  
                        print("Invalid Selection!")     
                    if dbm.deletePlaylist(playlists[selectedIndex][3]):
                        print("Deleted playlist \"{}\"!".format(playlists[selectedIndex][0]))
                    else:
                        print("Error deleting playlist")
                    
                else:
                    print("\tNo Playlists!")
                    continue
            else:
                print("You must be logged in!")

        case _:
            print("Unknown Command!")