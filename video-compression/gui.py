import sys
import os
import test6
from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog,QLineEdit,QFormLayout,QWidget, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QSlider
import subprocess


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = ''
        self.setWindowTitle("Motion Tracker")

        # File
        self.formInitialized = False
        self.filebutton = QPushButton("Select File")
        self.filebutton.clicked.connect(self.getfile)
        self.Form = QFormLayout()



        self.view = QQuickWidget()
        self.view.setSource(QUrl.fromLocalFile('media.qml'))

        self.Form.addRow(self.filebutton)

        self.setLayout(self.Form) 

    def getfile(self):
        #TODO REMOVE SELECT FILE BTTON
        self.filename = QFileDialog.getOpenFileUrl(self, 'Open file')
        self.initializeForm()
        self.formInitialized = True

    

    def initializeForm(self):
        if self.formInitialized:
            return
        self.submissionbutton = QPushButton('Submit')
        #self.submissionbutton.clicked.connect(self.processVideo)


        frame_width, frame_height, fps  = test6.getVideoBounds(self.filename[0].path())

        print(frame_width)
        print(frame_height)
        print(fps)
        self.rescaleRatio = QLineEdit()
        self.outputfps = QSpinBox()
        self.firstRow = QHBoxLayout()

        self.firstRow.addWidget(QLabel("Rescale Ratio: "))
        self.firstRow.addWidget(self.rescaleRatio)
        self.firstRow.addWidget(QLabel("Output FPS:"))
        self.outputfps.setValue(int(fps))
        self.outputfps.setMaximum(int(fps))
        self.firstRow.addWidget(self.outputfps)
        self.Form.addRow(self.firstRow)


        self.secondRow = QHBoxLayout()
        self.thirdRow = QHBoxLayout()


        self.secondRow.addWidget(QLabel("Height Lower Bound:"))
        self.y = QSpinBox()
        self.secondRow.addWidget(self.y)

        self.secondRow.addWidget(QLabel("Height Upper Bound:"))
        self.height = QSpinBox()
        self.height.setMaximum(frame_height)
        self.height.setValue(frame_height)
        self.secondRow.addWidget(self.height)

        self.thirdRow.addWidget(QLabel("Width Lower bound:"))
        self.x = QSpinBox()
        self.thirdRow.addWidget(self.x)

        self.thirdRow.addWidget(QLabel("Width Upper Bound:"))
        self.width = QSpinBox()
        self.width.setMaximum(frame_width)
        self.width.setValue(frame_width)
        self.thirdRow.addWidget(self.width)



        self.Form.addRow(self.secondRow)
        self.Form.addRow(self.thirdRow)
        self.Form.addRow(self.view)
        player = self.view.rootObject().findChild(QMediaPlayer, "player")
        player.setProperty('source', self.filename[0].path())
        player.play()

        self.Form.addRow(self.submissionbutton)



    def processVideo(self):
        test6.processVideo()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()