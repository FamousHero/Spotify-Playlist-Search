import requests
import spotipy
import webbrowser
class Client:
    #implement gui to   1)take current song or a song name
    #                   2)Ask for a new search
    #                   3) allow user to logout
    #implement in code
    #                   1)add a way to check cache for current spotify account
    #                   2)search with current song (by song_id)
    #                   3) clear user tokens when they logout
    
    #Bugs: only checks the 1st 100 of eah playlist
    def __init__(self):
        pass
    def search(self, searchType):
        """Get the users playlists and pass it to the specified search"""
        client_id = YOUR_CLIENT_ID
        client_secret = YOUR_CLIENT_SECRET
        redirect_uri = 'http://127.0.0.1:9090'
        scope = ["playlist-read-private", "playlist-read-collaborative","user-top-read"]
        
        auth_manager = spotipy.SpotifyOAuth(client_id = client_id,
        client_secret = client_secret, redirect_uri= redirect_uri, scope= scope)
        user = spotipy.Spotify(auth_manager = auth_manager)
        playlists = user.current_user_playlists()
        amount_of_playlists_left = playlists["total"] - 50
        offset = 50
        while(amount_of_playlists_left > 0):
            playlists_to_add = user.current_user_playlists(offset=offset)
            for dict in playlists_to_add["items"]:
                playlists["items"].append(dict)
            amount_of_playlists_left -= 50
            offset += 50
        if searchType == "name":
           self.search_by_name(input, playlists, user)
        #elif searchType == "current_song":
        #   search_by_current_song(client_id, client_secret, redirect_uri)
        return
    def search_by_name(self, song_name, playlists, user):
        playlists_name_id = {}
        for index in range(len(playlists["items"])):
            playlists_name_id[playlists["items"][index]["name"]] = playlists["items"][index]["id"]
        song_name = input("----------\n"+
        "What song are you looking for: ")
        print(song_name + " is in playlist: ")
        playlists_with_song = []
        for name in playlists_name_id:
            tracks = user.playlist_tracks(playlist_id = playlists_name_id[name], 
            fields= "items(track(name))")
            for index in range(len(tracks["items"])):
                if song_name == tracks["items"][index]["track"]["name"]:
                    playlists_with_song.append(name)
        if(len(playlists_with_song) <= 0):
            print("\tError: No playlist currently has this song")
        else:
            for playlist in playlists_with_song:
                print("\t"+playlist)


    #gives name of every playlist
    

    #want to print the name of playlists with track in it
    #check the song by unique id since names can repeat
