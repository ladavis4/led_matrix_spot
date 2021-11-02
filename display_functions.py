from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
import pygame



class Display:
    def __init__(self, width, height):
        self.options = RGBMatrixOptions()
        self.options.rows = width
        self.options.cols = height
        self.options.gpio_slowdown = 4
        self.matrix = RGBMatrix(options=self.options)
        self.image = Image.new("RGB", (width, height))

    def display_image(self, image):
        self.image = image
        self.matrix.SetImage(image, 0, 0)

    def get_image(self):
        return self.image

    def clear_image(self):
        self.matrix.Clear()




if __name__ == "__main__":
    caller = spotifyWrapper()
    img = caller.get_current_img()
    img.show()

