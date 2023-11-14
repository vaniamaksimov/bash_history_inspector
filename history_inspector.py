from app.application import Application

if __name__ == '__main__':
    with Application() as app:
        app.start()
