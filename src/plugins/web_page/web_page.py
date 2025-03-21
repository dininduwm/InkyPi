from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image
import os
import requests
import logging
from datetime import datetime, timezone
import pytz
from io import BytesIO
from utils.image_utils import take_screenshot_web_page

logger = logging.getLogger(__name__)

WEB_PAGE_URL = "https://google.com"

class WebPage(BasePlugin):
    def generate_image(self, settings, device_config):

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        image = take_screenshot_web_page(WEB_PAGE_URL, dimensions)
        return image