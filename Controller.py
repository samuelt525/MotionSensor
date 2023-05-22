from PyQt6.QtWidgets import QApplication
from View import MainWindow
from Model import Model
import os
import sys
import tracker

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
        self.confFileName = "MotionTracker.conf"
        self.view.widget.setInputPath(self.checkInputPath())
        self.view.show()

        self.view.fileSettingsChangedSignal.connect(self.saveToConfFile)
        self.view.defaultOutputVideoPathTextFieldSignal.connect(self.setDefaultOutputVideoPathTextInput)
        self.view.setDefaultVideoOutputPathSignal.connect(self.setOutputPath)
        self.view.widget.selectFileSignal.connect(self.setFile)
        self.view.widget.processFileSignal.connect(self.processFile)
        self.view.widget.outputfpsSignal.connect(self.setOutputfps)
        self.view.widget.rescaleRatioSignal.connect(self.setRescaleRatio)
        self.view.widget.xlbSignal.connect(self.setxlb)
        self.view.widget.xubSignal.connect(self.setxub)
        self.view.widget.ylbSignal.connect(self.setylb)
        self.view.widget.yubSignal.connect(self.setyub)
        self.view.widget.sensitivtyThreshold.connect(self.setSensitivtyThreshold)

    def checkInputPath(self):
        path = ''
        if os.path.exists(os.path.join(documents_dir, self.confFileName)):
            with open(os.path.join(documents_dir, self.confFileName)) as f:
                path = f.readline()
        return path

    def setFile(self,filename):
        self.model.setFileName(self.view.widget.filename)
        self.setFilePath()
        w, h, fps = tracker.getVideoBounds(filename[0][0])
        self.view.widget.setInitialParameters(w,h,fps)
    def setFilePath(self):
        filePath = ''
        filePathArr = self.view.widget.filename[0][0].split('/')
        filePathArr.pop()
        for d in filePathArr:
            filePath += d + '/'
        filePath = filePath.rstrip('/')
        self.model.setFilePath(filePath)
        self.setOutputPath()
    def setOutputPath(self, outputPath = ''):
        if outputPath:
            self.model.setOutputPath(outputPath)
        elif not outputPath and not self.model.outputPath:
            self.model.setOutputPath(self.model.filePath)
    def setDefaultOutputVideoPathTextInput(self):
        self.view.default_output_text_input.setText(self.model.outputPath)
    def saveToConfFile(self, lineNum, text_input):
        lines = ['', '']
        confFilePath = os.path.join(documents_dir, self.confFileName)
        if os.path.exists(confFilePath):
            with open(confFilePath, 'r') as f:
                lines = f.readlines()
        with open(confFilePath, "w") as f:
            lines[lineNum] = text_input + '/'
            for line in lines:
                f.write(f'{line.strip()}' +'\n')
        self.model.setInputPath(lines[0].rstrip())

        self.view.widget.setInputPath(self.model.inputPath)
        self.view.widget.setOutputPath(self.model.outputPath)
        print("File saved to:", self.confFileName)

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
    def setxlb(self, xlb):
        self.model.setxlb(xlb)
    def setxub(self, xub):
        self.model.setxub(xub)
    def setylb(self, ylb):
        self.model.setylb(ylb)
    def setyub(self, yub):
        self.model.setyub(yub)
    def setSensitivtyThreshold(self, threshold):
        self.model.setSensitivtyThreshold(threshold)
    def processFile(self):
        for filename in self.model.fileName[0]:
            tracker.processVideo(filename, self.view.widget.progressBar, self.model.outputfps, self.model.rescaleRatio, self.model.sensitivtyThreshold, self.model.xlb, self.model.xub, self.model.ylb, self.model.yub, self.model.outputPath)
        self.view.close()
    def run(self):
        self.app.exec()

if __name__ == '__main__':
    # Create and run controller
    controller = Controller()
    controller.run()