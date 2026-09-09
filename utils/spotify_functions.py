import os
import json
from io import BytesIO
from PIL import Image
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyWrapper:
    def __init__(self, debug=False):
        self.CID = None
        self.SECRET = None

        self.read_credentials(debug=debug)

        self.scope = "user-read-currently-playing"
        self.redirect_uri = "http://127.0.0.1:8888/callback"

        # Correctly pass SpotifyOAuth as the auth_manager
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.CID,
                client_secret=self.SECRET,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
                open_browser=True
            )
        )
        self.img = None
        self.current_song_name = None
        self.online = False

    def check_if_online(self):
        response = self.sp.currently_playing()
        if response is not None:
            self.online = True
        else:
            self.online = False
        return self.online

    def is_online(self):
        return self.online

    def get_current_img(self):
        try:
            response = self.sp.currently_playing()
            if response is not None and 'item' in response and response['item'] is not None:
                self.current_song_name = response['item']['name']
                # Index 2 usually targets the smaller image size (64x64), 
                # use index 0 for the largest or 1 for medium if desired.
                url = response['item']['album']['images'][0]['url']
                img_response = requests.get(url)
                self.img = Image.open(BytesIO(img_response.content))

                self.online = True
                return self.img
            else:
                self.online = False
                return None
        except Exception as e:
            print(f"EXCEPTION: Get current image failed -> {e}")
            self.online = False
            return None

    def read_credentials(self, credential_path='credentials/spotify_credentials.json', debug=False):
        full_path = os.path.join(os.getcwd(), credential_path)
        with open(full_path) as json_file:
            data = json.load(json_file)

        self.CID = data.get('cid')
        self.SECRET = data.get('secret')

        if debug:
            print(f"Read settings from {full_path}")

        return None


if __name__ == "__main__":
    caller = SpotifyWrapper(debug=True)
    out = caller.check_if_online()
    print(f"Is online: {out}")
    img = caller.get_current_img()
    if img:
        print(f"Now playing: {caller.current_song_name}")
        img.show()
    else:
        print("No song currently playing or playback is paused.")