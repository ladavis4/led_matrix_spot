import os

import spotipy
from PIL import Image
import requests
from io import BytesIO
from spotipy import SpotifyClientCredentials, SpotifyOAuth
import json



class SpotifyWrapper:
    def __init__(self, debug=False):
        self.CID = None
        self.SECRET = None

        self.read_credentials()

        self.scope = "user-read-currently-playing"
        self.username = "ldavisiv2017"
        self.redirect_uri = "http://localhost:8888/callback/"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri=self.redirect_uri, client_secret=self.SECRET,
                                                            client_id=self.CID, scope=self.scope))
        self.img = None
        self.current_song_name = None

        self.online = False

    def check_if_online(self):
        response = self.sp.currently_playing()
        if response is not None:
            self.online = True
        else:
            self.online = False

    def is_online(self):
        return self.online

    def get_current_img(self):
        try:
            response = self.sp.currently_playing()
            if response is not None:
                self.current_song_name = response['item']['name']
                url = response['item']['album']['images'][2]['url']
                response = requests.get(url)
                self.img = Image.open(BytesIO(response.content))

                self.online = True
                return self.img
            else:
                self.online = False
                return None
        except:
            print("EXCEPTION: Get current image failed")
            return None

    def read_credentials(self, credential_path ='credentials/spotify_credentials.json', debug=False):
        with open(os.path.join(os.getcwd(), credential_path)) as json_file:
            data = json.load(json_file)

        self.CID = data['cid']
        self.SECRET = data['secret']

        if debug:
            print(f"Read settings", {data})

        return None


if __name__ == "__main__":
    caller = SpotifyWrapper(debug=True)
    out = caller.check_if_online()
    print(out)
    img = caller.get_current_img()
    img.show()

