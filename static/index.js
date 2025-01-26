window.addEventListener('load', () => {
    if (!navigator.geolocation) {
        updateWeatherCard({"error": "Геолокация не поддерживается вашим браузером"});
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async (pos) => {
            try {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const data = await eel.get_weather_from_coords(lat, lon)();
                updateWeatherCard(data);
                if (data.city) {
                    const details = await eel.get_details("Москва")(); // используем дефолтный город для деталей
                    updateDayForecast(details);
                }
            } catch (error) {
                updateWeatherCard({"error": "Ошибка при получении погоды"});
            }
        },
        (error) => {
            let message = "Ошибка при определении местоположения";
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    message = "Пожалуйста, разрешите доступ к геолокации";
                    break;
                case error.POSITION_UNAVAILABLE:
                    message = "Информация о местоположении недоступна";
                    break;
                case error.TIMEOUT:
                    message = "Истекло время ожидания определения местоположения";
                    break;
            }
            updateWeatherCard({"error": message});
        },
        {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        }
    );
});

function updateWeatherCard(data) {
    document.getElementById('weatherCity').innerText = data.city || data.error || "";
    const iconElem = document.getElementById('weatherIcon');
    if (data.icon) {
        iconElem.src = `http://openweathermap.org/img/wn/${data.icon}@2x.png`;
        iconElem.style.display = 'block';
    } else {
        iconElem.style.display = 'none';
    }
    document.getElementById('weatherDescription').innerText = data.description || "";
    document.getElementById('weatherTemperature').innerText = data.temperature || "";
    document.getElementById('weatherWind').innerText = data.wind || "";
    document.getElementById('weatherHumidity').innerText = data.humidity || "";
}

function updateDayForecast(data) {
    if (data.error) return;
    document.getElementById('morningTemp').innerText = `Утро: ${data.morning}`;
    document.getElementById('dayTemp').innerText = `День: ${data.day}`;
    document.getElementById('eveningTemp').innerText = `Вечер: ${data.evening}`;
}

document.getElementById('weatherForm')?.addEventListener('submit', async function(event) {
    event.preventDefault();
    const city = document.getElementById('city').value;
    const data = await eel.get_weather(city)();
    updateWeatherCard(data);
    const details = await eel.get_details(city)();
    updateDayForecast(details);
    await updateMonthForecast(city);
});

async function updateMonthForecast(city) {
    const data = await eel.get_month_forecast(city)();
    const contentDiv = document.getElementById('monthForecastContent');
    if (data.error) {
        contentDiv.innerHTML = `<p class="error">${data.error}</p>`;
        return;
    }
    contentDiv.innerHTML = data.forecasts
        .map(forecast => `<p>${forecast}</p>`)
        .join('');
}

document.getElementById('showMonthForecast')?.addEventListener('click', async () => {
    const city = document.getElementById('weatherCity').innerText;
    if (!city || city === "Моё местоположение") {
        alert("Пожалуйста, сначала выберите город");
        return;
    }
    document.getElementById('weatherCard').style.display = 'none';
    document.getElementById('monthForecast').style.display = 'block';
    await updateMonthForecast(city);
});

document.getElementById('backToWeather')?.addEventListener('click', () => {
    document.getElementById('monthForecast').style.display = 'none';
    document.getElementById('weatherCard').style.display = 'block';
});