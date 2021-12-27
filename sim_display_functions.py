from PIL import Image, ImageDraw, ImageFont
import pygame
from datetime import datetime

from constants import *


class SimDisplay:
    def __init__(self, width, height, scaler=6):
        #pygame
        pygame.init()
        self.out_screen = pygame.display.set_mode((width * scaler, height * scaler))
        self.screen = pygame.surface.Surface((width, height))
        pygame.display.set_caption("Display")
        pygame.font.init()
        self.font_time = pygame.font.Font(r"VeraMono.ttf", 20)
        self.font_temp = pygame.font.Font(r"VeraMono.ttf", 13)
        self.font_stocks = pygame.font.Font(r"VeraMono.ttf", 10)

        self.background = pygame.surface.Surface((width, height))
        self.background.fill(BLACK)

        self.image = Image.new("RGB", (width, height))
        self.width = width
        self.height = height
        self.scaler = scaler

        self.screen.fill(BLACK)

    def display_image(self, image):

        mode = image.mode
        size = image.size
        data = image.tobytes()

        py_image = pygame.image.fromstring(data, size, mode)
        py_image = pygame.transform.scale(py_image, (self.width, self.height))
        self.screen.blit(py_image, (0, 0))
        picture = pygame.transform.scale(self.screen, (self.width * self.scaler, self.height * self.scaler))
        self.out_screen.blit(picture, (0, 0))
        pygame.display.flip()
        pygame.event.pump()

    def display_time_and_weather(self, image, temp, stock_name, stock_price):
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # Add time to surface
        txt_surf = self.font_time.render(current_time, False, WHITE)
        txt_rect = txt_surf.get_rect()
        txt_rect.center = (self.width/2, self.height/2)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(txt_surf, txt_rect)

        # Add Temperature to surface
        txt_surf = self.font_temp.render(str(temp) + "F", False, WHITE)
        txt_rect = txt_surf.get_rect()
        txt_rect.midbottom = (self.width/4, self.height)
        self.screen.blit(txt_surf, txt_rect)

        # Weather to surface
        mode = image.mode
        size = image.size
        data = image.tobytes()
        weather_image = pygame.image.fromstring(data, size, mode)
        weather_image = pygame.transform.scale(weather_image, (32, 28))
        weather_rect = weather_image.get_rect()
        weather_rect.midbottom = (self.width * 3 / 4, self.height + 6)
        self.screen.blit(weather_image, weather_rect)

        # Add stocks to surface
        stock_txt_surf = self.font_stocks.render(f"{stock_name}:{stock_price}", False, WHITE)
        stock_txt_rect = stock_txt_surf.get_rect()
        stock_txt_rect.midtop = (self.width / 2, 1)
        self.screen.blit(stock_txt_surf, stock_txt_rect)

        # Specific to sim
        picture = pygame.transform.scale(self.screen, (self.width * self.scaler, self.height * self.scaler))
        self.out_screen.blit(picture, (0, 0))
        pygame.display.flip()
        pygame.event.pump()

    def clear_image(self):
        self.screen.fill(BLACK)
