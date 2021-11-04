from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
import pygame
from datetime import datetime
from constants import *


class Display:
    def __init__(self, width, height):
        self.options = RGBMatrixOptions()
        self.options.rows = width
        self.options.cols = height
        self.options.gpio_slowdown = 4
        self.matrix = RGBMatrix(options=self.options)
        self.image = Image.new("RGB", (width, height))

        self.width = width
        self.height = height

        # pygame
        pygame.init()
        self.screen = pygame.surface.Surface((self.width, self.height))
        self.background = pygame.surface.Surface((self.width, self.height))
        self.background.fill(BLACK)
        pygame.font.init()
        self.font = pygame.font.Font("PTM55FT.ttf", 13)
        

    def display_image(self, image):
        self.image = image
        self.matrix.SetImage(image, 0, 0)

    def get_image(self):
        return self.image

    def clear_image(self):
        self.matrix.Clear()

    def display_time_and_weather(self, image, temp):
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # Add to pygame surface
        txt_surf = self.font.render(current_time, False, WHITE)
        txt_rect = txt_surf.get_rect()
        txt_rect.midtop = (self.width/2, 0)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(txt_surf, txt_rect)

        # Add Temperature to surface
        txt_surf = self.font.render(str(temp) + "F", False, WHITE)
        txt_rect = txt_surf.get_rect()
        txt_rect.midbottom = (self.width/ 4, self.height + 3)
        self.screen.blit(txt_surf, txt_rect)

        mode = image.mode
        size = image.size
        data = image.tobytes()

        py_image = pygame.image.fromstring(data, size, mode)
        py_image = pygame.transform.scale(py_image, (32, 32))
        py_rect = py_image.get_rect()
        py_rect.midbottom = (self.width*3/ 4, self.height + 7)
        self.screen.blit(py_image, py_rect)

        self.image = Image.fromarray(pygame.surfarray.pixels3d(self.screen).swapaxes(1, 0))
        self.display_image(self.image)

