from sim_display_functions import SimDisplay
from spotify_functions import SpotifyWrapper
import time
from weather_functions import weatherAPI
import threading
from constants import *

spotify = SpotifyWrapper()
display = SimDisplay(64, 64)
weather = weatherAPI('Claremont')

temp = weather.get_temp()
weather_image = weather.get_icon_image()

spotify_flag = False
spotify_image = None


def check_spotify():
    global spotify_flag
    global spotify_image

    spotify_flag = spotify.is_online()
    if spotify_flag:
        spotify_image = spotify.get_current_img()
    threading.Timer(SPOTIFY_UPDATE_FREQ, check_spotify).start()


def update_weather():
    global temp
    global weather_image
    temp = weather.get_temp()
    weather_image = weather.get_icon_image()
    threading.Timer(SPOTIFY_UPDATE_FREQ, update_weather).start()


check_spotify()
update_weather()
while 1:
    if spotify_flag:
        display.display_image(spotify_image)
    else:
        display.display_time_and_weather(weather_image, temp)
    time.sleep(.1)  






