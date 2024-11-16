import paho.mqtt.client as mqtt
from utils.constants import *
import json

class SettingMQTT:
    def __init__(self, on=True, show_image=True, show_time=True, show_calendar=True, show_spotify=True, brightness=100, lat=26.3851, long=127.8569, city_name='', debug=False):
        self.on = on
        self.show_image = show_image
        self.show_time = show_time
        self.show_calendar = show_calendar
        self.show_spotify = show_spotify
        self.brightness = brightness
        self.lat = lat
        self.long = long
        self.city_name = city_name
        self.debug = debug

        self.power_topic_state = "oki/screen/power/state"
        self.bright_topic_state = "oki/screen/bright/state"
        self.pic_topic_state = "oki/screen/pic/state"
        self.weather_topic_state = "oki/screen/weather/state"
        self.calendar_topic_state = "oki/screen/cal/state"
        self.spotify_topic_state = "oki/screen/spot/state"

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_SERVER, MQTT_PORT, 60)
        self.client.loop_start()
        print("MQTT Client Started")

    def update_on(self, value):
        self.on = value
        if value:
            self.client.publish(self.power_topic_state, 'ON'.encode("utf-8"))
        else:
            self.client.publish(self.power_topic_state, 'OFF'.encode("utf-8"))

    def update_image(self, value):
        self.show_image = value
        if value:
            self.client.publish(self.pic_topic_state, 'ON'.encode("utf-8"))
        else:
            self.client.publish(self.pic_topic_state, 'OFF'.encode("utf-8"))

    def update_time(self, value):
        self.show_time = value
        if value:
            self.client.publish(self.weather_topic_state, 'ON'.encode("utf-8"))
        else:
            self.client.publish(self.weather_topic_state, 'OFF'.encode("utf-8"))

    def update_calendar(self, value):
        self.show_calendar = value
        if value:
            self.client.publish(self.calendar_topic_state, 'ON'.encode("utf-8"))
        else:
            self.client.publish(self.calendar_topic_state, 'OFF'.encode("utf-8"))

    def update_spotify(self, value):
        self.show_spotify = value
        if value:
            self.client.publish(self.spotify_topic_state, 'ON'.encode("utf-8"))
        else:
            self.client.publish(self.spotify_topic_state, 'OFF'.encode("utf-8"))

    def update_brightness(self, value):
        # Value should be an int
        self.brightness = value
        self.client.publish(self.bright_topic_state, value.encode("utf-8"))

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
        if self.debug:
            print("An unidentified message was detected")
            print(msg.payload.decode("utf-8"))

    def power_callback(self, client, userdata, msg):
        # Handles power toggle for the LED Screen
        if self.debug:
            print("A power message was received")
            print(msg.payload.decode("utf-8"))
        self.on = msg.payload.decode("utf-8") == 'ON'
        self.client.publish(self.power_topic_state, msg.payload)

    def bright_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        if self.debug:
            print("A brightness message was received")
            print(msg.payload.decode("utf-8"))
        self.brightness = msg.payload.decode("utf-8")
        self.client.publish(self.bright_topic_state, msg.payload)

    def picture_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        if self.debug:
            print("A picture message was received")
            print(msg.payload.decode("utf-8"))
        self.show_image= msg.payload.decode("utf-8") == 'ON'
        self.client.publish(self.pic_topic_state, msg.payload)

    def weather_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        if self.debug:
            print("A weather message was received")
            print(msg.payload.decode("utf-8"))
        self.show_time = msg.payload.decode("utf-8") == 'ON'
        self.client.publish(self.weather_topic_state, msg.payload)

    def calendar_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        if self.debug:
            print("A calendar message was received")
            print(msg.payload.decode("utf-8"))
        self.show_calendar = msg.payload.decode("utf-8") == 'ON'
        self.client.publish(self.calendar_topic_state, msg.payload)

    def spotify_callback(self, client, userdata, msg):
        # Handles brightness settings for the LED Screen
        if self.debug:
            print("A spotify message was received")
            print(msg.payload.decode("utf-8"))
        self.show_spotify = msg.payload.decode("utf-8") == 'ON'
        self.client.publish(self.spotify_topic_state, msg.payload)

    def create_and_publish_discovery(self):
        f = open('mqtt_discovery.json')
        data = json.load(f)
        self.client.publish("homeassistant/switch/ledscreen_power/config", json.dumps(data['power_discovery']))
        self.client.publish("homeassistant/number/ledscreen/config", json.dumps(data['brightness_discovery']))
        self.client.publish("homeassistant/switch/ledscreen_picture_sw/config", json.dumps((data['picture_discovery'])))
        self.client.publish("homeassistant/switch/ledscreen_weather_sw/config", json.dumps(data['weather_discovery']))
        self.client.publish("homeassistant/switch/ledscreen_calednar_sw/config", json.dumps(data['calendar_discovery']))
        self.client.publish("homeassistant/switch/ledscreen_spotify_sw/config", json.dumps(data['spotify_discovery']))
        f.close()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("oki/screen/#")

        client.message_callback_add("oki/screen/power/set", self.power_callback)
        client.message_callback_add("oki/screen/bright/set", self.bright_callback)
        client.message_callback_add("oki/screen/pic/set", self.picture_callback)
        client.message_callback_add("oki/screen/cal/set", self.calendar_callback)
        client.message_callback_add("oki/screen/weather/set", self.weather_callback)
        client.message_callback_add("oki/screen/spot/set", self.spotify_callback)


        self.create_and_publish_discovery()

        self.client.publish(self.power_topic_state, get_state_string(self.on))
        self.client.publish(self.bright_topic_state, get_number_string(self.brightness))
        self.client.publish(self.pic_topic_state, get_state_string(self.show_image))
        self.client.publish(self.weather_topic_state, get_state_string(self.show_time))
        self.client.publish(self.calendar_topic_state, get_state_string(self.show_calendar))
        self.client.publish(self.spotify_topic_state, get_state_string(self.show_spotify))


def get_state_string(state):
    if state:
        return "ON".encode("utf-8")
    else:
        return "OFF".encode("utf-8")

def get_number_string(number):
    return str(number).encode("utf-8")
