import sys


from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    window = Window()

    engine.rootContext().setContextProperty('window', window)

    engine.load('test.qml')

    sys.exit(app.exec())