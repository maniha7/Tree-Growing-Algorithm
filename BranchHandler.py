
#for the sole purpose of knowing how many currently growing branches there are
class BranchHandler:
    def __init__(self):
        self.numBranches = 0

    def addBranch(self):
        self.numBranches+=1

    def finishBranch(self):
        self.numBranches-=1

    def getNumBranches(self):
        return self.numBranches
