import eel
from api import index, get_month_forecast, get_full_forecast, get_details_forecast, get_weather_by_coords, get_coordinates
from baggage import get_luggage_list  
import smtplib
from email.mime.text import MIMEText

@eel.expose
def get_weather(city):
    """
    Получает данные о погоде для указанного города и возвращает их для веб-интерфейса.
    
    Args:
        city (str): Название города
        
    Returns:
        dict: Данные о погоде, включая текущую погоду и прогноз
    """
    return get_full_forecast(city)

@eel.expose
def get_month_forecast(city):
    return get_month_forecast(city)

@eel.expose
def get_detailed_weather(city):
    """
    Получает детальный прогноз погоды на разное время суток.
    
    Args:
        city (str): Название города
        
    Returns:
        dict: Прогноз на утро, день и вечер
    """
    return get_details_forecast(city)

@eel.expose
def get_weather_coords(lat, lon):
    """
    Получает погоду по координатам.
    
    Args:
        lat (float): Широта
        lon (float): Долгота
        
    Returns:
        dict: Данные о погоде для указанных координат
    """
    return get_weather_by_coords(lat, lon)

@eel.expose
def get_luggage(city):
    return get_luggage_list(city)

@eel.expose
def get_coords(city):
    """
    Получает координаты города по названию.
    
    Args:
        city (str): Название города
        
    Returns:
        dict: Координаты города (широта и долгота)
    """
    return get_coordinates(city)

@eel.expose
def send_contact_email(name, email, subject, message):
    SMTP_SERVER = "smtp.example.com"         # замените на адрес вашего SMTP-сервера
    SMTP_PORT = 587                          # либо другой порт SMTP-сервера
    SMTP_USER = "your_email@example.com"     # логин вашей почты
    SMTP_PASSWORD = "your_password"          # пароль или API-ключ почты
    to_email = "destination@example.com"     # куда отправлять письма

    body = f"Имя: {name}\nEmail: {email}\nТема: {subject}\nСообщение:\n{message}"
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except Exception as e:
        return {"status": "error", "message": f"Ошибка отправки: {e}"}