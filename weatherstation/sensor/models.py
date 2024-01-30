from django.db import models

# Create your models here.
class Temperature(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value}°C"

class Humidity(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value}%"

class AudioNoise(models.Model):
    value = models.BooleanField() # True = noise, False = no noise
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Noisy' if self.value else 'Quiet'}"

class Light(models.Model):
    value = models.BooleanField() # True = light, False = no light
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Light' if self.value else 'Dark'}"

class AirPollution(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    value = models.BooleanField() # True = polluted, False = clean
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Polluted' if self.value else 'Clean'}"

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"