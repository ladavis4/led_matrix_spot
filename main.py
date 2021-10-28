from spotify_functions import spotifyCaller
from PIL import Image, ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

options = RGBMatrixOptions()
options.rows = 64
options.cols= 64
options.gpio_slowdown = 4

matrix = RGBMatrix(options = options)

caller = spotifyCaller()

while(1): 
    image = caller.get_current_img()

    matrix.Clear()
    matrix.SetImage(image, 0, 0)
    time.sleep(10)







