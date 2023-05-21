class Model:
    def __init__(self):
        self.fileName = ''
        self.filePath = ''
        self.outputfps = 0
        self.rescaleRatio = 0
        self.xlb = 0
        self.xub = 0
        self.ylb = 0
        self.yub = 0 
        self.inputPath = ''
        self.outputPath = ''
        self.sensitivtyThreshold = 0
    
    def setInputPath(self, inputPath):
        self.inputPath = inputPath
    def setOutputPath(self, outputPath):
        self.outputPath = outputPath

    def setFileName(self, filename):
        self.fileName = filename
    def setFilePath(self, filePath):
        self.filePath = filePath
    def setOutputfps(self, outputfps):
        self.outputfps = outputfps
    def setRescaleRatio(self, rescaleRatio):
        self.rescaleRatio = rescaleRatio
    def setxlb(self, xlb):
        self.xlb = xlb
    def setxub(self, xub):
        self.xub = xub
    def setylb(self, ylb):
        self.ylb = ylb
    def setyub(self, yub):
        self.yub = yub
    def setSensitivtyThreshold(self, threshold):
        self.sensitivtyThreshold = threshold