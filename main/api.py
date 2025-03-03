import requests
from datetime import datetime
import locale
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
import math

def index(city_name):
    """
    Получает текущую погоду для указанного города.
    
    Args:
        city_name (str): Название города
        
    Returns:
        dict: Информация о текущей погоде
    """
    API_KEY = '8da0d3e0f6e59a5e5c7430ce18b874c1'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url).json()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%A, %d %B %Y, %H:%M:%S")
    city_weather_update = {
        'city': city_name,
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
        'temperature': 'Температура: ' + str(response['main']['temp']) + ' °C',
        'country_code': response['sys']['country'],
        'wind': 'Ветер: ' + str(response['wind']['speed']) + ' км/ч',
        'humidity': 'Влажность: ' + str(response['main']['humidity']) + '%',
        'time': formatted_time
    }
    return city_weather_update

def get_month_forecast(city_name):
    """
    Получает прогноз погоды на 5 дней (максимум для бесплатного API).
    
    Args:
        city_name (str): Название города
        
    Returns:
        dict: Прогноз погоды по дням или сообщение об ошибке
    """
    API_KEY = '8da0d3e0f6e59a5e5c7430ce18b874c1'
    try:
        # Получаем координаты
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
        response_geo = requests.get(geocode_url).json()
        
        if not response_geo:
            return {"error": "Город не найден"}
            
        lat, lon = response_geo[0]['lat'], response_geo[0]['lon']
        
        # Получаем прогноз на 5 дней (максимум бесплатного API)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&lang=ru&appid={API_KEY}"
        forecast_response = requests.get(forecast_url).json()
        
        if 'list' not in forecast_response:
            return {"error": "Не удалось получить прогноз"}
            
        # Группируем прогнозы по дням
        daily_forecasts = {}
        for forecast in forecast_response['list']:
            date = forecast['dt_txt'].split()[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    'temp': forecast['main']['temp'],
                    'description': forecast['weather'][0]['description']
                }
        
        result = []
        for date, forecast in daily_forecasts.items():
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            result.append(f"{formatted_date}: {math.floor(forecast['temp'])}°C, {forecast['description']}")
        
        return {"forecasts": result}
        
    except Exception as e:
        return {"error": f"Ошибка: {str(e)}"}

def get_full_forecast(city_name):
    """
    Получает полный прогноз погоды, включая текущую погоду и прогноз на 5 дней.
    
    Args:
        city_name (str): Название города
        
    Returns:
        dict: Полный прогноз погоды
    """
    day_forecast = index(city_name)
    month_forecast = get_month_forecast(city_name)
    return {
        "day": day_forecast,
        "month": month_forecast
    }

def get_details_forecast(city_name):
    """
    Получает детальный прогноз погоды на день с разбивкой по времени суток.
    
    Args:
        city_name (str): Название города
        
    Returns:
        dict: Прогноз погоды для утра, дня и вечера или сообщение об ошибке
    """
    API_KEY = '8da0d3e0f6e59a5e5c7430ce18b874c1'
    try:
        # Получаем координаты
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
        response_geo = requests.get(geocode_url).json()
        
        if not response_geo:
            return {"error": "Город не найден"}
            
        lat, lon = response_geo[0]['lat'], response_geo[0]['lon']
        
        
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&lang=ru&appid={API_KEY}"
        forecast_response = requests.get(forecast_url).json()
        
        if 'list' not in forecast_response:
            return {"error": "Не удалось получить прогноз"}
            
        
        forecasts = forecast_response['list'][:8]  
        morning = next((f for f in forecasts if '09:00' in f['dt_txt']), forecasts[0])
        day = next((f for f in forecasts if '15:00' in f['dt_txt']), forecasts[1])
        evening = next((f for f in forecasts if '21:00' in f['dt_txt']), forecasts[2])
        
        return {
            "morning": f"{math.floor(morning['main']['temp'])}°C, {morning['weather'][0]['description']}",
            "day": f"{math.floor(day['main']['temp'])}°C, {day['weather'][0]['description']}",
            "evening": f"{math.floor(evening['main']['temp'])}°C, {evening['weather'][0]['description']}"
        }
        
    except Exception as e:
        return {"error": f"Ошибка: {str(e)}"}

def get_weather_by_coords(lat, lon):
    """
    Получает текущую погоду по географическим координатам.
    
    Args:
        lat (float): Широта
        lon (float): Долгота
        
    Returns:
        dict: Информация о текущей погоде или сообщение об ошибке
    """
    try:
        API_KEY = '8da0d3e0f6e59a5e5c7430ce18b874c1'
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={API_KEY}"
        response = requests.get(url).json()
        
        if 'weather' not in response:
            return {"error": "Не удалось получить данные о погоде"}
            
        current_time = datetime.now()
        formatted_time = current_time.strftime("%A, %d %B %Y, %H:%M:%S")
        
        return {
            "city": "Моё местоположение",
            "description": response['weather'][0]['description'],
            "icon": response['weather'][0]['icon'],
            "temperature": f"Температура: {math.floor(response['main']['temp'])} °C",
            "wind": f"Ветер: {response['wind']['speed']} км/ч",
            "humidity": f"Влажность: {response['main']['humidity']}%",
            "time": formatted_time
        }
    except Exception as e:
        return {"error": f"Ошибка при получении погоды: {str(e)}"}

def get_coordinates(city_name):
    """
    Получает географические координаты для указанного города.
    
    Args:
        city_name (str): Название города
        
    Returns:
        dict: Широта и долгота или сообщение об ошибке
    """
    API_KEY = '8da0d3e0f6e59a5e5c7430ce18b874c1'
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(geocode_url).json()
    if response:
        return {"lat": response[0]['lat'], "lon": response[0]['lon']}
    return {"error": "Город не найден"}