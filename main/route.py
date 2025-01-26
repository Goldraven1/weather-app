import eel
from api import index, get_month_forecast as month_api, get_details_forecast, get_weather_by_coords

@eel.expose
def get_weather(city):
    weather_data = index(city)
    return weather_data

@eel.expose
def get_month_forecast(city):
    return month_api(city)

@eel.expose
def get_details(city):
    return get_details_forecast(city)

@eel.expose
def get_month_full(city):
    return month_api(city)  # используем существующую функцию get_month_forecast

@eel.expose
def get_weather_from_coords(lat, lon):
    return get_weather_by_coords(lat, lon)