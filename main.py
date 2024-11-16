import google.auth.exceptions
from utils.spotify_functions import SpotifyWrapper
from utils.calendar_functions import Calendar
from utils.constants import *
from utils.drive_functions import download_files
from display_programs import CalDisplay, TimeDisplay, SpotifyDisplay, ImageDisplay, ErrorDisplay
import utils.mqtt_functions as mqtt_functions
import pygame
from PIL import Image
import os
import time

# Settings
SIM = True

# Globals
global spotify_flag, spotify_image  # Information updated from callbacks

def main():
    # Begin MQTT monitoring
    settings = mqtt_functions.SettingMQTT(on=False)
    matrix = None

    while 1:
        while not settings.on:  # This will force the system to sleep while waiting for the signal to turn on
            time.sleep(1)

        start_successful = True
        error_strings = []

        if not SIM:
            if matrix is None: 
                from rgbmatrix import RGBMatrix, RGBMatrixOptions
                options = RGBMatrixOptions()
                options.rows = WIDTH
                options.cols = HEIGHT
                options.gpio_slowdown = 4
                options.brightness = settings.brightness
                matrix = RGBMatrix(options=options)
            else:
                matrix.brightness = settings.brightness

        ### MAIN SCREEN, PROGRAMS, PYGAME ###
        pygame.init()
        screen_sim = pygame.display.set_mode((WIDTH * 4, HEIGHT * 4))
        screen_main = pygame.surface.Surface((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        display_programs = []

        ### IMAGE PROGRAM ###
        # Download images from Google Drive into images folder
        try:
            download_files(folder_id=DRIVE_IMAGE_FOLDER_ID, local_folder_path="images/")
        except:
            print("Failed to download new image files - try deleting token.json")
        image_names = os.listdir("images")
        image_path_list = []
        for name in image_names:
            image_path_list.append(os.path.join("images", name))
        image_disp = ImageDisplay(screen_main, image_path_list, IMAGE_DISPLAY_TIME)
        if settings.show_image:
            display_programs.append(image_disp)

        ### TIME PROGRAM ###
        # Stock wrapper setup
        time.sleep(1)
        try:
            global temp, weather_image, stock_prices
            stock_prices = None
        except:
            start_successful = False
            error_strings.append("Stock API Failure")
            settings.update_time(False)
            print("There was an error with stock price API, turning off the time display")
        # Weather wrapper setup
        try:
            stock_names = ['TSLA', 'PLTR', 'MTCH', 'TSP']
            time_disp = TimeDisplay(screen_main, settings.lat, settings.long, stock_names, option=1)
            if settings.show_time:
                display_programs.append(time_disp)
        except:
            start_successful = False
            error_strings.append("Weather API Failure")
            # Update the settings to not show the calendar
            settings.update_time(False)
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
            settings.update_calendar(False)
            print("There was an error with GCal, turning off the calendar display")

        ### SPOTIFY PROGRAM ###
        global spotify_flag, spotify_image
        spotify_start_successful = False
        spotify_flag = False
        try:
            spotify = SpotifyWrapper()
            spotify_image = None
            check_spotify(spotify)
            spot_disp = SpotifyDisplay(screen_main, spotify_image)
            spotify_start_successful = True
        except Exception as error:
            start_successful = False
            print("An exception occurred:", error) # An exception occurred: division by zero
            error_strings.append("Spotify Failure")
            #Update settings
            settings.update_spotify(False)
            print("There was an error with spotify, turning off the spotify display")

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

        program_num = 0
        num_of_programs = len(display_programs) - 1
        program = display_programs[program_num]
        t_settings = pygame.time.get_ticks()
        t_spotify = pygame.time.get_ticks()
        done = False
        while settings.on:
            # check if the settings changed
            current_time = pygame.time.get_ticks()
            if current_time - t_spotify > SPOTIFY_UPDATE_FREQ and spotify_start_successful:
                check_spotify(spotify)
                t_spotify = current_time
                print("Spotify checked") 
            if current_time - t_settings > CHECK_SETTINGS_FREQ:
                t_settings = current_time
                display_programs = []
                if settings.show_image:
                    display_programs.append(image_disp)
                if settings.show_time:
                    display_programs.append(time_disp)
                if settings.show_calendar:
                    display_programs.append(cal_disp)
                if not SIM:
                    if settings.brightness != matrix.brightness:
                        matrix.brightness = settings.brightness
                num_of_programs = len(display_programs) - 1
            
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

        #Stopping and resetting:
        pygame.quit()
        if not SIM:
            #matrix.SetBrightness(1) #Turns the brightness wayyyyy down to make the screen off
            matrix.Clear()
            matrix.brightness = 1 #This might also be the answer


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

if __name__ == "__main__":
    main()

