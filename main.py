import imp
import sys

from utils.spotify_functions import SpotifyWrapper
from utils.calendar_functions import Calendar
from utils.weather_functions import weatherAPI
from utils.constants import *
from utils.settings_obj import Settings
from utils.stock_functions import StockWrapper
from display_programs import CalDisplay, TimeDisplay, SpotifyDisplay, ImageDisplay
import pygame
from PIL import Image
import os
import threading
import json
import time

# Settings
SIM = True
# Globals
global temp, weather_image, stock_prices, spotify_flag, spotify_image  # Information updated from callbacks


def write_settings_to_json(settings_obj, debug=False):
    """"
    Writes the custom settings object to a dictionary
    """
    settings_dict={'button_img':settings_obj.show_image, 'button_time': settings_obj.show_time, 'button_cal':settings_obj.show_calendar, 'button_spot':settings_obj.show_spotify, 'slider_brightness':100}
    with open('temp/settings.json', 'w') as outfile:
        json.dump(settings_dict, outfile)

    if debug:
        print("Wrote settings to file")

def read_settings_json(settings_obj, debug=False):
    """"
    Writes the custom settings object to a dictionary
    """
    with open('temp/settings.json') as json_file:
        data = json.load(json_file)

    settings_obj.show_image = data['button_img']
    settings_obj.show_time = data['button_time']
    settings_obj.show_calendar = data['button_cal']
    settings_obj.show_spotify = data['button_spot']
    settings_obj.brightness = data['slider_brightness']

    if debug:
        print(f"Read settings", {data})

    return settings_obj

def main():
    if not SIM:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions

    ### MAIN SCREEN, PROGRAMS, PYGAME ###
    pygame.init()
    screen_sim = pygame.display.set_mode((WIDTH * 4, HEIGHT * 4))
    screen_main = pygame.surface.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    display_programs = []

    settings = Settings()
    if not os.path.exists('temp/settings.json'):
        write_settings_to_json(settings, debug=True)
    else:
        settings = read_settings_json(settings)
        print("Settings already exist, loading old values")

    ### IMAGE PROGRAM ###
    image_names = os.listdir(os.path.join(os.getcwd(), "images"))
    image_path_list = []
    for name in image_names:
        image_path_list.append(os.path.join(os.getcwd(), "images", name))
    image_disp = ImageDisplay(screen_main, image_path_list, IMAGE_DISPLAY_TIME)
    if settings.show_image:
        display_programs.append(image_disp)

    ### TIME PROGRAM ###
    # Stock wrapper setup
    time.sleep(1)
    stock_names = ['TSLA', 'PLTR', 'MTCH', 'TSP']
    global temp, weather_image, stock_prices
    stocks = StockWrapper(stock_names)
    stock_prices = None
    update_stocks(stocks)
    # Weather wrapper setup
    city_name = 'Philadelphia'
    weather = weatherAPI(city_name)
    temp = None
    weather_image = None
    update_weather(weather)
    time_disp = TimeDisplay(screen_main, weather_image, temp, stock_names, stock_prices)
    if settings.show_time:
        display_programs.append(time_disp)

    ### CALENDAR PROGRAM ###
    calendar = Calendar(tz='US/Eastern')
    times, events = calendar.get_today_events()
    cal_disp = CalDisplay(screen_main, times, events)
    if settings.show_calendar:
        display_programs.append(cal_disp)

    ### SPOTIFY PROGRAM ###
    # Only runs when I am playing music on spotify
    spotify = SpotifyWrapper()
    global spotify_flag, spotify_image
    spotify_flag = False
    spotify_image = None
    check_spotify(spotify)
    spot_disp = SpotifyDisplay(screen_main, spotify_image)

    # Set up LED Matrix
    if not SIM:
        options = RGBMatrixOptions()
        options.rows = WIDTH
        options.cols = HEIGHT
        options.gpio_slowdown = 4
        options.brightness = settings.brightness
        matrix = RGBMatrix(options=options)

    # Main loop
    program_num = 0
    num_of_programs = len(display_programs) - 1
    program = display_programs[program_num]

    t_settings = pygame.time.get_ticks()

    ### MAIN LOOP ###
    while 1:
        #Check if the settings changed
        current_time = pygame.time.get_ticks()
        if current_time - t_settings > CHECK_SETTINGS_FREQ:
            t_settings = current_time
            # Apply the settings changes
            old_brightness = settings.brightness
            settings = read_settings_json(settings)
            display_programs = []
            if settings.show_image:
                display_programs.append(image_disp)
            if settings.show_time:
                display_programs.append(time_disp)
            if settings.show_calendar:
                display_programs.append(cal_disp)
            num_of_programs = len(display_programs) - 1

            if old_brightness != settings.brightness:
                sys.exit()

        if spotify_flag and settings.show_spotify:
            spot_disp.update(spotify_image)

        else:
            done = program.update()
            if done:
                program_num += 1
                if program_num > num_of_programs:
                    program_num = 0

                program = display_programs[program_num]
                program.start()


        #screen_sim.blit(pygame.transform.scale(screen_main, (256, 256)), (0, 0))
        # image = Image.fromarray(pygame.surfarray.pixels3d(screen_main).swapaxes(1, 0))
        # matrix.SetImage(image, 0, 0)

        #Display the screen
        if SIM:
            screen_sim.blit(pygame.transform.scale(screen_main, (256, 256)), (0, 0))
        else:
            image = Image.fromarray(pygame.surfarray.pixels3d(screen_main).swapaxes(1, 0))
            matrix.SetImage(image, 0, 0)
        
        pygame.display.flip()
        pygame.event.pump()
        clock.tick(10)


### CALLBACK FUNCTIONS TO UPDATE GLOBAL INFORMATION ###
def check_spotify(spotify):
    global spotify_flag, spotify_image
    spotify.check_if_online()
    if spotify.is_online():
        spotify_image = spotify.get_current_img()
        if spotify_image is not None:
            spotify_flag = True
        else:
            spotify_flag = False
    else:
        spotify_flag = False
    t_spot = threading.Timer(SPOTIFY_UPDATE_FREQ, check_spotify, args=[spotify])
    t_spot.daemon = True
    t_spot.start()


def update_stocks(stocks):
    global stock_prices
    stock_prices = stocks.all_stock_prices()
    t_stock = threading.Timer(STOCKS_UPDATE_FREQ, update_stocks, args=[stocks])
    t_stock.daemon = True
    t_stock.start()


def update_weather(weather):
    global temp, weather_image
    temp = weather.get_temp()
    weather_image = weather.get_icon_image()
    t_weather = threading.Timer(WEATHER_UPDATE_FREQ, update_weather, args=[weather])
    t_weather.daemon = True
    t_weather.start()



if __name__ == "__main__":
    main()

