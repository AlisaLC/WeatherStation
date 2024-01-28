from django.db import models

# Create your models here.
class Temperature(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Humidity(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class AudioNoise(models.Model):
    value = models.BooleanField() # True = noise, False = no noise
    timestamp = models.DateTimeField(auto_now_add=True)

class Light(models.Model):
    value = models.BooleanField() # True = light, False = no light
    timestamp = models.DateTimeField(auto_now_add=True)

class AirPollution(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)