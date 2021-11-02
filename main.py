from sim_display_functions import simDisplay
#from display_functions import Display
from spotify_functions import spotifyWrapper
import time




wrapper = spotifyWrapper()
display = simDisplay(64,64)


while(1):
    image = wrapper.get_current_img()
    display.clear_image()
    display.display_image(image)

    time.sleep(10)






