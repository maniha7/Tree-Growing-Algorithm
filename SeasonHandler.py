import random
import time
from GenLeaves import Leaf

from Brain import memory

class SeasonHandler:
    def __init__(self, branchHandler):
        self.seasons = ['summer','fall','winter','spring']
        self.currentSeason = self.seasons[0]
        self.leafCores = {}
        self.deadCores = []
        self.leaves = {}
        self.fallingLeaves = {}
        self.branchHandler = branchHandler
        self.numLeaves = 0
        self.numLeavesToFall = 0
        self.GUI = None

        #handle waiting for growth finish
        self.listeningForChange = False
        self.numUnfinishedCores = 0
        self.fallingLeafTimeOffsetCounter = 0


        #grass things
        self.grassTimerDelay = 0
        self.grassColor = (30, 71, 6)
        self.grassLinesUpdated = False
        self.grassRowCounter = 0

        #Leaf memory (passed in later by GenLeaves)
        self.memory =None
        self.fallingLeafMemory = memory()
        self.leafMemorials = {}
        self.liveLeafMemorials = {}

        #manual screen clearers
        self.manualRestartHandler = 0
        self.restartSnowHandler = 0

        #snow handling
        self.flakes = {}
        self.restingFlakes = {}
        self.snowStopped = 0
        self.snowThroughSnow = {}
        self.snowSlow = 0
        self.snowDelay = 1
        self.snowCounter = 0

        #loop to beginning handler
        self.leafCoresRegrown=False
        self.leafStarts= {}
        self.nextHandler = None
        self.growthsLeft = 1


    def updateGUI(self,gui):
        self.GUI = gui

        if self.grassRowCounter==0:
            self.grassRowCounter=(self.GUI.height//self.GUI.scaleFactor-((self.GUI.height//self.GUI.scaleFactor)//12)*11)



    def setMemory(self,memory):
        self.memory=memory

    #add leaf core to handler
    def addLeafCore(self,core):
        self.leafCores[core]=core
        self.listeningForChange=True
        self.numUnfinishedCores+=1

    #add leaf to handler
    def addLeaf(self,leaf):
        self.leaves[leaf]=leaf

    #signal that a leaf core has finished growing
    def finishLeafCoreGrowth(self, gui):
        self.numUnfinishedCores-=1
        if self.numUnfinishedCores==0 and self.branchHandler.getNumBranches()==0 and self.listeningForChange==True:
            gui.initSeasonChange()
            self.numLeaves=len(self.leaves)
            self.numLeavesToFall=self.numLeaves//280
        #print(self.numUnfinishedCores)

    #if restart button is pressed mid-fall restore falling leaf memories
    def restartFallers(self):
        self.manualRestartHandler=1
        if len(self.leaves)!=0:
            self.fallingLeaf()


    def fallingLeaf(self):
        self.fallingLeafMemory.updateGUI(self.GUI)
        doneFalling = []
        if len(self.fallingLeaves)!=0:
            #clear the falling leaves from 1 pixel ago
            for leaf in self.leafMemorials:
                self.fallingLeafMemory.restoreMemory(leaf)
            self.leafMemorials.clear()



        #move falling leaves down
        for leaf in self.fallingLeaves:
            if self.fallingLeaves[leaf]<80 and leaf.y+self.fallingLeaves[leaf]+1<=leaf.getScreenHeight()-1 and self.manualRestartHandler==0:
                #if leaf has not fallen maximum amount, log where its next pixel location will be and get a memory of that spot
                self.fallingLeaves[leaf]+=1
                nextSpot = self.GUI.leafAtLocation(leaf.x, leaf.y + self.fallingLeaves[leaf])
                keepGoing = True
                if nextSpot in self.leaves:
                    doneFalling.append(leaf)
                    keepGoing = False
                else:
                    self.leafMemorials[nextSpot]=nextSpot
                    self.fallingLeafMemory.addMemory(nextSpot)

                #merge color with falling leaf and pixel below it and draw pixel below it that color
                #mergeColor = leaf.mergePixels(nextSpot,self.fallingLeaves[leaf])
                if keepGoing==True:
                    nextSpot.color=leaf.color
                    nextSpot.draw(pix=nextSpot)
            else:
                doneFalling.append(leaf)

        #eliminate leaves that have finished falling
        for leaf in doneFalling:
            self.fallingLeaves.pop(leaf)


    def addFallingLeaf(self,leaf):
        self.fallingLeaves[leaf]=1


    def changeSeason(self):
        if self.currentSeason=='summer':
            self.toFall()

        if self.currentSeason=='fall':
            self.toWinter()

        if self.currentSeason=='winter':
            self.toSpring()

        if self.currentSeason=='spring':
            self.toSummer()

    def restartSnow(self):
        for flake in self.flakes:
            flake.draw(self.flakes[flake],pix=flake)
        for flake in self.restingFlakes:
            flake.draw(self.restingFlakes[flake],pix=flake)



    def toFall(self):
        counter = 0
        for leaf in self.leaves:
            if leaf.color[0]<240:
                leaf.color=(leaf.color[0]+1,leaf.color[1],leaf.color[2])
                leaf.draw(pix=leaf)
            else:
                counter+=1
        for leaf in self.leafCores:
            if leaf.color[0]<240:
                leaf.color=(leaf.color[0]+1,leaf.color[1],leaf.color[2])
                leaf.draw(pix=leaf)
        if counter==len(self.leaves):
            self.currentSeason=self.seasons[1]

    def toWinter(self):
        self.fallingLeafTimeOffsetCounter+=1
        if self.fallingLeafTimeOffsetCounter%2==0:

            #Handle lonely leaves
            tempRemoveLeaves = []
            for leaf in self.leaves:
                #leaves with only 1 or no neighbors should die instantly
                if self.leaves[leaf].getLiveNeighbors(leaf, self.GUI,self.leaves)<=1:
                    tempRemoveLeaves.append(leaf)
            for leaf in tempRemoveLeaves:
                leaf = self.leaves.pop(leaf)
                self.memory.restoreMemory(leaf)

            for i in range(self.numLeavesToFall):
                if len(self.leaves)!=0:
                    #randomly pick some leaves to die
                    leaf = random.choice(list(self.leaves.values()))
                    liveNeighbors = self.leaves[leaf].getLiveNeighbors(leaf, self.GUI,self.leaves)

                    #only let them die if they dont have neighbors on all sides (prioritize spreading deaths of leaves rather than 100% random)
                    if liveNeighbors!=4:
                        leaf=self.leaves.pop(leaf)
                        self.memory.restoreMemory(leaf)
                        #randomly choose if leaf will animate falling
                        fallLimit = 7
                        if len(self.leaves)<=80:
                            fallLimit = 19
                        if len(self.leaves)<=30:
                            fallLimit = 45
                        if len(self.leaves)<=10:
                            fallLimit = 65
                        rareFall = random.randint(0,fallLimit)
                        if rareFall==0 and len(self.leaves)>10:
                            self.addFallingLeaf(leaf)

                else:
                    while len(self.fallingLeaves)!=0:
                        self.GUI.update(self.GUI)
                        self.fallingLeaf()


                    if len(self.leaves)==0:
                        self.currentSeason=self.seasons[2]


        #kill the leaf cores!
        for core in self.leafCores:
            if core.getLiveNeighbors(core,self.GUI,self.leaves)==0:
                self.memory.restoreMemory(core)
                self.deadCores.append(core)
        for core in self.deadCores:
            if core in self.leafCores:
                self.leafCores.pop(core)

        self.fallingLeaf()



    def toSpring(self):
        #Check if time to stop snowing
        if len(self.restingFlakes) + len(self.flakes) <= 50:
            self.snowDelay=9
        elif len(self.restingFlakes) + len(self.flakes) <= 100:
            self.snowDelay=6
        elif len(self.restingFlakes) + len(self.flakes) <= 150:
            self.snowDelay=3
        elif len(self.restingFlakes) + len(self.flakes) <= 150:
            self.snowDelay=1

        if len(self.restingFlakes) + len(self.flakes) >= 4060:
            self.snowDelay=2
        if len(self.restingFlakes) + len(self.flakes) >= 4100:
            self.snowDelay=4
        if len(self.restingFlakes) + len(self.flakes) >= 4150:
            self.snowDelay=6
        if len(self.restingFlakes) + len(self.flakes) >= 4180:
            self.snowDelay=9
        if len(self.restingFlakes)+len(self.flakes)>=4200:
            self.snowStopped=1
        if len(self.flakes)==0 and self.snowStopped==1:
            self.currentSeason=self.seasons[3]
        newFlakes = []
        oldFlakes = []
        fallPastCheck = 0
        for flake in self.flakes:
            stop = False
            if flake.y+1<=self.GUI.height-1 and self.restartSnowHandler == 0:
                next = self.GUI.pixAtLocation(flake.x,flake.y+1)
                #fall freely unless hit the edge of a branch, more snow, or grass
                if next.color!=(0,0,0) and next.getCurColor(next.x,next.y)!=(255,255,255) and next.color!=self.grassColor:
                    newFlakes.append(next)
                else:
                    #make sure it doesn't get stuck to the inside of branches
                    if flake.y-1>=0:
                        aboveChecker = self.GUI.pixAtLocation(flake.x,flake.y-1)
                    #better way to fix but it works quickly
                    else: aboveChecker = self.GUI.pixAtLocation(flake.x,flake.y+1)

                    #check if snow is stacked too high
                    if (next.color==(0,0,0) and (aboveChecker.getCurColor(aboveChecker.x,aboveChecker.y)[2]>10) and aboveChecker.y>0) or (next.getCurColor(next.x,next.y)==(255,255,255) and next.y<920):
                        #randomly have some flakes fall past other branches
                        fallPastCheck = random.randint(0,1)
                        next2 = self.GUI.pixAtLocation(next.x,next.y+1)
                        next3 = self.GUI.pixAtLocation(next2.x, next2.y + 1)
                        if next.getCurColor(next.x,next.y)==(255,255,255) and next2.getCurColor(next2.x,next2.y)==(255,255,255) and next3.getCurColor(next3.x,next3.y)==(255,255,255):
                            fallPastCheck=1

                        if next.color==(0,0,0) and next2.getCurColor(next2.x,next2.y)==(0,0,0):
                            fallPastCheck=0

                        #if chosen to keep falling, keep going, otherwise stop, which leaves the flake in place
                        if fallPastCheck==0:
                            stop = True
                        else:
                            if next.getCurColor(next.x,next.y)!=(0,0,0):
                                self.snowThroughSnow[next]=next
                            newFlakes.append(next)

                    #for ground covering snow
                    else:
                        if next.color==(0,0,0) and (aboveChecker.getCurColor(aboveChecker.x,aboveChecker.y)[2]>10):
                            stop=True
                        if next.color!=self.grassColor:
                            next2 = None
                            next3 = None

                            # make sure it doesnt try to reach pixels off the screen
                            if next.y + 1 < self.GUI.height:
                                next2 = self.GUI.pixAtLocation(next.x, next.y + 1)
                                if next2.y + 1 < self.GUI.height:
                                    next3 = self.GUI.pixAtLocation(next2.x, next2.y + 1)


                            if next2!=None and next3!=None:
                                # stop lower height snow from stacking
                                if next.getCurColor(next.x,next.y) == (255, 255, 255) and next2.getCurColor(next2.x, next2.y) == (255, 255, 255) and next3.getCurColor(next3.x, next3.y) == (255, 255, 255):
                                    flake.draw(self.flakes[flake], pix=flake,resetColor=False)
                                    stop=True
                                elif next.getCurColor(next.x,next.y)==(255,255,255):
                                    stop=True
                                else:
                                    newFlakes.append(next)
                            else:
                                newFlakes.append(next)
                        else:
                            stop=True
            #DRAW STOPPED FLAKE
            if stop:
                oldFlakes.append(flake)
                self.restingFlakes[flake]=self.flakes[flake]

            #ELSE DRAW FALLING FLAKE
            else:
                if flake not in self.snowThroughSnow:
                    flake.draw(self.flakes[flake], pix=flake, resetColor=False)
                else:
                    if flake.getCurColor(flake.x, flake.y) != (0, 0, 0):
                        flake.draw((255,255,255), pix=flake, resetColor=False)

                    self.snowThroughSnow.pop(flake)
                oldFlakes.append(flake)
        for flake in oldFlakes:
            self.flakes.pop(flake)



        numFlakes = random.randint(0,12-self.snowSlow)
        flakePos = []
        if self.snowStopped==0 and self.snowCounter%self.snowDelay==0:
            for i in range(numFlakes):
                pos = random.randint(0,self.GUI.width-1)
                flakePos.append(pos)

        for flakePos in flakePos:
            flake = self.GUI.pixAtLocation(flakePos,0)
            newFlakes.append(flake)

        for flake in newFlakes:
            self.flakes[flake]=flake.color
            flake.draw((255,255,255),pix=flake,resetColor=False)

        self.snowCounter+=1





    def toSummer(self):


        flakeMelt = {}
        #choose flakes to melt
        maxRange = 400
        if len(self.restingFlakes)<=maxRange:
            maxRange=len(self.restingFlakes)
        for i in range(maxRange):
            flake = random.choice(list(self.restingFlakes.items()))
            if flake[0].y-1 >=0:
                if self.GUI.pixAtLocation(flake[0].x,flake[0].y-1).curColor!=(255,255,255):
                    flake[0].draw(flake[1],pix=flake[0])
                    flakeMelt[flake[0]]=flake[0]
            else:
                flake[0].draw(flake[1], pix=flake[0])
                flakeMelt[flake[0]] = flake[0]
        if len(self.restingFlakes)<100:
            for flake in self.flakes:
                if flake.getCurColor(flake.x, flake.y - 1) != (255, 255, 255):
                    flake.draw(self.restingFlakes[flake], pix=flake)
                    flakeMelt[flake]=flake
        #remove melted flakes from flake list
        for flake in flakeMelt:
            if flake in self.restingFlakes:
                self.restingFlakes.pop(flake)

        #restart cycle if snow is gone
        if len(self.restingFlakes)==0:
            #respawn leaf cores if not yet done
            if not self.leafCoresRegrown:
                for core in self.deadCores:
                    core.resetColor()
                    self.leafCores[core]=core
                #pause a second and initialize a new seasonHandler for the next cycle

                self.GUI.cleanSlateLeaf()
                self.nextHandler = SeasonHandler(self.branchHandler)
                self.nextHandler.GUI = self.GUI

                #draw the cores and init the leaf generators
                for core in self.leafCores:
                    core.draw(pix=core)
                    start = Leaf(core,self.GUI,self.nextHandler,self.branchHandler)
                    self.leafStarts[start]=start
                self.leafCoresRegrown = True
                #num leaf cores done spreading
                self.growthsLeft = len(self.leafStarts)

            #else if leaf cores already respawned, grow leaves from them
            else:
                if self.growthsLeft!=0:
                    finishedCores = []
                    for core in self.leafStarts:
                        core.grow()
                        if core.finished==True:
                            self.growthsLeft-=1
                            finishedCores.append(core)
                    for core in finishedCores:
                        core = self.leafStarts.pop(core)
                        self.leafCores[core]=core

                #pass off new handler to GUI
                else:
                    time.sleep(1.5)
                    self.GUI.seasonHandler = self.nextHandler






