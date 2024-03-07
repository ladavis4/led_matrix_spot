import sys

import google.auth.exceptions

from utils.spotify_functions import SpotifyWrapper
from utils.calendar_functions import Calendar
from utils.weather_functions import weatherAPI
from utils.constants import *
from utils.settings_obj import Settings
from utils.stock_functions import StockWrapper
from utils.drive_functions import download_files
from display_programs import CalDisplay, TimeDisplay, SpotifyDisplay, ImageDisplay, ErrorDisplay
import pygame
from PIL import Image
import os
import threading
import time

# Settings
SIM = True

# Globals
global temp, weather_image, stock_prices, spotify_flag, spotify_image, feels_like, humidity  # Information updated from callbacks


def main():
    # variables to catch errors and display them to screen
    start_successful = True
    error_strings = []

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
        settings.write_settings_to_json(debug=True)
    else:
        settings.read_settings_json()
        print("Settings already exist, loading old values")

    ### IMAGE PROGRAM ###
    # Download images from Google Drive into images folder
    try:
        download_files(folder_id=DRIVE_IMAGE_FOLDER_ID, local_folder_path=os.path.join(os.getcwd(), "images"))
    except:
        print("Failed to download new image files - try deleting token.json")
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
    try:
        stock_names = ['TSLA', 'PLTR', 'MTCH', 'TSP']
        global temp, weather_image, stock_prices
        stocks = StockWrapper(stock_names)
        stock_prices = None
        update_stocks(stocks)
    except:
        start_successful = False
        error_strings.append("Stock API Failure")
        settings.show_time = False
        settings.write_settings_to_json()
        print("There was an error with stock price API, turning off the time display")


    # Weather wrapper setup
    try:
        weather = weatherAPI(lat=settings.lat, long=settings.long, city_name=settings.city_name)
        update_weather(weather)
        time_disp = TimeDisplay(screen_main, weather_image, temp, stock_names, stock_prices, humidity=humidity,
                                feels_like=feels_like, option=1)
        if settings.show_time:
            display_programs.append(time_disp)
    except:
        start_successful = False
        error_strings.append("Weather API Failure")
        # Update the settings to not show the calendar
        settings.show_time = False
        settings.write_settings_to_json()
        print("There was an error with weather API, turning off the time display")


    ### CALENDAR PROGRAM ###
    try:
        calendar = Calendar(tz='US/Eastern')
        times, events = calendar.get_today_events()
        cal_disp = CalDisplay(screen_main, times, events)
        if settings.show_calendar:
            display_programs.append(cal_disp)
    except google.auth.exceptions.RefreshError as e:
        # Display error message
        start_successful = False
        error_strings.append("GCal Failure: Delete token.json and try again")
        # Update the settings to not show the calendar
        settings.show_calendar = False
        settings.write_settings_to_json()
        print("There was an error with GCal, turning off the calendar display")

    ### SPOTIFY PROGRAM ###
    # Only runs when I am playing music on spotify
    try:
        spotify = SpotifyWrapper()
        global spotify_flag, spotify_image
        spotify_flag = False
        spotify_image = None
        check_spotify(spotify)
        spot_disp = SpotifyDisplay(screen_main, spotify_image)
    except:
        start_successful = False
        error_strings.append("Spotify Failure")
        #Update settings
        settings.show_spotify = False
        settings.write_settings_to_json()
        print("There was an error with spotify, turning off the spotify display")

    # Set up LED Matrix
    if not SIM:
        options = RGBMatrixOptions()
        options.rows = WIDTH
        options.cols = HEIGHT
        options.gpio_slowdown = 4
        options.brightness = settings.brightness
        matrix = RGBMatrix(options=options)

    # Check to make sure at least one display is turned on
    if not settings.show_spotify and not settings.show_time and not settings.show_calendar and not settings.show_image:
        start_successful = False
        error_strings.append("No screen activated!")

    ### Error Loop ###
    if not start_successful:
        error_disp = ErrorDisplay(screen_main, error_strings)
        done = False
        while not done:
            done = error_disp.update()
            # Display the screen
            if SIM:
                screen_sim.blit(pygame.transform.scale(screen_main, (256, 256)), (0, 0))
            else:
                image = Image.fromarray(pygame.surfarray.pixels3d(screen_main).swapaxes(1, 0))
                matrix.SetImage(image, 0, 0)

            pygame.display.flip()
            pygame.event.pump()
            clock.tick(10)

    # Main loop
    program_num = 0
    num_of_programs = len(display_programs) - 1
    program = display_programs[program_num]

    t_settings = pygame.time.get_ticks()
    ### MAIN LOOP ###
    while 1:
        # check if the settings changed
        current_time = pygame.time.get_ticks()
        if current_time - t_settings > CHECK_SETTINGS_FREQ:
            t_settings = current_time
            # Apply the settings changes
            old_brightness = settings.brightness
            settings.read_settings_json()
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
    global temp, weather_image, feels_like, humidity
    temp, humidity, feels_like = weather.get_temp()
    weather_image = weather.get_icon_image()
    t_weather = threading.Timer(WEATHER_UPDATE_FREQ, update_weather, args=[weather])
    t_weather.daemon = True
    t_weather.start()



if __name__ == "__main__":
    main()

