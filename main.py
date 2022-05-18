from utils.spotify_functions import SpotifyWrapper
from utils.calendar_functions import Calendar
from utils.weather_functions import weatherAPI
from utils.constants import *
from utils.stock_functions import StockWrapper
from display_programs import CalDisplay, TimeDisplay, SpotifyDisplay, ImageDisplay
import pygame
from PIL import Image
import os
import threading

# Settings
SIM = True

# Globals
global temp, weather_image, stock_prices, spotify_flag, spotify_image  # Information updated from callbacks


def main():
    if not SIM:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions

    ### MAIN SCREEN, PROGRAMS, PYGAME ###
    pygame.init()
    screen_sim = pygame.display.set_mode((WIDTH * 4, HEIGHT * 4))
    screen_main = pygame.surface.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    display_programs = []

    ### IMAGE PROGRAM ###
    image_names = ["vibing_cat.bmp"]
    image_path_list = []
    for name in image_names:
        image_path_list.append(os.path.join(os.getcwd(), "images", name))
    image_disp = ImageDisplay(screen_main, image_path_list)
    display_programs.append(image_disp)

    ### TIME PROGRAM ###
    # Stock wrapper setup
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
    display_programs.append(time_disp)

    ### CALENDAR PROGRAM ###
    calendar = Calendar(tz='US/Eastern')
    times, events = calendar.get_today_events()
    cal_disp = CalDisplay(screen_main, times, events)
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
        matrix = RGBMatrix(options=options)

    # Main loop
    program_num = 0
    num_of_programs = len(display_programs) - 1
    program = display_programs[program_num]
    while 1:
        if not spotify_flag:
            done = program.update()
            print(program_num)
            if done:
                program_num += 1
                if program_num > num_of_programs:
                    program_num = 0
                program = display_programs[program_num]
                program.start()
        else:
            spot_disp.update(spotify_image)

        # Display the screen
        if SIM:
            screen_sim.blit(pygame.transform.scale(screen_main, (256, 256)), (0, 0))
        else:
            image = Image.fromarray(pygame.surfarray.pixels3d(screen_sim).swapaxes(1, 0))
            matrix.SetImage(image, 0, 0)

        pygame.display.flip()
        pygame.event.pump()
        clock.tick(10)


### CALLBACK FUNCTIONS TO UPDATE GLOBAL INFORMATION ###
def check_spotify(spotify):
    global spotify_flag, spotify_image
    if spotify.is_online():
        spotify_image = spotify.get_current_img()
        spotify_flag = True
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

