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

    def display_image(self, image):
        self.image = image
        self.matrix.SetImage(image, 0, 0)

    def get_image(self):
        return self.image

    def clear_image(self):
        self.matrix.Clear()

    def display_time(self):
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # Add to pygame surface
        txt_surf = self.font.render(current_time, False, WHITE)
        txt_rect = txt_surf.get_rect()
        txt_rect.center = (self.width/2, self.height/2)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(txt_surf, txt_rect)

        self.image = pygame.surfarray.array3d(self.surface)
        self.display_image(self.image)


