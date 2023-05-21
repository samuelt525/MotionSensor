from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

class Model:
    def __init__(self):
        self._data = ""

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Click me", self)
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        controller.update_model("Button clicked")

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_model(self, data):
        self.model.data = data
        print("Model data updated:", self.model.data)

# Create the QApplication instance before creating any QWidget
app = QApplication([])

# Create the Model, View, and Controller instances
model = Model()
view = View()
controller = Controller(model, view)

# Start the application event loop
view.show()
sys.exit(app.exec())