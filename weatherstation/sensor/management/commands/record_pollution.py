from io import BytesIO
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from PIL import Image
import numpy as np

from sensor.models import AirPollution

import time
import logging

import requests

logger = logging.getLogger(__name__)

def KL_divergence(mean1, std1, mean2, std2):
    return np.log(std2 / std1) + (std1 ** 2 + (mean1 - mean2) ** 2) / (2 * std2 ** 2) - 0.5

def JS_divergence(mean1, std1, mean2, std2):
    return 0.5 * (KL_divergence(mean1, std1, mean2, std2) + KL_divergence(mean2, std2, mean1, std1))

def air_status(img):
    KL_blue_clear = JS_divergence(200, 17, img[:, :, 2].mean(), img[:, :, 2].std())
    KL_blue_polluted = JS_divergence(153, 13, img[:, :, 2].mean(), img[:, :, 2].std())
    if KL_blue_clear > KL_blue_polluted:
        return True
    else:
        return False

class Command(BaseCommand):
    help = "Record Air Pollution sensor data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        while True:
            try:
                response = requests.get(settings.CAMERA_URL)
                img = np.array(Image.open(BytesIO(response.content)))
                polluted = air_status(img)
                logger.info(f"Air Pollution: {polluted}")
                AirPollution.objects.create(value=polluted)
            except Exception as e:
                logger.error(e)
            time.sleep(settings.CAMERA_INTERVAL)