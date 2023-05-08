from PyQt6.QtWidgets import QApplication
from View import MainWindow
from Model import Model
import os
import sys

documents_dir = ''
if (sys.platform == 'win32'):
    documents_dir = os.getenv('USERPROFILE') + '\Documents'
else:
    documents_dir = os.path.expanduser("~/Documents")

class Controller:
    def __init__(self):
        self.app = QApplication([])
        self.model = Model()
        self.view = MainWindow()
        self.view.widget.setInputPath(self.checkInputPath())
        self.view.show()

        self.view.widget.selectFileSignal.connect(self.setFile)
        self.view.widget.processFileSignal.connect(self.processFile)
        self.view.widget.outputfpsSignal.connect(self.setOutputfps)
        self.view.widget.rescaleRatioSignal.connect(self.setRescaleRatio)

    def checkInputPath(self):
        file_name = "MotionTracker.conf"
        if os.path.exists(os.path.join(documents_dir, file_name)):
            with open(os.path.join(documents_dir, file_name)) as f:
                path = f.readline()
        return path

    def setFile(self):
        self.model.setFileName(self.view.widget.filename)
    def setOutputfps(self, outputfps):
        try:
            outputfps = int(outputfps)
        except ValueError:
            outputfps = 0 
        self.model.setOutputfps(outputfps)
    def setRescaleRatio(self, rescaleRatio):
        try:
            rescaleRatio = int(rescaleRatio)
        except ValueError:
            rescaleRatio = 0 
        self.model.setRescaleRatio(rescaleRatio)
    def processFile(self):
        pass
    def run(self):
        self.app.exec()

if __name__ == '__main__':
    # Create and run controller
    controller = Controller()
    controller.run()