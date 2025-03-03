import eel
import os
from route import get_weather

# Получаем абсолютный путь к директории static
current_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(os.path.dirname(current_dir), 'static')
eel.init(static_path)

if __name__ == '__main__':
    try:
        eel.start('first.html', mode="chrome", port=8081)
    except:
        try:
            eel.start('first.html', mode="default", port=9090)
        except:
            eel.start('first.html', 
                     port=9090,
                     host="localhost",
                     size=(1920, 1080),
                     block=True)