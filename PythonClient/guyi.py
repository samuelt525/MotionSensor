import sys
import os
from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,QLineEdit,QFormLayout,QWidget
import subprocess
import platform

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = ''
        self.setWindowTitle("My App")
        self.filebutton = QPushButton("Select File")
        self.filebutton.hasFocus()
        self.filebutton.clicked.connect(self.getfile)
        self.submissionbutton = QPushButton('Submit')
        self.submissionbutton.clicked.connect(self.processVideo)
        self.player = 0
        
        self.rescaleRatio = QLineEdit()
        self.outputfps = QLineEdit()
        self.path = QLineEdit()

        self.view = QQuickWidget()
        self.view.setSource(QUrl.fromLocalFile('media.qml'))

        self.flo = QFormLayout()
        self.flo.addRow('rescale ratio', self.rescaleRatio)
        self.flo.addRow('output fps ', self.outputfps)
        self.flo.addRow(self.filebutton)
        self.flo.addRow(self.path)
        self.flo.addRow(self.submissionbutton)
        self.flo.addRow(self.view)


        self.setLayout(self.flo) 

    def getfile(self):
        self.filename = QFileDialog.getOpenFileUrl(self, 'Open file')
        print(self.filename)
        if not self.filename == '':
            if self.rescaleRatio.text() == '':
                print('hello?')
                self.rescaleRatio.setText('50')
            if self.outputfps.text() == '':
                print('hello2?')
                self.outputfps.setText('50')
            self.path.setText(self.filename[0].fileName())
            player = self.view.rootObject().findChild(QMediaPlayer, "player")
            player.setProperty('source', self.filename[0].path())
            player.play()


    def processVideo(self):
        filePath = self.filename[0].path()
        if(platform.system() == 'Windows'):
            filePath = self.filename[0].path()[1::]
        subprocess.Popen([sys.executable, '../video-compression/compression-test1.py', filePath, self.rescaleRatio.text(), self.outputfps.text()], env=os.environ)
app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()