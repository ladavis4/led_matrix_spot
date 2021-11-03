import spotipy
from PIL import Image
import requests
from io import BytesIO
from spotipy import SpotifyClientCredentials, SpotifyOAuth
import urllib.request
import json


class spotifyWrapper():
    def __init__(self):
        self.CID = '1fba714b4aab4063ad674ccf88a75a95'
        self.SECRET = 'd474333d8628450da05a913e8c3e0641'
        self.scope = "user-read-currently-playing"
        self.username = "ldavisiv2017"
        self.redirect_uri = "http://localhost:8888/callback/"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri=self.redirect_uri, client_secret=self.SECRET,
                                                            client_id=self.CID, scope=self.scope))

    def is_online(self):
        response = self.sp.currently_playing()
        if response is not None:
            out = True
        else:
            out = False
        return out



    def get_current_img(self):  # Function pulls tract number from census website given lat/lon.
        response = self.sp.currently_playing()
        url = response['item']['album']['images'][2]['url']
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        return img


if __name__ == "__main__":
    caller = spotifyWrapper()
    img = caller.get_current_img()
    img.show()

