import sys
import os
import tracker
import subprocess
import copy
from PyQt6.QtCore import QSize, Qt, QUrl, pyqtSlot, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QLineEdit, QFormLayout, QWidget, QWidgetItem, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QSlider, QProgressBar, QRadioButton
from PyQt6.QtGui import QPixmap

class MainWindow(QWidget):
    # for qml video player resizing with window size; commented out due to segmentation fault error on mac
    resized = pyqtSignal()
    valueChanged = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.filename = ''
        self.setWindowTitle("Motion Tracker")
        # File
        self.formInitialized = False
        self.filebutton = QPushButton("Select File")
        self.filebutton.clicked.connect(self.getfile)
        self.filebutton.setFixedWidth(500)
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.filebutton)
        self.h_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.view = QQuickWidget()
        self.view.rootContext().setContextProperty("guiParent", self)
        self.view.setSource(QUrl.fromLocalFile('media.qml'))

        self.Form = QFormLayout()

        self.logo = QLabel()
        pixmap = QPixmap('Logo.png')
        pixmap = pixmap.scaled(500,160)
        self.logo.setPixmap(pixmap)
        self.Form.addRow(self.logo)
        self.Form.addRow(self.h_layout)
        self.setLayout(self.Form)

        self.progressBar = QProgressBar()

    def getfile(self):
        self.filename = QFileDialog.getOpenFileUrl(self, 'Open file')
        self.filebutton.hide()
        self.logo.hide()
        self.initializeForm()
        self.formInitialized = True

    def initializeForm(self):
        if self.formInitialized:
            return

        self.submissionbutton = QPushButton('Submit')
        self.submissionbutton.clicked.connect(self.processVideo)

        self.frame_width, self.frame_height, fps  = tracker.getVideoBounds(self.filename[0].path())

        self.rescaleRatio = QLineEdit()
        self.outputfps = QSpinBox()
        self.firstRow = QHBoxLayout()

        self.rescaleRatioLabel = QLabel("Rescale Ratio: ")
        self.firstRow.addWidget(self.rescaleRatioLabel)
        self.firstRow.addWidget(self.rescaleRatio)
        self.rescaleRatio.setText("100")
        self.outputfpsLabel = QLabel("Output FPS:")
        self.firstRow.addWidget(self.outputfpsLabel)
        self.outputfps.setValue(int(fps))
        self.outputfps.setMaximum(int(fps))
        self.firstRow.addWidget(self.outputfps)
        self.Form.addRow(self.firstRow)


        self.secondRow = QHBoxLayout()
        self.thirdRow = QHBoxLayout()
        self.fourthRow = QHBoxLayout()


        self.userYLBLabel = QLabel("Height Lower bound:")
        self.secondRow.addWidget(self.userYLBLabel)
        self.userYLB = QSpinBox()
        self.secondRow.addWidget(self.userYLB)
        self.userYLB.valueChanged.connect(self.handleBoundValueChanged)

        self.userYUBLabel = QLabel("Height Upper Bound:")
        self.secondRow.addWidget(self.userYUBLabel)
        self.userYUB = QSpinBox()
        self.userYUB.setMaximum(self.frame_height)
        self.userYUB.setValue(self.frame_height)
        self.userYUB.valueChanged.connect(self.handleBoundValueChanged)
        self.secondRow.addWidget(self.userYUB)

        self.userXLBLabel = QLabel("Width Lower Bound:")
        self.thirdRow.addWidget(self.userXLBLabel)
        self.userXLB = QSpinBox()
        self.userXLB.valueChanged.connect(self.handleBoundValueChanged)
        self.thirdRow.addWidget(self.userXLB)

        self.userXUBLabel = QLabel("Width Upper Bound:")
        self.thirdRow.addWidget(self.userXUBLabel)
        self.userXUB = QSpinBox()
        self.userXUB.setMaximum(self.frame_width)
        self.userXUB.setValue(self.frame_width)
        self.userXUB.valueChanged.connect(self.handleBoundValueChanged)
        self.thirdRow.addWidget(self.userXUB)

        self.directionLabel = QLabel("Racewalker Direction:")
        self.fourthRow.addWidget(self.directionLabel)
        self.directionLeft = QRadioButton("Left")
        self.fourthRow.addWidget(self.directionLeft)
        self.directionLeft.setDown(True)
        self.directionRight = QRadioButton("Right")
        self.fourthRow.addWidget(self.directionRight)
        self.directionUp = QRadioButton("Up")
        self.fourthRow.addWidget(self.directionUp)
        self.directionDown = QRadioButton("Down")
        self.fourthRow.addWidget(self.directionDown)

        self.Form.addRow(self.secondRow)
        self.Form.addRow(self.thirdRow)
        self.Form.addRow(self.fourthRow)
        self.Form.addRow(self.view)

        self.width, self.height = 825, 675
        self.setMinimumSize(self.width, self.height)
        self.resize(self.width, self.height)

        #print(self.view.rootObject().findChild())
        self.player = self.view.rootObject().findChild(QMediaPlayer, "player")
        self.player.setProperty('source', self.filename[0].path())
        self.player.setLoops(self.player.Loops.Infinite)
        self.player.play() 

        self.Form.removeWidget(self.filebutton)
        self.Form.addRow(self.submissionbutton)

    @pyqtSlot(result=QSize)
    def getSize(self):
        return self.size()
    # resizes qml video player with window
    def resizeEvent(self, event):
        self.resized.emit()
        self.setFixedSize(event.size())
        super(MainWindow, self).resizeEvent(event)
    def handleBoundValueChanged(self):
        self.userYLB.setMaximum(self.userYUB.value()-1)
        self.userXLB.setMaximum(self.userXUB.value()-1)
        self.valueChanged.emit()
    @pyqtSlot(result=list)
    def getBounds(self):
        return [self.userYLB.value(), self.userYUB.value(), self.userXLB.value(), self.userXUB.value()]
    @pyqtSlot(result=list)
    def getVideoDimensions(self):
        return [self.frame_width, self.frame_height]

    def processVideo(self):
        self.rescaleRatio.hide()
        self.rescaleRatioLabel.hide()
        self.outputfps.hide()
        self.outputfpsLabel.hide()
        self.userYLB.hide()
        self.userYLBLabel.hide()
        self.userYUB.hide()
        self.userYUBLabel.hide()
        self.userXLB.hide()
        self.userXLBLabel.hide()
        self.userXUB.hide()
        self.userXUBLabel.hide()
        self.view.hide()
        self.submissionbutton.hide()

        self.progressBar.setGeometry(50, 50, 250, 30)
        self.firstRow.addWidget(self.progressBar)
        self.progressLabel = QLabel("Processing video...")
        self.secondRow.addWidget(self.progressLabel)
        self.setMinimumSize(825, 100)
        self.resize(825, 100)
        print(self.filename[0].path(), self.outputfps.value(), int(self.rescaleRatio.text()), self.userXLB.value(), self.userXUB.value(), self.userYLB.value(), self.userYUB.value())
        tracker.processVideo(self.filename[0].path(), self.progressBar, self.outputfps.value(), int(self.rescaleRatio.text()), self.userXLB.value(), self.userXUB.value(), self.userYLB.value(), self.userYUB.value())
        self.close()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()

windowWidth = window.size().width()
windowHeight = window.size().height()

app.exec()
sys.exit()