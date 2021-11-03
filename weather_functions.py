import requests
import urllib.request
import json
from io import BytesIO
from PIL import Image


class weatherAPI():
    def __init__(self, city_name):
        self.KEY = '886705b4c1182eb1c69f28eb8c520e20'
        self.city_name = city_name
        self.temp = 0
        self.icon_name = ''
        self.data = 0

    def get_temp(self):  # Function pulls tract number from census website given lat/lon.
        string = 'https://api.openweathermap.org/data/2.5/weather?q=' + self.city_name + '&appid=' + self.KEY + "&units=imperial"
        print(string)

        response = urllib.request.urlopen(string)
        self.data = json.load(response)
        self.temp = self.data['main']['temp']
        self.icon_name = self.data['weather'][0]['icon']
        return round(self.temp)

    def get_icon_image(self):
        url = "http://openweathermap.org/img/wn/" + self.icon_name + "@2x.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img



if __name__ == "__main__":
    weather = weatherAPI('Philadelphia')
    temp = weather.get_temp()
    print(temp)
    img = weather.get_icon_image()
    img.show()


