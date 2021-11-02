from PIL import Image, ImageDraw
import pygame
import datetime

class simDisplay():
    def __init__(self, width, height, scaler=6):
        self.image = Image.new("RGB", (width, height))
        self.width = width
        self.height = height
        self.scaler = scaler
        pygame.init()
        self.screen = pygame.display.set_mode((width * scaler, height * scaler))
        pygame.display.set_caption("Display")
        self.screen.fill((0,0,0))

    def display_image(self, image):
        mode = image.mode
        size = image.size
        data = image.tobytes()

        py_image = pygame.image.fromstring(data, size, mode)
        py_image = pygame.transform.scale(py_image, (self.width * self.scaler, self.height * self.scaler))
        self.screen.blit(py_image, (0, 0))
        pygame.display.flip()

    def clear_image(self):
        self.screen.fill((0,0,0))