from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sensor.models import AudioNoise

import time
import logging

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Record KY038 sensor data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(settings.KY038_PIN, GPIO.IN, pull_up_down = GPIO.PUD_OFF)

    def handle(self, *args, **options):
        while True:
            noise = False
            for i in range(settings.KY038_FREQUENCY):
                if GPIO.input(settings.KY038_PIN):
                    noise = True
                    break
                time.sleep(settings.KY038_INTERVAL / settings.KY038_FREQUENCY)
            if noise:
                AudioNoise.objects.create(value=True)
                logger.info(f'Noise detected')
                time.sleep((settings.KY038_FREQUENCY - i) / settings.KY038_FREQUENCY * settings.KY038_INTERVAL)
            else:
                AudioNoise.objects.create(value=False)
                logger.info(f'No noise detected')