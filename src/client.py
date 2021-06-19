import requests
import spotipy
import webbrowser
import time

class Client:
    #implement gui to
    #                   1) allow user to logout
    #
    #implement in code
    #                   1)add a way to check cache for current spotify account
    #                   3) clear user tokens when they logout
    #                   4) possible create a database storing playlists and their songs
    #                   so that you dont have to get the info from the api every call (.2 per playlist,
    #                                                                                  .1 per tracks)
    #                   if done just check every call that the total playlists == db using offset=total(.2s)
    #                   if it doesnt you will have the missing playlists starting at offset and 
    #                   can reuse code to build db
    #                   do the same for tracks
    def __init__(self):
        pass
    def search(self, searchType, name=None):
        """Get the users playlists and pass it to the specified search"""
        client_id = YOUR_CLIENT_ID
        client_secret = YOUR_CLIENT_SECRET

        redirect_uri = 'http://127.0.0.1:9090'
        scope = ["playlist-read-private", "playlist-read-collaborative"
                ,"user-top-read", "user-read-currently-playing"]
        
        auth_manager = spotipy.SpotifyOAuth(client_id = client_id,
        client_secret = client_secret, redirect_uri= redirect_uri, scope= scope)
        user = spotipy.Spotify(auth_manager = auth_manager)
        playlists = user.current_user_playlists()
        amount_of_playlists = playlists["total"] 
        self.get_total_info(user, playlists, "playlist", amount_of_playlists)        
        if searchType == "name":
           return self.search_by_name(name, playlists, user)
        
        elif searchType == "current_song":
            song_name = user.current_user_playing_track()
            song_name = song_name["item"]["name"]
            return self.search_by_name(song_name, playlists, user)




    def search_by_name(self, song_name, playlists, user):
        returnstring = song_name + " is in:\n"
        playlists_name_id = {}
        for index in range(len(playlists["items"])):
            playlists_name_id[playlists["items"][index]["name"]] = playlists["items"][index]["id"]
        playlists_with_song = []
        search_timer = time.time()
        #self.search_song_in_playlists()
        for name in playlists_name_id:
            track_time = time.time()
            tracks = user.playlist_tracks(playlist_id = playlists_name_id[name], 
            fields= "items(track(name)), total")
            self.get_total_info(user, tracks, "tracks", tracks["total"], playlists_name_id[name])
            mid_index = tracks["total"]
            for index in range(tracks["total"]):
                if tracks["items"][index]["track"] != None:
                    if song_name == tracks["items"][index]["track"]["name"]:
                        returnstring += name+"\n"
        if(returnstring == song_name + " is in:\n"):
            return "\tError: No playlist currently has this song"
        else:
            #for playlist in playlists_with_song:
            #    print("\t"+playlist)
            #print("search_by_name() time: %s" % (time.time()-search_timer))
            return returnstring

    def get_total_info(self, user, container, type, total, playlist_id = None):
        if type == "playlist":
            offset = 50
            while(total > offset):
                playlists_to_add = user.current_user_playlists(offset=offset)
                container["items"].extend(playlists_to_add["items"])
                offset += 50
        elif type == "tracks":
            offset = 100
            while(total > offset):
                tracks_to_add = user.playlist_tracks(playlist_id = playlist_id, 
                                                    fields= "items(track(name))", offset = offset)
                container["items"].extend(tracks_to_add["items"])
                offset += 100
        return
