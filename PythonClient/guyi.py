import sys
import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,QLineEdit,QFormLayout,QWidget
import subprocess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = ''
        self.setWindowTitle("My App")
        self.filebutton = QPushButton("Select File")
        self.filebutton.clicked.connect(self.getfile)
        self.submissionbutton = QPushButton('Submit')
        self.submissionbutton.clicked.connect(self.processVideo)
        
        self.rescaleRatio = QLineEdit()
        self.outputfps = QLineEdit()
        self.path = QLineEdit()

        flo = QFormLayout()
        flo.addRow('rescale ratio', self.rescaleRatio)
        flo.addRow('output fps ', self.outputfps)
        flo.addRow(self.filebutton)
        flo.addRow(self.path)
        flo.addRow(self.submissionbutton)

        self.setLayout(flo) 

    def getfile(self):
        self.filename = QFileDialog.getOpenFileUrl(self, 'Open file')
        if not self.filename == '':
            if self.rescaleRatio.text() == '':
                self.outputfps.setText('50')
            if self.outputfps.text() == '':
                self.outputfps.setText('50')
            self.path.setText(self.filename[0].fileName())
    def processVideo(self):
        subprocess.Popen(['python3', '../video-compression/compression-test1.py', self.filename[0].path(), self.rescaleRatio.text(), self.outputfps.text()], env=os.environ)
app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()