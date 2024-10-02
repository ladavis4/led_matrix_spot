import paho.mqtt.client as mqtt
from utils.constants import *
import json

class SettingMQTT:
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

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_SERVER, MQTT_PORT, 60)
        self.client.loop_start()
        print("MQTT Client Started")

    def update_on(self, value):
        self.on = value

    def update_image(self, value):
        self.show_image = value

    def update_time(self, value):
        self.show_time = value

    def update_calendar(self, value):
        self.show_calendar = value

    def update_spotify(self, value):
        self.show_spotify = value

    def update_brightness(self, value):
        # Value should be an int
        self.brightness = value

    def update_lat(self, value):
        # Value should be a float
        self.lat = value

    def update_long(self, value):
        # Value should be a float
        self.long = value

    def update_city(self, value):
        # Value should be a string
        self.city_name = value

    def on_message(self, client, userdata, msg):
        # This function is the general MQTT callback. If the message is unidentified it
        # will handle the data
        print("An unidentified message was detected")
        print(msg.payload.decode("utf-8"))

    def power_callback(self, client, userdata, msg):
        # Handles power toggle for the LED Screen
        print("A power message was received")
        print(msg.payload.decode("utf-8"))
        self.on = msg.payload.decode("utf-8") == 'ON'

    def bright_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        print("A brightness message was received")
        print(msg.payload.decode("utf-8"))
        self.brightness = msg.payload.decode("utf-8")

    def picture_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        print("A picture message was received")
        print(msg.payload.decode("utf-8"))
        self.show_image= msg.payload.decode("utf-8") == 'ON'

    def weather_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        print("A weather message was received")
        print(msg.payload.decode("utf-8"))
        self.show_time = msg.payload.decode("utf-8") == 'ON'

    def calendar_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        print("A calendar message was received")
        print(msg.payload.decode("utf-8"))
        self.show_calendar = msg.payload.decode("utf-8") == 'ON'

    def spotify_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        print("A spotify message was received")
        print(msg.payload.decode("utf-8"))
        self.show_spotify = msg.payload.decode("utf-8") == 'ON'

    def on_message(self, client, userdata, msg):
        # This function is the general MQTT callback. If the message is unidentified it
        # will handle the data
        print("An unidentified message was detected")
        print(msg.payload.decode("utf-8"))

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("oki/screen/#")

        # Discovery JSONs
        # Discovery JSON
        power_json = {
            "name": "power",
            "unique_id": "ledscreen_power",
            "command_topic": "oki/screen/power/set",
            "optimistic": "true",
            "device": {
                "name": "RPi LED Device",
                "identifiers": "ledscreen",
                "manufacturer": "Lenny Davis",
                "model": "Raspberry Pi 4B",
            }
        }
        bright_json = {
            "name": "brightness",
            "unique_id": "ledscreen_brightness",
            "command_topic": "oki/screen/bright/set",
            "mode": "slider",
            "device": {
                "name": "RPi LED Device",
                "identifiers": "ledscreen"
            }
        }
        picture_json = {
            "name": "pictures_sw",
            "unique_id": "ledscreen_picture_sw",
            "command_topic": "oki/screen/pic/set",
            "device": {
                "name": "RPi LED Device",
                "identifiers": "ledscreen"
            }
        }
        weather_json = {
            "name": "weather_sw",
            "unique_id": "ledscreen_weather_sw",
            "command_topic": "oki/screen/weather/set",
            "device": {
                "name": "RPi LED Device",
                "identifiers": "ledscreen"
            }
        }
        calendar_json = {
            "name": "calendar_sw",
            "unique_id": "ledscreen_calendar_sw",
            "command_topic": "oki/screen/cal/set",
            "device": {
                "name": "RPi LED Device",
                "identifiers": "ledscreen"
            }
        }
        spotify_json = {
            "name": "spotify_sw",
            "unique_id": "ledscreen_spotify_sw",
            "command_topic": "oki/screen/spot/set",
            "device": {
                "name": "RPi LED Device",
                "identifiers": "ledscreen"
            }
        }

        client.publish("homeassistant/switch/ledscreen_power/config", json.dumps(power_json))
        client.publish("homeassistant/number/ledscreen/config", json.dumps(bright_json))
        client.publish("homeassistant/button/ledscreen_picture_sw/config", json.dumps(picture_json))
        client.publish("homeassistant/switch/ledscreen_weather_sw/config", json.dumps(weather_json))
        client.publish("homeassistant/switch/ledscreen_calednar_sw/config", json.dumps(calendar_json))
        client.publish("homeassistant/switch/ledscreen_spotify_sw/config", json.dumps(spotify_json))

        client.message_callback_add("oki/screen/power/set", self.power_callback)
        client.message_callback_add("oki/screen/bright/set", self.bright_callback)
        client.message_callback_add("oki/screen/pic/set", self.picture_callback)
        client.message_callback_add("oki/screen/cal/set", self.calendar_callback)
        client.message_callback_add("oki/screen/weather/set", self.weather_callback)
        client.message_callback_add("oki/screen/spot/set", self.spotify_callback)

