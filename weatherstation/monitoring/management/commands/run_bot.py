from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import telebot
from telebot import apihelper
apihelper.API_URL = settings.TELEGRAM_API_URL
apihelper.FILE_URL = settings.TELEGRAM_FILE_URL

from PIL import Image

import requests
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

from django.utils import timezone
from django.db import models

from sensor.models import Temperature, Humidity, AudioNoise, Light, AirPollution, Location
from notification.models import Email, EmailAttachment

class Command(BaseCommand):
    help = "Run the bot"

    def handle(self, *args, **kwargs):
        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

        @bot.message_handler(commands=["start"])
        def start(message):
            bot.reply_to(message, "Welcome to the weather station bot!")

        @bot.message_handler(commands=["help"])
        def help(message):
            bot.reply_to(message, "This bot will provide you with the latest weather data")

        @bot.message_handler(commands=["latest"])
        def latest(message):
            latest_temperature = Temperature.objects.latest("timestamp")
            latest_humidity = Humidity.objects.latest("timestamp")
            latest_audio_noise = AudioNoise.objects.latest("timestamp")
            latest_light = Light.objects.latest("timestamp")
            latest_air_pollution = AirPollution.objects.latest("timestamp")
            latest_location = Location.objects.latest("timestamp")
            bot.reply_to(
                message, 
                f"""Latest temperature: {latest_temperature.value:.2f}°C
Latest humidity: {latest_humidity.value:.2f}%
Latest audio noise: {'Yes' if latest_audio_noise.value else 'No'}
Latest light: {'Yes' if latest_light.value else 'No'}
Latest air pollution: {'Yes' if latest_air_pollution.value else 'No'}
Latest location: {latest_location.latitude:.5f}, {latest_location.longitude:.5f}""")
            bot.send_location(message.chat.id, latest_location.latitude, latest_location.longitude)
        
        def plot(Model):
            temperatures = Model.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))
            if isinstance(temperatures[0].value, bool):
                values = [1 if temperature.value else 0 for temperature in temperatures]
            else:
                values = [temperature.value for temperature in temperatures]
                values = values[:2] + [sum(values[i-2:i+3])/5 for i in range(2, len(values)-2)] + values[-2:]
            timestamps = [temperature.timestamp for temperature in temperatures]
            model = LinearRegression()
            model.fit([[i] for i in range(len(timestamps))], values)
            prediction = model.predict([[len(timestamps)]])
            fig = go.Figure()
            fig.add_scatter(x=timestamps, y=values, mode="lines", name="Data")
            fig.add_scatter(x=[timestamps[-1], timestamps[-1] + timezone.timedelta(days=1)], y=[values[-1], prediction[0]], mode="lines", name="Prediction")
            fig.write_image("plot.png")
        
        @bot.message_handler(commands=["temperature"])
        def temperature(message):
            plot(Temperature)
            bot.send_photo(message.chat.id, open("plot.png", "rb"))

        @bot.message_handler(commands=["humidity"])
        def humidity(message):
            plot(Humidity)
            bot.send_photo(message.chat.id, open("plot.png", "rb"))

        @bot.message_handler(commands=["audio_noise"])
        def audio_noise(message):
            plot(AudioNoise)
            bot.send_photo(message.chat.id, open("plot.png", "rb"))

        @bot.message_handler(commands=["light"])
        def light(message):
            plot(Light)
            bot.send_photo(message.chat.id, open("plot.png", "rb"))

        @bot.message_handler(commands=["air_pollution"])
        def air_pollution(message):
            plot(AirPollution)
            bot.send_photo(message.chat.id, open("plot.png", "rb"))
            data = AirPollution.objects.latest("timestamp")
            bot.send_photo(message.chat.id, open(data.image.path, "rb"), caption=f"Air pollution: {'Yes' if data.value else 'No'}")
        
        @bot.message_handler(commands=["weather"])
        def weather(message, send_plot=True):
            location = Location.objects.latest("timestamp")
            r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,soil_temperature_0cm,soil_moisture_0_to_1cm&timezone=GMT&past_days=7&forecast_days=1')
            data = r.json()
            timestamps = data["hourly"]["time"]
            temperature = data["hourly"]["temperature_2m"]
            humidity = data["hourly"]["relative_humidity_2m"]
            wind_speed = data["hourly"]["wind_speed_10m"]
            soil_temperature = data["hourly"]["soil_temperature_0cm"]
            soil_moisture = data["hourly"]["soil_moisture_0_to_1cm"]
            fig = go.Figure()
            fig.add_scatter(x=timestamps, y=temperature, mode="lines", name="Temperature")
            fig.add_scatter(x=timestamps, y=humidity, mode="lines", name="Humidity")
            fig.add_scatter(x=timestamps, y=wind_speed, mode="lines", name="Wind speed")
            fig.add_scatter(x=timestamps, y=soil_temperature, mode="lines", name="Soil temperature")
            fig.add_scatter(x=timestamps, y=soil_moisture, mode="lines", name="Soil moisture")
            fig.write_image("weather.png")
            if send_plot:
                bot.send_photo(message.chat.id, open("weather.png", "rb"))
        
        @bot.message_handler(commands=["email"])
        def email(message):
            latest_temperature = Temperature.objects.latest("timestamp")
            mean_temperature = Temperature.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7)).aggregate(models.Avg("value"))["value__avg"]
            latest_humidity = Humidity.objects.latest("timestamp")
            mean_humidity = Humidity.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7)).aggregate(models.Avg("value"))["value__avg"]
            latest_audio_noise = AudioNoise.objects.latest("timestamp")
            latest_light = Light.objects.latest("timestamp")
            latest_air_pollution = AirPollution.objects.latest("timestamp")
            latest_location = Location.objects.latest("timestamp")
            email = Email(
                subject="Weather data",
                recipient=settings.EMAIL_RECIPIENT,
                body=f"""Latest temperature: {latest_temperature.value:.2f}°C
Last Week Mean temperature: {mean_temperature:.2f}°C
Latest humidity: {latest_humidity.value:.2f}%
Last Week Mean humidity: {mean_humidity:.2f}%
Latest audio noise: {'Yes' if latest_audio_noise.value else 'No'}
Latest light: {'Yes' if latest_light.value else 'No'}
Latest air pollution: {'Yes' if latest_air_pollution.value else 'No'}
Latest location: {latest_location.latitude:.5f}, {latest_location.longitude:.5f}""")
            email.save()
            email.send()
            bot.reply_to(message, "Email sent")

        bot.polling()