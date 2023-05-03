from PyQt6.QtWidgets import QApplication
from View import MainWindow
from Model import Model

class Controller:
    def __init__(self):
        self.app = QApplication([])
        self.model = Model()
        self.view = MainWindow()
        self.view.show()

    def run(self):
        self.app.exec()

if __name__ == '__main__':
    # Create and run controller
    controller = Controller()
    controller.run()