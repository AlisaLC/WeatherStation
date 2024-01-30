from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from sensor.models import Location, Temperature, Humidity

import time
import logging

import pynmea2

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Record DHT sensor data"

    def handle(self, *args, **options):
        with open('/dev/ttyAMA0', 'r') as f:
            while True:
                newdata = f.readline()
                if newdata[0:6] == "$GPRMC":
                    newmsg=pynmea2.parse(newdata)
                    lat=newmsg.latitude
                    lng=newmsg.longitude
                    Location.objects.create(latitude=lat, longitude=lng)
                    logger.info(f'Location: {lat}, {lng}')
                    time.sleep(settings.GPS_INTERVAL)