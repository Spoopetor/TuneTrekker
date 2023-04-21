from model import *
import math

helpMessage = "Commands:\ncreate account - begins account creation process.\n\nlogin - login to account.\n\n" \
              "follow - allows you to follow another user by email.\n\nlist following - lists all the users you are following.\n\n" \
              "unfollow - lets you unfollow someone.\n\ncreate playlist - lets you create a playlist to store songs.\n\n" \
              "list playlists - lists all of your playlists.\n\nrename playlist - lets you rename a playlist.\n\n" \
              "view playlist - lists all songs in a specified playlist\n\n"\
              "delete playlist - delete one of your playlists.\n\nadd song - adds a song to a playlist.\n\n" \
              "remove song - removes a song from a playlist.\n\nadd ablum - adds an entire album of songs to a playlist.\n\n" \
              "remove album - removes an entire album of songs from a playlist.\n\nsearch song - lets you search for a song by name, artist" \
              ", album and genre.\n\nlisten - lets you either listen to a single song or an entire playlist.\n\nthirty - gets the top 50 songs in the last 30 days."\
              "\n\ntop friends - gets the top 50 songs your friends listen to.\n\ntop genres - gets the top 5 genres of the month\n\nrecommend - gets"\
              " recommendations for you based on your play history, as well as the play history of similar users.\n\nquit - ends the application."

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

        case "view playlist":
            if(dbm.isLoggedIn()):
                playlists = dbm.listPlaylists()
                if playlists != None and playlists != []:
                    print("{}'s Playlists:".format(dbm.loggedInUser))
                    i = 1
                    for p in playlists:
                        print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1], math.ceil(p[2]/60)))
                        i+=1
                    while True:
                        selection = input("Select Playlist ID to view: ")
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
                    else:
                        print("No Songs in Playlist!")
                        continue
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

        case "remove album":
            if dbm.isLoggedIn():
                album = input("What album would you like to remove?: ")
                albumlist = dbm.findAlbums(album)
                i = 1
                print("Here are the albums that match what you searched for: \n\t")
                for s in albumlist:
                    print("\t{0: <3}: {1: <18}".format(i, s[0]))
                    i += 1
                while True:
                    finalChoice = input("Which of these would you like to remove?: ")
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
                    playlist = input("Which of your above playlists would you like to remove this album from?: ")
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
                    print("Successfully removed album from playlist!")
                else:
                    print("Error removing album!!")
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

                    if songslist == None or songslist == []:
                        print("No Results!")
                        continue
                    i = 1
                    print("SONGS:\n\t{0: <3}: {1: <18}: {2: <40}: {3: <40}".format("#", "TITLE", "ARTIST(s)", "ALBUM(s)"))
                    for s in songslist:
                        print("\t{0: <3}: {1: <18}: {2: <40}: {3: <40}: {4: <3} Minutes :   {5: <5} Listens".format(i, s[1], tuplistToString(s[2]), tuplistToString(s[3]), math.ceil(int(s[4])/60), s[5]))
                        i += 1

                case "artist":
                    name = input("What artist would you like to search for?: ")
                    songslist = dbm.searchSongArtist(name)

                    if songslist == None or songslist == []:
                        print("No Results!")
                        continue
                    i = 1
                    print(
                        "SONGS:\n\t{0: <3}: {1: <18}: {2: <40}: {3: <40}".format("#", "TITLE", "ARTIST(s)", "ALBUM(s)"))
                    for s in songslist:
                        print("\t{0: <3}: {1: <18}: {2: <40}: {3: <40}: {4: <3} Minutes :   {5: <5} Listens".format(i, s[1], tuplistToString(s[2]), tuplistToString(s[3]), math.ceil(int(s[4]) / 60), s[5]))
                        i += 1

                case "album":
                    name = input("What album would you like to search for?: ")
                    songslist = dbm.searchAlbumName(name)

                    if songslist == None or songslist == []:
                        print("No Results!")
                        continue
                    i = 1
                    print("SONGS:\n\t{0: <3}: {1: <18}: {2: <40}: {3: <40}".format("#", "TITLE", "ARTIST(s)", "ALBUM(s)"))
                    for s in songslist:
                        print("\t{0: <3}: {1: <18}: {2: <40}: {3: <40}: {4: <3} Minutes :   {5: <5} Listens".format(i, s[1], tuplistToString(s[2]), tuplistToString(s[3]), math.ceil(int(s[4])/60), s[5]))
                        i += 1

                case "genre":
                    genre = input("What genre would you like to search for?: ")
                    songslist = dbm.searchGenreType(genre)

                    if songslist == None or songslist == []:
                        print("No Results!")
                        continue
                    i = 1
                    print("SONGS:\n\t{0: <3}: {1: <18}: {2: <40}: {3: <40}".format("#", "TITLE", "ARTIST(s)", "ALBUM(s)"))
                    for s in songslist:
                        print("\t{0: <3}: {1: <18}: {2: <40}: {3: <40}: {4: <3} Minutes :   {5: <5} Listens".format(i, s[1],tuplistToString(s[2]),tuplistToString(s[3]),math.ceil(int(s[4]) / 60),s[5]))
                        i += 1

        case "listen":
            searches = ["song", "playlist"]
            while True:
                choice = input("Would you like to listen to a song or a playlist (input song or playlist)?: ").lower()
                if(choice in searches):
                    break
            match choice:
                case "song":
                    title = input("What title would you like to search for?: ")
                    songslist = dbm.searchSongName(title)

                    if songslist == None or songslist == []:
                        print("No Results!")
                        continue
                    i = 1
                    print("SONGS:\n\t{0: <3}: {1: <18}: {2: <40}: {3: <40}".format("#", "TITLE", "ARTIST(s)", "ALBUM(s)"))
                    for s in songslist:
                        print("\t{0: <3}: {1: <18}: {2: <40}: {3: <40}: {4: <3} Minutes :   {5: <5} Listens".format(i, s[1], tuplistToString(s[2]), tuplistToString(s[3]), math.ceil(int(s[4]) / 60), s[5]))
                        i += 1
                    choice = input("Which of these songs would you like to listen to?: ")
                    dbm.playSong(songslist[int(choice) - 1][0])
                    print("Listened to " + songslist[int(choice)-1][1])
                case "playlist":
                    playlists = dbm.listPlaylists()
                    if playlists != None and playlists != []:
                        print("{}'s Playlists:".format(dbm.loggedInUser))
                        i = 1
                        for p in playlists:
                            print("\t{0: <3} :  {1: <18}: {2: <3} songs  :  {3} minutes".format(i, p[0], p[1],math.ceil(p[2] / 60)))
                            i += 1
                    else:
                        print("\tNo Playlists!")
                        continue
                    while True:
                        playlist = input("Which of your above playlists would you like to listen to?: ")
                        if playlist.isnumeric():
                            if (int(playlist) - 1) in range(len(playlists)):
                                break
                        else:
                            print("Invalid Selection (must be a number)")
                    pid = playlists[int(playlist)-1][3]
                    dbm.playPlaylist(pid)
                    print("Listened to " + playlists[int(playlist)-1][0])

        case "thirty":
            if(dbm.isLoggedIn()):
                songslist = dbm.mostPopularThirty()
                count = 1
                for s in songslist:
                    print("#"+str(count)+ " - " + s[0])
                    count += 1

        case "top friends":
            if(dbm.isLoggedIn()):
                songslist = dbm.mostPopularFriends()
                count = 1
                for s in songslist:
                    print("#"+str(count)+ " - " + s[0])
                    count += 1

        case "top genres":
            genrelist = dbm.topGenres()
            count = 1
            for g in genrelist:
                print("#"+str(count)+ " - " + g[0])
                count += 1

        case "recommend":
            reclist = dbm.recommendPlayHistory()
            print("Here's 25 songs we think you might like:")
            for r in reclist:
                print(r[0])





        case _:
            print("Unknown Command!")