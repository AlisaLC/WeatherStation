from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sensor.models import Temperature, Humidity

import time
import logging

import Adafruit_DHT as dht

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Record DHT sensor data"

    def handle(self, *args, **options):
        while True:
            humidity, temperature = dht.read_retry(dht.DHT22, settings.DHT_PIN)
            if humidity is not None and temperature is not None:
                Temperature.objects.create(value=temperature)
                Humidity.objects.create(value=humidity)
                logger.info(f'Temperature: {temperature} C, Humidity: {humidity} %')
            else:
                logger.warning('Failed to get reading. Try again!')
            time.sleep(settings.DHT_INTERVAL)