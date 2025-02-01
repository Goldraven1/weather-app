import re
from api import index

def get_luggage_list(city_name):
    weather = index(city_name)
    temperature_text = weather.get("temperature", "")
    description = weather.get("description", "").lower()
    
    # Базовый список вещей
    items = ["Документы", "Зарядное устройство", "Личные вещи"]
    
    # Попытка извлечь числовое значение температуры
    match = re.search(r'(-?\d+)', temperature_text)
    temp = int(match.group(1)) if match else 20
    
    # Расширяем список багажа в зависимости от температуры
    if temp < 0:
        items.extend([
            "Экстремально тёплая куртка",
            "Термобелье",
            "Тёплые штаны",
            "Шапка",
            "Перчатки",
            "Шарф"
        ])
    elif temp < 10:
        items.extend([
            "Тёплая куртка",
            "Свитер",
            "Шапка",
            "Перчатки"
        ])
    elif temp < 20:
        items.extend([
            "Лёгкая куртка или свитер",
            "Джинсы или брюки"
        ])
    elif temp < 30:
        items.extend([
            "Футболка",
            "Лёгкие брюки/шорты"
        ])
    else:
        items.extend([
            "Кепка или шляпа",
            "Солнцезащитные очки",
            "Лёгкая одежда",
            "Бутылка воды"
        ])
    
    # Добавляем аксессуары по описанию погоды
    if "дождь" in description or "ливень" in description:
        items.extend(["Зонт", "Плащ"])
    if "снег" in description:
        items.append("Снежные ботинки")
    if "ветер" in description:
        items.append("Ветрозащитная куртка")
    
    return {"luggage": items}
