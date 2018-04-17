

class ASTNode:

    def __init__(self, lineNr, positionNr):
        self.lineNr = lineNr
        self.positionNr = positionNr

    def getPosition(self):
        return "Line " + str(self.lineNr) + " at " + str(self.positionNr + 1)
