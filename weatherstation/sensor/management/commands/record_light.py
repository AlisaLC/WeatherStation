from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sensor.models import Light

import time
import logging

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Record LDR sensor data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(settings.LDR_PIN, GPIO.IN)

    def handle(self, *args, **options):
        while True:
            if not GPIO.input(settings.LDR_PIN):
                logger.info(f'Light detected')
                Light.objects.create(value=True)
            else:
                logger.info(f'No light detected')
                Light.objects.create(value=False)
            time.sleep(settings.LDR_INTERVAL)