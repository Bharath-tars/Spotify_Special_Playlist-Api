import spotipy
from bs4 import BeautifulSoup
import requests

travel_time = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{travel_time}")
web_html = response.text
soup = BeautifulSoup(web_html, "html.parser")
titles = soup.select("li ul li h3")
songs_playlist=[title.getText().strip() for title in titles]

user_details = spotipy.client.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id="",
client_secret="",
scope="playlist-modify-private",
redirect_uri="",
cache_path="token.txt"))

year = travel_time[0:4]
song_uris = []
for song in songs_playlist:
    song_details = user_details.search(f"track: {song} year: {year}", type='track', limit=1)
    try:
        r = song_details["tracks"]["items"][0]["uri"]
        song_uris.append(r)
    except IndexError:
        print(f"{song} doesn't exist in Spotify.")
print(song_uris)
user_id=user_details.current_user()["id"]
print(user_id)
playlist_id = user_details.user_playlist_create(user=user_id,name=f"{travel_time}Billboard 100",public=False)
user_details.playlist_add_items(playlist_id=playlist_id["id"], items=song_uris)
