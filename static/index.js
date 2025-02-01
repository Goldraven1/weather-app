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
        // Используем HTTPS для загрузки иконки
        iconElem.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
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

document.getElementById('getBaggage')?.addEventListener('click', async () => {
    const city = document.getElementById('weatherCity').innerText;
    if (!city) {
        alert("Сначала укажите город");
        return;
    }
    try {
        const data = await eel.get_luggage(city)();
        const luggageDiv = document.getElementById('luggageContent');
        luggageDiv.innerHTML = data.luggage
            .map(item => `<p>${item}</p>`)
            .join('');
        document.getElementById('luggageList').style.display = 'block';
    } catch (error) {
        alert("Ошибка формирования списка багажа");
    }
});

document.getElementById('hideBaggage')?.addEventListener('click', () => {
    document.getElementById('luggageList').style.display = 'none';
});

// Функция для отображения нужного раздела и скрытия остальных
function showSection(sectionId) {
    const sections = ['homeSection', 'tripPlanning', 'baggageSection', 'destinations', 'travelTips', 'contacts'];
    sections.forEach(id => {
        document.getElementById(id).style.display = (id === sectionId) ? 'block' : 'none';
    });
}

// Функция для установки активного класса у навигационных табов
function setActiveNav(activeId) {
    const navItems = document.querySelectorAll('.nav-tab');
    navItems.forEach(item => {
        if (item.id === activeId) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

// Добавляем обработчики клика для навигационных элементов
document.getElementById('navHome')?.addEventListener('click', () => {
    setActiveNav('navHome');
    showSection('homeSection');
});
document.getElementById('navTrip')?.addEventListener('click', () => {
    setActiveNav('navTrip');
    showSection('tripPlanning');
});
document.getElementById('navBaggage')?.addEventListener('click', () => {
    setActiveNav('navBaggage');
    showSection('baggageSection');
});
document.getElementById('navDestinations')?.addEventListener('click', () => {
    setActiveNav('navDestinations');
    showSection('destinations');
});
document.getElementById('navTips')?.addEventListener('click', () => {
    setActiveNav('navTips');
    showSection('travelTips');
});
document.getElementById('navContacts')?.addEventListener('click', () => {
    setActiveNav('navContacts');
    showSection('contacts');
});

// Функция для расчёта расстояния (в км) по формуле гаверсина
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Радиус Земли в км
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Обработка формы планирования маршрута с расчетом расстояния и выбором транспорта
document.getElementById('tripForm')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const origin = document.getElementById('origin').value.trim();
    const destination = document.getElementById('destination').value.trim();
    const date = document.getElementById('tripDate').value;
    if (!(origin && destination && date)) {
        alert("Заполните все поля для расчёта маршрута.");
        return;
    }
    try {
        const originCoords = await eel.get_coordinates(origin)();
        const destCoords = await eel.get_coordinates(destination)();
        if(originCoords.error || destCoords.error) {
            throw new Error(originCoords.error || destCoords.error);
        }
        const distance = calculateDistance(originCoords.lat, originCoords.lon, destCoords.lat, destCoords.lon);
        let transport = "";
        let ticketLink = "";
        if (distance < 300) {
            transport = "такси";
            ticketLink = '<a href="https://taxi.ru" target="_blank">Заказать такси</a>';
        } else if (distance < 1500) {
            transport = "поезд";
            ticketLink = '<a href="https://www.rzd.ru" target="_blank">Купить билет на поезд</a>';
        } else {
            transport = "авиаперелет";
            ticketLink = '<a href="https://www.aviasales.ru" target="_blank">Купить авиабилет</a>';
        }
        const resultText = `Расстояние от ${origin} до ${destination}: ${Math.floor(distance)} км.<br>
        Рекомендуемый вид транспорта – ${transport}.<br>
        ${ticketLink}<br>
        Поездка запланирована на ${new Date(date).toLocaleDateString()}.`;
        document.getElementById('tripResult').innerHTML = resultText;
        document.getElementById('tripResult').classList.add('fade-in');
    } catch (error) {
        alert("Ошибка при расчёте маршрута: " + error.message);
    }
});

// Обработка формы обратной связи с имитацией AJAX-запроса
document.getElementById('contactForm')?.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = document.getElementById('contactName').value.trim();
    const email = document.getElementById('contactEmail').value.trim();
    const subject = document.getElementById('contactSubject').value.trim();
    const message = document.getElementById('contactMessage').value.trim();
    if (name && email && subject && message) {
        eel.send_contact_email(name, email, subject, message)().then(response => {
            document.getElementById('contactFeedback').innerText = response.message;
            document.getElementById('contactFeedback').classList.add('fade-in');
            document.getElementById('contactForm').reset();
        }).catch(error => {
            alert("Ошибка при отправке: " + error);
        });
    } else {
        alert("Пожалуйста, заполните все поля.");
    }
});

// Обработка кнопки обновления багажа с анимацией
document.getElementById('refreshBaggage')?.addEventListener('click', async () => {
    const city = document.getElementById('weatherCity').innerText;
    if (!city) {
        alert("Сначала укажите город на главной странице");
        return;
    }
    try {
        const data = await eel.get_luggage(city)();
        document.getElementById('baggageResult').innerHTML = data.luggage
            .map(item => `<p>${item}</p>`)
            .join('');
        document.getElementById('baggageResult').classList.add('fade-in');
    } catch (error) {
        alert("Ошибка обновления списка багажа");
    }
});