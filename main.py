from display_functions import Display
from spotify_functions import SpotifyWrapper
import time
from weather_functions import weatherAPI
import threading
from constants import *
from stock_functions import StockWrapper

stock_names = ['TSLA', 'PLTR', 'MTCH', 'TSP']
stock_num = 0
num_of_stocks = len(stock_names) - 1
city_name = 'Claremont'

stocks = StockWrapper(stock_names)
print("Done with stock init")
spotify = SpotifyWrapper()
print("Done with spotify init")
display = Display(64, 64)
print("Done with display init")
weather = weatherAPI(city_name)
print("Done with weather init")

temp = None
weather_image = None
stock_prices = None

spotify_flag = False
spotify_image = None
spotify_title = None
display_song_name = None


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


check_spotify()
update_weather()
update_stocks()
change_display_stock()


while 1:
    if spotify_flag:
        display.display_image(spotify_image)
    else:
        display.display_time_and_weather(weather_image, temp, stock_names[stock_num], stock_prices[stock_num])
    time.sleep(.05)









