from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import telebot
from telebot import apihelper

import requests
import plotly.express as px

from monitoring.models import LinearRegression

import timezone

from sensor.models import Temperature, Humidity, AudioNoise, Light, AirPollution, Location

class Command(BaseCommand):
    help = "Run the bot"

    def handle(self, *args, **kwargs):
        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
        apihelper.proxy = {
            'http', f'socks5://{settings.SOCKS5_IP}:{settings.SOCKS5_PORT}',
            'https', f'socks5://{settings.SOCKS5_IP}:{settings.SOCKS5_PORT}',
        }

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
                f"""
                Latest temperature: {latest_temperature.value}°C
                Latest humidity: {latest_humidity.value}%
                Latest audio noise: {'Yes' if latest_audio_noise.value else 'No'}
                Latest light: {'Yes' if latest_light.value else 'No'}
                Latest air pollution: {'Yes' if latest_air_pollution.value else 'No'}
                Latest location: {latest_location.latitude}, {latest_location.longitude}
                """)
        
        def plot(Model):
            temperatures = Model.objects.filter(timestamp__gte=timezone.now()-timezone.timedelta(days=7))
            timestamps = [temperature.timestamp for temperature in temperatures]
            values = [temperature.value for temperature in temperatures]
            model = LinearRegression()
            model.fit([[i] for i in range(len(timestamps))], values)
            prediction = model.predict([[len(timestamps)]])
            fig = px.line(x=timestamps, y=values, labels={"x": "Time", "y": "Value"}, title=Model.__name__)
            fig.add_scatter(x=[timestamps[-1], timestamps[-1]+timezone.timedelta(days=1)], y=[values[-1], prediction[0]], mode="lines", name="Prediction")
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
        
        @bot.message_handler(commands=["weather"])
        def weather(message):
            location = Location.objects.latest("timestamp")
            r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,soil_temperature_0cm,soil_moisture_0_to_1cm&timezone=GMT&past_days=7&forecast_days=1')
            data = r.json()
            timestamps = data["hourly"]["time"]
            temperature = data["hourly"]["temperature_2m"]
            humidity = data["hourly"]["relative_humidity_2m"]
            wind_speed = data["hourly"]["wind_speed_10m"]
            soil_temperature = data["hourly"]["soil_temperature_0cm"]
            soil_moisture = data["hourly"]["soil_moisture_0_to_1cm"]
            fig = px.line(x=timestamps, y=[temperature, humidity, wind_speed, soil_temperature, soil_moisture], labels={"x": "Time", "y": "Value"}, title="Weather forecast")
            fig.write_image("weather.png")
            bot.send_photo(message.chat.id, open("weather.png", "rb"))

        bot.polling()