from django.shortcuts import render
from rest_framework.generics import ListAPIView
from django.utils import timezone

# Create your views here.
from sensor.models import Temperature, Humidity, AudioNoise, Light, AirPollution, Location
from sensor.serializers import TemperatureSerializer, HumiditySerializer, AudioNoiseSerializer, LightSerializer, AirPollutionSerializer, LocationSerializer

class TemperatureList(ListAPIView):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    def get_queryset(self):
        return Temperature.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))

class HumidityList(ListAPIView):
    queryset = Humidity.objects.all()
    serializer_class = HumiditySerializer

    def get_queryset(self):
        return Humidity.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))

class AudioNoiseList(ListAPIView):
    queryset = AudioNoise.objects.all()
    serializer_class = AudioNoiseSerializer

    def get_queryset(self):
        return AudioNoise.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))

class LightList(ListAPIView):
    queryset = Light.objects.all()
    serializer_class = LightSerializer

    def get_queryset(self):
        return Light.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))

class AirPollutionList(ListAPIView):
    queryset = AirPollution.objects.all()
    serializer_class = AirPollutionSerializer

    def get_queryset(self):
        return AirPollution.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))

class LocationList(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))