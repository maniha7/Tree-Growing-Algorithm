import random
import math
from Brain import memory


class Leaf:
    def __init__(self, leaf, window, SeasonHandler, BranchHandler):
        # Leaf Memory
        self.window = window
        self.memory = self.window.memory

        #leaf core
        self.leaf=leaf
        self.SeasonHandler = SeasonHandler
        self.SeasonHandler.addLeafCore(leaf)
        self.BranchHandler = BranchHandler
        self.recentChangedLeaves = {}
        self.changingLeaves = {}
        self.drawLeaf(leaf)
        self.changingLeaves[leaf]=leaf
        self.finished=False
        for x in range(leaf.x * leaf.scaleFactor, leaf.x * leaf.scaleFactor + 5):
            for y in range(leaf.y * leaf.scaleFactor, leaf.y * leaf.scaleFactor + 5):
                self.window.addActivePixel(x, y)
        self.maxLeaf = 8
        self.growCounter = 0
        self.growthDelay = random.randint(45,85)

        #Give seasonHandler access to memory
        self.SeasonHandler.setMemory(self.memory)



    def drawLeaf(self,leaf):

        if leaf not in self.memory.leafMemory:
            self.memory.addMemory(leaf)
        leaf.draw(pix=leaf)

    def getDist(self,leaf):
        xDist = abs(self.leaf.x-leaf.x)
        yDist = abs(self.leaf.y-leaf.y)*2
        dist = math.sqrt((xDist^2)+(yDist^2))
        return dist


    def grow(self):
        self.growCounter += 1
        if self.finished==False and self.growCounter%self.growthDelay!=0:
            tempNewLeaves = []
            for leaf in self.changingLeaves:
                for neighbor in leaf.getNeighbors(leaf,self.window):

                    if neighbor not in self.recentChangedLeaves and not neighbor.isLive(neighbor):
                        # Make leaves only SOMETIMES grow (less likely when further from leaf core)
                        dist = self.getDist(neighbor)
                        toGrow = random.randint(0, round(self.maxLeaf - dist)+1)
                        if dist <self.maxLeaf and toGrow>=2:
                            tempNewLeaves.append(neighbor)

            self.recentChangedLeaves.clear()
            self.recentChangedLeaves = self.changingLeaves.copy()
            self.changingLeaves.clear()

            if len(tempNewLeaves)==0:
                self.finished=True
                self.SeasonHandler.finishLeafCoreGrowth(self.window)


            for newleaf in tempNewLeaves:
                self.changingLeaves[newleaf]=newleaf
                self.drawLeaf(newleaf)
                self.SeasonHandler.addLeaf(newleaf)

                for x in range(newleaf.x*newleaf.scaleFactor, newleaf.x*newleaf.scaleFactor + 5):
                    for y in range(newleaf.y*newleaf.scaleFactor, newleaf.y*newleaf.scaleFactor + 5):
                        self.window.addActivePixel(x,y)

