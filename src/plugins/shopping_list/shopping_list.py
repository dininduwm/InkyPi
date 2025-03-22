from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image
import os
import requests
import logging
from datetime import datetime, timezone
import pytz
from io import BytesIO
import paho.mqtt.client as mqtt
import json

logger = logging.getLogger(__name__)

# MQTT topics
shopping_list_topic = "homeassistant/shopping_list"
inventory_list_topic = "homeassistant/inventory_list"

shopping_list_global = []
inventory_list_global = []

class ShoppingList(BasePlugin):
    def generate_image(self, settings, device_config):

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        template_params = {}

        mqtt_user       = device_config.load_env_key("MQTT_USER")
        mqtt_password   = device_config.load_env_key("MQTT_PASSWORD")
        mqtt_broker     = device_config.load_env_key("MQTT_BROKER")
        mqtt_port       = int(device_config.load_env_key("MQTT_PORT"))
        self.fetch_data(mqtt_broker, mqtt_port, mqtt_user, mqtt_password)

        template_params['shopping_list']   = shopping_list_global
        template_params['inventory_list']  = inventory_list_global
        template_params["plugin_settings"] = settings
        
        image = self.render_image(dimensions, "shopping_list.html", "shopping_list.css", template_params)
        return image

    def fetch_data(self, mqtt_broker, mqtt_port, mqtt_user, mqtt_password):
        # Callback when the MQTT client receives a message
        def on_message(client, userdata, msg):
            global shopping_list_global, inventory_list_global
            print(f"Received message on {msg.topic}: {msg.payload.decode()}")
            try:
                data = json.loads(msg.payload.decode().replace("'", '"'))
                if msg.topic == shopping_list_topic:
                    shopping_list_global = [item['summary'] for item in data]
                else:
                    inventory_list_global = [item['summary'] for item in data]
            except json.JSONDecodeError:
                print("Failed to decode message into JSON.")

        # Callback for when the client connects to the MQTT broker
        def on_connect(client, userdata, flags, rc):
            print(f"Connected to MQTT broker")
            # Subscribe to the shopping list topic to get updates
            client.subscribe(shopping_list_topic)
            client.subscribe(inventory_list_topic)

        # Initialize the MQTT client
        client = mqtt.Client()

        # Set username and password if required for authentication
        client.username_pw_set(mqtt_user, mqtt_password)

        # Set callback functions
        client.on_connect = on_connect
        client.on_message = on_message

        # Connect to the MQTT broker
        client.connect(mqtt_broker, mqtt_port, 60)

        # Loop to process incoming MQTT messages
        client.loop_start()

        # Wait a bit to receive messages
        import time
        time.sleep(2)

        # Stop the MQTT loop after some time
        client.loop_stop()
