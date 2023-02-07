import sys
import os
import tracker
import subprocess
from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QLineEdit, QFormLayout, QWidget, QWidgetItem, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QSlider, QProgressBar
from PyQt6.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.width, self.height = 700, 600
        self.setMinimumSize(self.width, self.height)

        self.filename = ''
        self.setWindowTitle("Motion Tracker")
        # File
        self.formInitialized = False
        self.filebutton = QPushButton("Select File")
        self.filebutton.clicked.connect(self.getfile)
        self.filebutton.setFixedWidth(200)
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.filebutton)
        self.h_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.view = QQuickWidget()
        self.view.setSource(QUrl.fromLocalFile('media.qml'))

        self.Form = QFormLayout()

        self.logo = QLabel()
        pixmap = QPixmap('Logo.png')
        self.logo.setPixmap(pixmap)
        self.Form.addRow(self.logo)
        self.Form.addRow(self.h_layout)
        self.setLayout(self.Form) 

        self.progressBar = QProgressBar()


    def getfile(self):
        self.filename = QFileDialog.getOpenFileUrl(self, 'Open file')
        self.filebutton.hide();
        self.logo.hide()
        self.initializeForm()
        self.formInitialized = True

    

    def initializeForm(self):
        if self.formInitialized:
            return

        self.submissionbutton = QPushButton('Submit')
        self.submissionbutton.clicked.connect(self.processVideo)

        frame_width, frame_height, fps  = tracker.getVideoBounds(self.filename[0].path())

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
        self.userYLB = QSpinBox()
        self.secondRow.addWidget(self.userYLB)

        self.secondRow.addWidget(QLabel("Height Upper Bound:"))
        self.userYUB = QSpinBox()
        self.userYUB.setMaximum(frame_height)
        self.userYUB.setValue(frame_height)
        self.secondRow.addWidget(self.userYUB)

        self.thirdRow.addWidget(QLabel("Width Lower bound:"))
        self.userXLB = QSpinBox()
        self.thirdRow.addWidget(self.userXLB)

        self.thirdRow.addWidget(QLabel("Width Upper Bound:"))
        self.userXUB = QSpinBox()
        self.userXUB.setMaximum(frame_width)
        self.userXUB.setValue(frame_width)
        self.thirdRow.addWidget(self.userXUB)

        self.Form.addRow(self.secondRow)
        self.Form.addRow(self.thirdRow)
        self.Form.addRow(self.view)

        #print(self.view.rootObject().findChild())
        player = self.view.rootObject().findChild(QMediaPlayer, "player")
        player.setProperty('source', self.filename[0].path())
        player.play()

        self.Form.removeWidget(self.filebutton)
        self.Form.addRow(self.submissionbutton)

    def processVideo(self):
        print(self.filename[0].path(), self.outputfps.value(), int(self.rescaleRatio.text()), self.userXLB.value(), self.userXUB.value(), self.userYLB.value(), self.userYUB.value())
        tracker.processVideo(self.filename[0].path(), self.progressBar, self.outputfps.value(), int(self.rescaleRatio.text()), self.userXLB.value(), self.userXUB.value(), self.userYLB.value(), self.userYUB.value())
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()