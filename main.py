#from sim_display_functions import simDisplay
from display_functions import Display
from spotify_functions import spotifyWrapper
import time
from datetime import datetime
from weather_functions import weatherAPI





spotify = spotifyWrapper()
display = Display(64, 64)
weather = weatherAPI('Philadelphia')

temp = weather.get_temp()
img = weather.get_icon_image()

while 1:
    if spotify.is_online():
        display.display_image(spotify.get_current_img())
    else:
        display.display_time_and_weather(img, temp)

    time.sleep(.1)  






