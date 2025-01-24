import eel


eel.init('static')

if __name__ == '__main__':
    eel.start('first.html', mode="none", size=(1920, 1080), host="localhost", port=8080)