import json

import paho.mqtt.client as mqtt
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("oki/lr/ac/mode/set")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + "" + str(msg.payload))


# Define constants
MQTT_SERVER = "192.168.0.95"
MQTT_PORT = 1883
DEVICE_ID = "ledScreen"

# Define MQTT Topics
TOPIC_DISCOVERY = "homeassistant/switch/ledScreen/config"
TOPIC_STATE = "oki/lr/screen/"
TOPIC_COMMAND = "oki/lr/screen/set"
TOPIC_AVAIL = "oki/lr/screen/available"

#Discovery JSON
dict = {
    "name" : "LED Screen",
    "unique_id": "ledScreen",
    "state_topic": TOPIC_STATE,
    "command_topic": TOPIC_COMMAND,
    "payload_on": "ON",
    "payload_off": "OFF",
    "state_on" : "ON",
    "state_off" : "OFF"
}
json_object = json.dumps(dict)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.0.95", 1883, 60)
mqttc.publish(TOPIC_DISCOVERY, json_object)
mqttc.publish(TOPIC_AVAIL, "online")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()