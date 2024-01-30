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
    if std1 == 0 or std2 == 0:
        return 0
    return np.log(std2 / std1) + (std1 ** 2 + (mean1 - mean2) ** 2) / (2 * std2 ** 2) - 0.5

def air_status(img):
    KL_red_clear = KL_divergence(190, 30, img[:, :, 0].mean(), img[:, :, 0].std())
    KL_green_clear = KL_divergence(206, 22, img[:, :, 1].mean(), img[:, :, 1].std())
    KL_blue_clear = KL_divergence(214, 17, img[:, :, 2].mean(), img[:, :, 2].std())
    KL_red_polluted = KL_divergence(173, 14, img[:, :, 0].mean(), img[:, :, 0].std())
    KL_green_polluted = KL_divergence(161, 14, img[:, :, 1].mean(), img[:, :, 1].std())
    KL_blue_polluted = KL_divergence(153, 13, img[:, :, 2].mean(), img[:, :, 2].std())
    KL_mean_clear = (KL_red_clear + KL_green_clear + KL_blue_clear) / 3
    KL_mean_polluted = (KL_red_polluted + KL_green_polluted + KL_blue_polluted) / 3
    if KL_mean_clear > KL_mean_polluted:
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
                AirPollution.objects.create(polluted=polluted)
            except Exception as e:
                logger.error(e)
            time.sleep(settings.CAMERA_INTERVAL)