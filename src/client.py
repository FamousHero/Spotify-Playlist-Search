import requests
import spotipy
import tkinter as tk
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
redirect_uri = 'http://127.0.0.1:9090'
scope = ["playlist-read-private", "playlist-read-collaborative","user-top-read"]
user = spotipy.Spotify(auth_manager = spotipy.SpotifyOAuth(client_id = client_id,
client_secret = client_secret, redirect_uri= redirect_uri, scope= scope))
playlists = user.current_user_playlists()
amount_of_playlists_left = playlists["total"] - 50
offset = 50
while(amount_of_playlists_left > 0):
    playlists_to_add = user.current_user_playlists(offset=offset)
    for dict in playlists_to_add["items"]:
        playlists["items"].append(dict)
    amount_of_playlists_left -= 50
    offset += 50
#gives name of every playlist
playlists_name_id = {}
for index in range(len(playlists["items"])):
    playlists_name_id[playlists["items"][index]["name"]] = playlists["items"][index]["id"]
song_to_search = input("what song are you looking for: ")
print(song_to_search + " is in playlist: ")
playlists_with_song = []
for name in playlists_name_id:
    tracks = user.playlist_tracks(playlist_id = playlists_name_id[name], 
    fields= "items(track(name))")
    for index in range(len(tracks["items"])):
        if song_to_search == tracks["items"][index]["track"]["name"]:
            playlists_with_song.append(name)
if(len(playlists_with_song) <= 0):
    print("\tError: No playlist currently has this song")
else:
    for playlist in playlists_with_song:
        print(playlist)
    

#want to print the name of playlists with track in it
#check the song by unique id since names can repeat