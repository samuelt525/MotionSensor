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
        print(outputfps)
        self.outputfps = outputfps
    def setRescaleRatio(self, rescaleRatio):
        print(rescaleRatio)
        self.rescaleRatio = rescaleRatio
    def setxlb(self, xlb):
        print(xlb)
        self.xlb = xlb
    def setxub(self, xub):
        print(xub)
        self.xub = xub
    def setylb(self, ylb):
        print(ylb)
        self.ylb = ylb
    def setyub(self, yub):
        print(yub)
        self.yub = yub
    