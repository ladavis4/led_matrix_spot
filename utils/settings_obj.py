import json

class Settings:
    def __init__(self, on=True, show_image=True, show_time=True, show_calendar=True, show_spotify=True, brightness=100, lat=26.3851, long=127.8569, city_name=''):
        self.on = on
        self.show_image = show_image
        self.show_time = show_time
        self.show_calendar = show_calendar
        self.show_spotify = show_spotify
        self.brightness = brightness
        self.lat = lat
        self.long = long
        self.city_name = city_name

    def write_settings_to_json(self, debug=False):
        """"
        Writes the custom settings object to a dictionary
        """
        settings_dict = {'button_on': self.on, 'button_img': self.show_image, 'button_time': self.show_time,
                         'button_cal': self.show_calendar, 'button_spot': self.show_spotify,
                         'slider_brightness': 100, 'lat': self.lat, 'long':self.long, 'city_name':self.city_name}
        with open('temp/settings.json', 'w') as outfile:
            json.dump(settings_dict, outfile)

        if debug:
            print("Wrote settings to file")

    def read_settings_json(self, debug=False):
        """"
        Writes the custom settings object to a dictionary
        """
        with open('temp/settings.json') as json_file:
            data = json.load(json_file)

        self.on = data['button_on']
        self.show_image = data['button_img']
        self.show_time = data['button_time']
        self.show_calendar = data['button_cal']
        self.show_spotify = data['button_spot']
        self.brightness = data['slider_brightness']
        self.lat = data['lat']
        self.long = data['long']
        self.city_name = data['city_name']

        if debug:
            print(f"Read settings", {data})
