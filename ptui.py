from model import *
import math

helpMessage = "Commands:\ncreate account - begins account creation process.\n"

print("Welcome to TuneTrekker!!!!\n\tPlease enter a command or enter 'Help' for command list.")

dbm = Model()

def tuplistToString(tuplist):
    out = ""
    for x in tuplist:
        out += x[0] + ", "
    return out[:-2]

while True:
    command = input(">> ").lower()

    match command:
        case "help":
            print(helpMessage)

        case "quit":
            print("Bye Bye!")
            exit(0)
        
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

        case "remove song":
            if(dbm.isLoggedIn()):
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1], math.ceil(p[2]/60)))
                        i+=1
                    
                    while True:
                        selection = input("Select Playlist ID to remove from: ")
                        if selection.isnumeric():
                            if (int(selection) - 1) in range(len(playlists)):
                                break
                        else:
                            print("Invalid Selection (must be a number)")
                    selectedIndex = int(selection) - 1
                    
                    playlistSongs = dbm.listSongs(playlists[selectedIndex][3])
                    if playlistSongs != False:
                        print("{}:".format(playlists[selectedIndex][0]))
                        i = 1
                        for s in playlistSongs:
                            print("\t{0: <3} :  {1}".format(i, s[0]))
                            i+=1
                        
                        while True:
                            selection = input("Select Song ID to remove from: ")
                            if selection.isnumeric():
                                if (int(selection) - 1) in range(len(playlists)):
                                    break
                            else:
                                print("Invalid Selection (must be a number)")
                        songIndex = int(selection) - 1
                        certain = ["y", "n"]
                        while True:
                            forActual = input("Are you sure you want to remove \"{}\"!? (y/n): ".format(playlistSongs[songIndex][0]))
                            if(forActual.lower()[0] in certain):
                                break  
                            print("Invalid Selection!")     
                        if dbm.removeSong(playlists[selectedIndex][3], playlistSongs[songIndex][1]):
                            print("Removed \"{}\" from \"{}\"!".format(playlistSongs[songIndex][0], playlists[selectedIndex][0]))
                        else:
                            print("Error removing song!")
                    else:
                        print("\tNo Songs!")
                    continue
                else:
                    print("\tNo Playlists!")
                    continue
            else:
                print("You must be logged in!")


        case "add song":
            if dbm.isLoggedIn():
                song = input("What song would you like to add?: ")
                songslist = dbm.searchSongName(song)
                i = 1
                print("Here are the songs that match what you searched for: \n\t")
                for s in songslist:
                    print("\t{0: <3}: {1: <18}: {2: <40}".format(i, s[1], tuplistToString(s[2])))
                    i += 1
                while True:
                    finalChoice = input("Which of these would you like to add?: ")
                    if not finalChoice.isnumeric() or int(finalChoice) > i:
                        print("Invalid Choice!!")
                    break
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1], math.ceil(p[2] / 60)))
                        i += 1
                while True:
                    playlist = input("Which of your above playlists would you like to add this song to?: ")
                    if playlist.isnumeric():
                        if (int(playlist) - 1) in range(len(playlists)):
                            break
                    else:
                        print("Invalid Selection (must be a number)")
                pid = playlists[int(playlist)-1][3]
                sidList = [songslist[int(finalChoice)-1][0]]
                if dbm.addSong(pid, sidList):
                    print("Successfully added song to playlist!")
                else:
                    print("Error adding song!!")
            else:
                print("Must be logged in!!!")

        case "add album":
            if dbm.isLoggedIn():
                album = input("What album would you like to add?: ")
                albumlist = dbm.findAlbums(album)
                i = 1
                print("Here are the albums that match what you searched for: \n\t")
                for s in albumlist:
                    print("\t{0: <3}: {1: <18}".format(i, s[0]))
                    i += 1
                while True:
                    finalChoice = input("Which of these would you like to add?: ")
                    if not finalChoice.isnumeric() or int(finalChoice) > i:
                        print("Invalid Choice!!")
                    break
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1],
                                                                                            math.ceil(p[2] / 60)))
                        i += 1
                while True:
                    playlist = input("Which of your above playlists would you like to add this album to?: ")
                    if playlist.isnumeric():
                        if (int(playlist) - 1) in range(len(playlists)):
                            break
                    else:
                        print("Invalid Selection (must be a number)")
                pid = playlists[int(playlist) - 1][3]
                sidListTuple = dbm.getSongsFromAlbum(albumlist[int(finalChoice) - 1][1])
                sidList = []
                for x in sidListTuple:
                    sidList.append(x[0])
                if dbm.addSong(pid, sidList):
                    print("Successfully added album to playlist!")
                else:
                    print("Error adding song!!")
            else:
                print("Must be logged in!!!")

        case "delete album":
            if dbm.isLoggedIn():
                album = input("What album would you like to delete?: ")
                albumlist = dbm.findAlbums(album)
                i = 1
                print("Here are the albums that match what you searched for: \n\t")
                for s in albumlist:
                    print("\t{0: <3}: {1: <18}".format(i, s[0]))
                    i += 1
                while True:
                    finalChoice = input("Which of these would you like to delete?: ")
                    if not finalChoice.isnumeric() or int(finalChoice) > i:
                        print("Invalid Choice!!")
                    break
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1],
                                                                                            math.ceil(p[2] / 60)))
                        i += 1
                while True:
                    playlist = input("Which of your above playlists would you like to delete this album from?: ")
                    if playlist.isnumeric():
                        if (int(playlist) - 1) in range(len(playlists)):
                            break
                    else:
                        print("Invalid Selection (must be a number)")
                pid = playlists[int(playlist) - 1][3]
                sidListTuple = dbm.getSongsFromAlbum(albumlist[int(finalChoice) - 1][1])
                sidList = []
                for x in sidListTuple:
                    sidList.append(x[0])
                if dbm.deleteAlbum(pid, sidList):
                    print("Successfully deleted album from playlist!")
                else:
                    print("Error deleting album!!")
            else:
                print("Must be logged in!!!")

        case "search song":
            searches = ["song name", "artist", "album", "genre"]
            while True:
                searchType = input("Search By <Song Name, Artist, Album, Genre>: ").lower()
                if(searchType in searches):
                    break
            
            match searchType:
                case "song name":
                    title = input("What title would you like to search for?: ")
                    songslist = dbm.searchSongName(title)

                    ##OTHER SEARCHES

                    if songslist == None or songslist == []:
                        print("No Results!")
                        continue
                    i = 1
                    print("SONGS:\n\t{0: <3}: {1: <18}: {2: <40}: {3: <40}".format("#", "TITLE", "ARTIST(s)", "ALBUM(s)"))
                    for s in songslist:
                        print("\t{0: <3}: {1: <18}: {2: <40}: {3: <40}: {4: <3} Minutes :   {5: <5} Listens".format(i, s[1], tuplistToString(s[2]), tuplistToString(s[3]), math.ceil(int(s[4])/60), s[5]))
                        i += 1

        case _:
            print("Unknown Command!")