import math
import sys
import os
import tracker
from PyQt6.QtCore import QSize, Qt, QUrl, pyqtSlot, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QMenu, 
                             QFileDialog, QLineEdit, QFormLayout, QWidget, QHBoxLayout, 
                             QLabel, QSlider, QProgressBar, QRadioButton)
from PyQt6.QtGui import QPixmap, QAction


documents_dir = ''
if (sys.platform == 'win32'):
    documents_dir = os.getenv('USERPROFILE') + '\Documents'
else:
    documents_dir = os.path.expanduser("~/Documents")


class MainWindow(QMainWindow):
    fileSettingsChangedSignal = pyqtSignal(int, str)
    def __init__(self):
        super().__init__()
        self.InitializeMenu()

        # Create a QWidget and set its layout
        self.widget = CustomWidget(self)
        self.setCentralWidget(self.widget)
        
        # Set the window title and show the window
        self.setWindowTitle('Main Window')
        self.show()
    def InitializeMenu(self):
        self.menuBar = self.menuBar()
        self.fileMenu = QMenu('File')
        self.menuBar.addMenu(self.fileMenu)

        self.defaultVideoPath = QAction('Default Input Video Path')
        self.fileMenu.addAction(self.defaultVideoPath)
        self.defaultVideoPath.triggered.connect(self.DefaultInputPathDialog)

        self.defaultOutputPath = QAction('Default Output Video Path')
        self.fileMenu.addAction(self.defaultOutputPath)
        self.defaultOutputPath.triggered.connect(self.DefaultOutputPathDialog)
    def resizeLol(self, yuh):
        self.setMinimumSize(825, 150)
        self.resize(825, 150)
    def DefaultInputPathDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Select Directory')
        layout = QVBoxLayout()

        # create text input
        text_label = QLabel('Enter Input Video Path')
        text_input = QLineEdit()
        layout.addWidget(text_label)
        layout.addWidget(text_input)

        select_button = QPushButton('Select Directory')
        layout.addWidget(select_button)
        select_button.clicked.connect(lambda: self.selectDirectory(text_input))

        # create OK button
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        dialog.setLayout(layout)
        # create file path
        file_path = os.path.join(documents_dir, "MotionTracker.conf")
        if os.path.exists(file_path):
            with open (file_path,"r") as rf:
                firstline = rf.readline()
                text_input.setText(firstline)
        accept = dialog.exec()

        if accept and text_input.text():
            self.fileSettingsChangedSignal.emit(0, text_input.text())

    def DefaultOutputPathDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Text Input')
        layout = QVBoxLayout()

        # create text input
        text_label = QLabel('Enter Output Video Path')
        text_input = QLineEdit()
        layout.addWidget(text_label)
        layout.addWidget(text_input)

        select_button = QPushButton('Select Directory')
        layout.addWidget(select_button)
        select_button.clicked.connect(lambda: self.selectDirectory(text_input))

        # create OK button
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        dialog.setLayout(layout)
        # create file path
        file_path = os.path.join(documents_dir, "MotionTracker.conf")
        if os.path.exists(file_path):
            with open (file_path,"r") as rf:
                rf.readline()
                secondline = rf.readline()
                text_input.setText(secondline)
        accept = dialog.exec()

        if accept and text_input.text():
            self.fileSettingsChangedSignal.emit(0, text_input.text())

    def selectDirectory(self, text_input):
        directory_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        directory_path = os.path.normpath(directory_path)
        # For some reason the directory path becomes "." when hitting cancel in the file explorer window
        if directory_path != "" and directory_path != ".":
            text_input.setText(directory_path)

class CustomWidget(QWidget):
    resized = pyqtSignal()
    valueChanged = pyqtSignal()
    closed = pyqtSignal()
    selectFileSignal = pyqtSignal(list or int)
    processFileSignal = pyqtSignal()
    outputfpsSignal = pyqtSignal(str)
    rescaleRatioSignal = pyqtSignal(str)
    xlbSignal = pyqtSignal(int)
    xubSignal = pyqtSignal(int)
    ylbSignal = pyqtSignal(int)
    yubSignal = pyqtSignal(int)
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
    def __init__(self, mainWindowParent):
        super().__init__()
        self.mainWindowParent = mainWindowParent
        self.filename = ''
        self.frame_width = 0
        self.frame_height = 0 
        self.fps = 0
        self.setWindowTitle("Motion Tracker")
        # File
        self.formInitialized = False
        self.filebutton = QPushButton("Select File")
        self.filebutton.clicked.connect(self.selectFile)
        self.filebutton.setFixedWidth(500)
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.filebutton)
        self.h_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.view = QQuickWidget()
        self.view.rootContext().setContextProperty("guiParent", self)
        qml_file = os.path.join(os.path.dirname(__file__), 'media.qml')
        self.view.setSource(QUrl.fromLocalFile(qml_file))

        self.Form = QFormLayout()

        self.logo = QLabel()
        pixmap = QPixmap('Logo.png')
        pixmap = pixmap.scaled(500,160)
        self.logo.setPixmap(pixmap)
        self.Form.addRow(self.logo)
        self.Form.addRow(self.h_layout)
        self.setLayout(self.Form)
    
    def selectFile(self):
        file_dialog = QFileDialog(self, 'Open File')
        if self.inputPath:
            file_dialog.setDirectory(self.inputPath)
            self.filename = file_dialog.getOpenFileNames()
        else:
            self.filename = file_dialog.getOpenFileNames()
        if self.filename[0] == '':
            exit()
        self.Form.removeRow(self.logo)
        self.Form.removeRow(self.h_layout)
        self.selectFileSignal.emit(self.filename)
        self.initializeForm()

    def setOutputfps(self):
        self.outputfpsSignal.emit(self.outputfps.text())

    def setRescaleRatio(self):
        self.rescaleRatioSignal.emit(self.rescaleRatio.text())
    def setxlb(self):
        self.xlbSignal.emit(self.userXLB.value())
    def setxub(self):
        self.xubSignal.emit(self.userXUB.value())
    def setylb(self):
        self.ylbSignal.emit(self.userYLB.value())
    def setyub(self):
        self.yubSignal.emit(self.userYUB.value())

    def initializeForm(self):
        filename = self.filename[0][0]
        self.outputfps = QLineEdit()
        self.outputfps.textChanged.connect(self.setOutputfps)
        self.rescaleRatio = QLineEdit()
        self.rescaleRatio.textChanged.connect(self.setRescaleRatio)
        self.firstRow = QHBoxLayout()

        self.rescaleRatioLabel = QLabel("Rescale Ratio: ")
        self.firstRow.addWidget(self.rescaleRatioLabel)
        self.firstRow.addWidget(self.rescaleRatio)
        self.rescaleRatio.setText("100")
        self.outputfpsLabel = QLabel("Output FPS:")
        self.firstRow.addWidget(self.outputfpsLabel)
        self.outputfps.setText(str(int(math.ceil(self.fps))))
        self.firstRow.addWidget(self.outputfps)
        self.Form.addRow(self.firstRow)

        self.secondRow = QHBoxLayout()
        self.thirdRow = QHBoxLayout()
        self.fourthRow = QHBoxLayout()

        self.userYLBLabel = QLabel("Height Lower Bound:")
        self.secondRow.addWidget(self.userYLBLabel)
        self.userYLB = QSlider(Qt.Orientation.Horizontal)
        self.userYLB.setMaximum(math.floor(self.frame_height/2))
        self.secondRow.addWidget(self.userYLB)
        self.userYLB.valueChanged.connect(self.handleBoundValueChanged)
        self.userYLB.valueChanged.connect(self.setylb)


        self.userYUBLabel = QLabel("Height Upper Bound:")
        self.secondRow.addWidget(self.userYUBLabel)
        self.userYUB = QSlider(Qt.Orientation.Horizontal)
        self.userYUB.setMinimum(math.floor(self.frame_height / 2))
        self.userYUB.setMaximum(self.frame_height)
        self.userYUB.setValue(self.frame_height)
        self.userYUB.valueChanged.connect(self.handleBoundValueChanged)
        self.secondRow.addWidget(self.userYUB)
        self.userYLB.valueChanged.connect(self.setyub)



        self.userXLBLabel = QLabel("Width Lower Bound:")
        self.thirdRow.addWidget(self.userXLBLabel)
        self.userXLB = QSlider(Qt.Orientation.Horizontal)
        self.userXLB.setMaximum(math.floor(self.frame_width/2))
        self.userXLB.valueChanged.connect(self.handleBoundValueChanged)
        self.thirdRow.addWidget(self.userXLB)
        self.userYLB.valueChanged.connect(self.setxlb)

        self.userXUBLabel = QLabel("Width Upper Bound:")
        self.thirdRow.addWidget(self.userXUBLabel)
        self.userXUB = QSlider(Qt.Orientation.Horizontal)
        self.userXUB.setMinimum(math.floor(self.frame_width/2))
        self.userXUB.setMaximum(self.frame_width)
        self.userXUB.setValue(self.frame_width)
        self.userXUB.valueChanged.connect(self.handleBoundValueChanged)
        self.thirdRow.addWidget(self.userXUB)
        self.userYLB.valueChanged.connect(self.setxub)

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

        self.player = self.view.rootObject().findChild(QMediaPlayer, "player")
        self.player.setProperty('source', filename)
        self.player.setLoops(self.player.Loops.Infinite)
        self.player.pause()
        self.player
        self.submissionbutton = QPushButton('Submit')
        self.submissionbutton.clicked.connect(self.processVideo)
        self.Form.addRow(self.submissionbutton)



    @pyqtSlot(result=QSize)
    def getSize(self):
        return self.size()
    # resizes qml video player with window
    def resizeEvent(self, event):
        self.resized.emit()
        self.setFixedSize(event.size())
        super(CustomWidget, self).resizeEvent(event)
    def handleBoundValueChanged(self):
        self.valueChanged.emit()
    @pyqtSlot(result=list)
    def getBounds(self):
        return [self.userYLB.value(), self.userYUB.value(), self.userXLB.value(), self.userXUB.value()]
    @pyqtSlot(result=list)
    def getVideoDimensions(self):
        return [self.frame_width, self.frame_height]

    def processVideo(self):
        self.Form.removeRow(self.firstRow)
        self.Form.removeRow(self.secondRow)
        self.Form.removeRow(self.thirdRow)
        self.Form.removeRow(self.fourthRow)
        self.Form.removeWidget(self.submissionbutton)
        self.Form.removeRow(self.view) 

        self.progressBar = QProgressBar()

        self.progressBar.setGeometry(50, 50, 250, 30)
        
        self.progressBarRow = QHBoxLayout()
        self.progressBarRow.addWidget(self.progressBar)
        self.Form.addRow(self.progressBarRow)

        self.progressLabelRow = QHBoxLayout()
        self.progressLabel = QLabel("Processing video...")
        self.progressLabelRow.addWidget(self.progressLabel)
        self.Form.addRow(self.progressLabelRow)
        self.setMinimumSize(825, 150)
        self.resize(825, 150)
        self.mainWindowParent.resizeLol(self.mainWindowParent)
        QApplication.processEvents()
        self.processFileSignal.emit()

        self.close()

    def setInputPath(self, inputpath):
        self.inputPath = inputpath
    def setInitialParameters(self, framewidth, frameheight, fps):
        self.frame_width = framewidth
        self.frame_height = frameheight 
        self.fps = fps
