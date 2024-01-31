from django.urls import path

from monitoring.views import TemperatureList, HumidityList, AudioNoiseList, LightList, AirPollutionList, LocationList

urlpatterns = [
    path("temperature/", TemperatureList.as_view(), name="temperature-list"),
    path("humidity/", HumidityList.as_view(), name="humidity-list"),
    path("audio_noise/", AudioNoiseList.as_view(), name="audio-noise-list"),
    path("light/", LightList.as_view(), name="light-list"),
    path("air_pollution/", AirPollutionList.as_view(), name="air-pollution-list"),
    path("location/", LocationList.as_view(), name="location-list"),
]