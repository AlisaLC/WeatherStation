from django.contrib import admin

# Register your models here.
from sensor.models import Temperature, Humidity, AudioNoise, Light, AirPollution, Location

admin.site.register(Temperature)
admin.site.register(Humidity)
admin.site.register(AudioNoise)
admin.site.register(Light)
admin.site.register(AirPollution)
admin.site.register(Location)