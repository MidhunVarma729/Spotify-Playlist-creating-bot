from spotipy.oauth2 import SpotifyOAuth
import spotipy
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Loading the credentials from the .env file
USER_ID = os.getenv('USER_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


# Taking input date and scraping the data from billboard
date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD:')
URL = 'https://www.billboard.com/charts/hot-100/' + date
req = requests.get(url=URL)
html_code = req.text
soap = BeautifulSoup(html_code, 'html.parser')
tags = soap.find_all(name="h3", id="title-of-a-story", class_="a-truncate-ellipsis")
songs = [tag.getText().strip() for tag in tags]


# Authorizing spotify account
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-public"))


# print(songs)
SONG_IDS = []

# retrieving song id's to search in spotify
for i in songs:
    details = sp.search(
        q=f"track: {i}", limit=1, offset=0, type='track')
    try:
        details['tracks']['items'][0]['id']
    except:
        pass
    else:
        SONG_IDS.append(details['tracks']['items'][0]['id'])

# Creating an empty playlist
results = sp.user_playlist_create(
    user=USER_ID, name=f'Top 100 on {date}')
PLAYLIST_ID = results['id']

# Loading all the songs through id's into the newly created playlist
results = sp.user_playlist_add_tracks(
    user=USER_ID, playlist_id=PLAYLIST_ID, tracks=SONG_IDS)
