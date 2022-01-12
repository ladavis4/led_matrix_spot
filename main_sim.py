from spotify_functions import SpotifyWrapper
from calendar_functions import Calendar
from weather_functions import weatherAPI
import threading
from constants import *
from stock_functions import StockWrapper
import pygame
from display_programs import CalDisplay, TimeDisplay, SpotifyDisplay, ImageDisplay
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

#Quick settings
DISPLAY_IMAGES = False
DISPLAY_MAIN = True
DISPLAY_CALENDAR = True


def check_spotify():
    global spotify_flag
    global spotify_image

    if spotify.is_online():
        spotify_image = spotify.get_current_img()
        spotify_flag = True
    else:
        spotify_flag = False
    threading.Timer(SPOTIFY_UPDATE_FREQ, check_spotify).start()

def update_stocks():
    global stock_prices
    stock_prices = stocks.all_stock_prices()
    threading.Timer(STOCKS_UPDATE_FREQ, update_weather).start()


def update_weather():
    global temp
    global weather_image
    temp = weather.get_temp()
    weather_image = weather.get_icon_image()
    threading.Timer(SPOTIFY_UPDATE_FREQ, update_weather).start()


def change_display_stock():
    global stock_num
    global num_of_stocks

    stock_num += 1
    if stock_num > num_of_stocks:
        stock_num = 0
    threading.Timer(STOCK_CHANGE_FREQ, change_display_stock).start()


if __name__ == "__main__":
    sim = False

    # images
    image_path_list = ["vibing_cat.bmp"]
    
    # stocks
    stock_names = ['TSLA', 'PLTR', 'MTCH', 'TSP']
    stock_num = 0
    num_of_stocks = len(stock_names) - 1
    stocks = StockWrapper(stock_names)
    stock_prices = None
    update_stocks()

    # weather
    city_name = 'Philadelphia'
    weather = weatherAPI(city_name)
    temp = None
    weather_image = None
    update_weather()

    # calendar
    calendar = Calendar(tz='US/Eastern')
    times, events = calendar.get_today_events() # update calendar
    
    # spotify
    spotify = SpotifyWrapper()
    global spotify_flag
    global spotify_image
    spotify_flag = False
    spotify_image = None
    spotify_title = None
    display_song_name = None
    check_spotify()

    # display and pygame
    pygame.init()
    #display_out = pygame.display.set_mode((WIDTH * 4, HEIGHT * 4))
    screen = pygame.display.set_mode((WIDTH * 4, HEIGHT * 4))
    small_screen = pygame.surface.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # led matrix
    if not sim:
        options = RGBMatrixOptions()
        options.rows = WIDTH
        options.cols = HEIGHT
        options.gpio_slowdown = 4
        matrix = RGBMatrix(options=options)

    while 1:
        while not spotify_flag:
            image_disp = ImageDisplay(small_screen, image_path_list)
            while not image_disp.done and not spotify_flag and DISPLAY_IMAGES:
                image_disp.update()
                if sim:
                    screen.blit(pygame.transform.scale(small_screen, (256, 256)), (0, 0))
                else:
                    image = Image.fromarray(pygame.surfarray.pixels3d(small_screen).swapaxes(1, 0))
                    matrix.SetImage(image, 0, 0)

                pygame.display.flip()
                pygame.event.pump()
                clock.tick(10)
                

            time_disp = TimeDisplay(small_screen, weather_image, temp, stock_names, stock_prices)
            while not time_disp.done and not spotify_flag and DISPLAY_MAIN:
                time_disp.update()
                if sim:
                    screen.blit(pygame.transform.scale(small_screen, (256, 256)), (0, 0))
                else:
                    image = Image.fromarray(pygame.surfarray.pixels3d(small_screen).swapaxes(1, 0))
                    matrix.SetImage(image, 0, 0)

                pygame.display.flip()
                pygame.event.pump()
                clock.tick(10)
                
            
            times, events = calendar.get_today_events() # update calendar
            cal_disp = CalDisplay(small_screen, times, events)
            while not cal_disp.done and not spotify_flag and DISPLAY_CALENDAR:
                cal_disp.update()
                if sim:
                    screen.blit(pygame.transform.scale(small_screen, (256, 256)), (0, 0))
                else:
                    image = Image.fromarray(pygame.surfarray.pixels3d(small_screen).swapaxes(1, 0))
                    matrix.SetImage(image, 0, 0)

                pygame.display.flip()
                pygame.event.pump()
                clock.tick(10)

        spot_disp = SpotifyDisplay(small_screen, spotify_image)
        while spotify_flag:
            spot_disp.update(spotify_image)
            if sim:
                screen.blit(pygame.transform.scale(small_screen, (256, 256)), (0, 0))
            else:
                image = Image.fromarray(pygame.surfarray.pixels3d(small_screen).swapaxes(1, 0))
                matrix.SetImage(image, 0, 0)
            pygame.display.flip()
            pygame.event.pump()
            clock.tick(1)

