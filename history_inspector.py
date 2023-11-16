from app.application import Application
from app.log_inspector.standart_library_inspector import StandartLibraryInspector

if __name__ == '__main__':
    with Application(log_inspector=StandartLibraryInspector()) as app:
        app.start()
