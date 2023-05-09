class Model:
    def __init__(self):
        self.fileName = ''
        self.outputfps = 0
        self.rescaleRatio = 0
        self.xlb = 0
        self.xub = 0
        self.ylb = 0
        self.yub = 0 
        self.outputPath = ''

    def setFileName(self, filename):
        self.fileName = filename
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
    