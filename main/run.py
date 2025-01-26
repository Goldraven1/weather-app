import eel
import os
from route import get_weather

eel.init('Davidov/static')

if __name__ == '__main__':
    try:
        eel.start('first.html', mode="chrome", port=8080)
    except:
        try:
            eel.start('first.html', mode="default", port=8080)
        except:
            eel.start('first.html', 
                     mode=None,
                     port=8080,
                     host="localhost",
                     size=(1920, 1080),
                     block=True)