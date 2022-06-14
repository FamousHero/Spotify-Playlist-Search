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
    def search(self, searchType, songname=None, artist=None):
        """Get the users playlists and pass it to the specified search"""
        song_id = None

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
        
        if(searchType == "current_song"):
           temp = user.current_user_playing_track()
           artist = temp["item"]["artists"][0]["name"]
           songname = temp["item"]["name"]
           song_id = temp["item"]["external_ids"]["isrc"]
           del temp

        header = songname
        if(artist != None):
            header += " by " + artist
        header += " is in:\n"
        returnstring = header 
        playlists_name_id = {}
        for index in range(len(playlists["items"])):
            playlists_name_id[playlists["items"][index]["name"]] = playlists["items"][index]["id"]
        
        for playlist in playlists_name_id:
            if(searchType == "name"):
                tracks = user.playlist_tracks(playlist_id = playlists_name_id[playlist], 
                fields= "items(track(album(artists), name)), total")
                self.get_total_info(user, tracks, "track_name", tracks["total"], playlists_name_id[playlist])
                for index in range(tracks["total"]):
                    if tracks["items"][index]["track"] != None:
                        if songname == tracks["items"][index]["track"]["name"]:
                            if artist == None:
                                returnstring += playlist+"\n"
                            elif artist.lower() == tracks["items"][index]["track"]["album"]["artists"][0]["name"].lower():
                                returnstring += playlist+"\n"
            elif(searchType == "current_song"):
                tracks = user.playlist_tracks(playlist_id = playlists_name_id[playlist], 
                fields= "items(track(external_ids)), total")
                self.get_total_info(user, tracks, "track_ids", tracks["total"], playlists_name_id[playlist])
                for index in range(tracks["total"]):
                    if tracks["items"][index]["track"] != None and "isrc" in tracks["items"][index]["track"]["external_ids"]:
                        if song_id == tracks["items"][index]["track"]["external_ids"]["isrc"]:
                            returnstring += playlist+"\n"
                        
        if(returnstring == header):
            return "\tError: No playlist currently has this song"
        else:
            return returnstring


    def get_total_info(self, user, container, type, total, playlist_id = None):
        if type == "playlist":
            offset = 50
            while(total > offset):
                playlists_to_add = user.current_user_playlists(offset=offset)
                container["items"].extend(playlists_to_add["items"])
                offset += 50
        elif type == "track_name":
            offset = 100
            while(total > offset):
                tracks_to_add = user.playlist_tracks(playlist_id = playlist_id, 
                                                    fields= "items(track(album(artists),name))", offset = offset)
                container["items"].extend(tracks_to_add["items"])
                offset += 100
        elif type == "track_ids":
            offset = 100
            while(total > offset):
                tracks_to_add = user.playlist_tracks(playlist_id = playlist_id, 
                                                    fields= "items(track(external_ids(isrc)))", offset = offset)
                container["items"].extend(tracks_to_add["items"])
                offset += 100
        return


