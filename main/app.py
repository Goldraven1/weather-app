from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from api import (
    index, get_month_forecast, get_full_forecast,
    get_details_forecast, get_weather_by_coords, get_coordinates
)

app = Flask(__name__)

# Метрики Prometheus
REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['method', 'endpoint'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    return response

@app.route('/metrics')
def metrics():
    """Endpoint для сбора метрик Prometheus."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/weather')
def weather():
    """Получение текущей погоды для указанного города."""
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Не указан город"}), 400
    
    return jsonify(index(city))

@app.route('/api/forecast/month')
def forecast_month():
    """Получение прогноза погоды на месяц для указанного города."""
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Не указан город"}), 400
    
    return jsonify(get_month_forecast(city))

@app.route('/api/forecast/full')
def forecast_full():
    """Получение полного прогноза погоды для указанного города."""
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Не указан город"}), 400
    
    return jsonify(get_full_forecast(city))

@app.route('/api/forecast/details')
def forecast_details():
    """Получение детального прогноза погоды для указанного города."""
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Не указан город"}), 400
    
    return jsonify(get_details_forecast(city))

@app.route('/api/weather/coordinates')
def weather_by_coords():
    """Получение погоды по координатам."""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "Не указаны координаты"}), 400
    
    try:
        return jsonify(get_weather_by_coords(float(lat), float(lon)))
    except ValueError:
        return jsonify({"error": "Неверный формат координат"}), 400

@app.route('/api/coordinates')
def coordinates():
    """Получение координат города."""
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Не указан город"}), 400
    
    return jsonify(get_coordinates(city))

@app.route('/health')
def health():
    """Проверка работоспособности сервиса."""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
