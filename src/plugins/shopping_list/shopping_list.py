from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image
import os
import requests
import logging
from datetime import datetime, timezone
import pytz
from io import BytesIO

logger = logging.getLogger(__name__)

class ShoppingList(BasePlugin):
    def generate_image(self, settings, device_config):

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        template_params = {}
        template_params['shopping_list'] = [
                                                "Spaghetti", "Avocado", "Salmon", "Mango", "Tacos", 
                                                "Oatmeal", "Blueberries", "Chicken wings", "Quinoa", "Zucchini", 
                                                "Almonds", "Eggs", "Brown rice", "Shrimp", "Broccoli"
                                            ]
        template_params['inventory_list'] = [
                                                "Pizza", "Grapes", "Steak", "Cauliflower", "Sweet potato", 
                                                "Cherries", "Cucumber", "Pork chops", "Pancakes", "Carrots", 
                                                "Greek yogurt", "Mushrooms", "Hummus", "Peaches", "Raspberries"
                                            ]
        template_params["plugin_settings"] = settings

        image = self.render_image(dimensions, "shopping_list.html", "shopping_list.css", template_params)
        return image
