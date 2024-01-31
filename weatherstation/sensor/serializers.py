from rest_framework import serializers

from sensor.models import Temperature, Humidity, AudioNoise, Light, AirPollution, Location

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"

class HumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Humidity
        fields = "__all__"

class AudioNoiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioNoise
        fields = "__all__"

class LightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Light
        fields = "__all__"

class AirPollutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirPollution
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"