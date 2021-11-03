from PIL import Image, ImageDraw, ImageFont
import pygame
from datetime import datetime

from constants import *

class simDisplay():
    def __init__(self, width, height, scaler=6):
        #pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width * scaler, height * scaler))
        pygame.display.set_caption("Display")
        pygame.font.init()
        self.font = pygame.font.Font(r"C:\Users\ladav\PycharmProjects\led_matrix_spot\PTM55FT.ttf", 16)
        self.background = pygame.surface.Surface((width * scaler, height * scaler))
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
        py_image = pygame.transform.scale(py_image, (self.width * self.scaler, self.height * self.scaler))
        self.screen.blit(py_image, (0, 0))
        pygame.display.flip()

    def display_time(self):
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # Add to pygame surface
        txt_surf = self.font.render(current_time, False, WHITE)
        txt_rect = txt_surf.get_rect()
        txt_rect.center = ((self.width * self.scaler)/2, (self.height * self.scaler)/2)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(txt_surf, txt_rect)
        pygame.display.flip()

    def clear_image(self):
        self.screen.fill(BLACK)
