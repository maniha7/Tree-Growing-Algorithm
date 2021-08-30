#This will remember what is behind leaves!
from Pixel import Pixel

class memory:
    def __init__(self):
        self.leafMemory = {}
        self.GUI = None
        self.liveLeafMemory = {}



    #keep live gui for correct memory
    def updateGUI(self,gui):
        self.GUI = gui

    def addMemory(self,leaf):
        self.leafMemory[leaf]=[]
        for x in range(leaf.scaleFactor):
            for y in range(leaf.scaleFactor):
                memFragment = self.GUI.pixAtLocation(leaf.x*leaf.scaleFactor+x,leaf.y*leaf.scaleFactor+y)
                self.leafMemory[leaf].append(memFragment)

    def addLivingLeafMemory(self,leaf):
        liveMem = self.GUI.leafAtLocation(leaf.x,leaf.y)
        self.liveLeafMemory[liveMem]=liveMem

    def restoreMemory(self,leaf):
        for pixel in self.leafMemory[leaf]:
            pixel.draw(pixel.color,pix=pixel)

    def restoreLivingLeafMemory(self,leaf):
        if leaf in self.liveLeafMemory:
            leaf.draw(pix=leaf)

    def forget(self,leaf):
        self.leafMemory.pop(leaf)




