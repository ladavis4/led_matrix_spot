from sim_display_functions import simDisplay
#from display_functions import Display
from spotify_functions import spotifyWrapper
import time
from datetime import datetime





spotify = spotifyWrapper()
display = simDisplay(64, 64)



while(1):
    if spotify.is_online():
        display.display_image(spotify.get_current_img())
    else:
        display.display_time()
    time.sleep(1)






