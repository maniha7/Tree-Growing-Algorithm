import Pixel
import random
from GenLeaves import Leaf



class Tree:
    def __init__(self, middle, startHeight, width, screen, initColor, seasonHandler, branchHandler, direction = 'up'):
        #SCREEN SETUP
        self.startHeight = startHeight
        self.direction=direction
        self.width=width
        self.middle = middle
        self.screen = screen
        #Just make sure red and green values are always higher than startHeight
        self.color = (120,79,5)
        #self.color = initColor

        #MAX HEIGHT AND BRANCH DISTANCE SETUP
        self.atMaxLength = False
        self.height = self.startHeight
        self.distance = 0
        self.maxLength = 10
        self.branchShrink = 5
        self.cornerFixer = 0
        if self.width>10 and self.height<=1000:
            self.maxLength = random.randrange(self.width,self.width*4)
        elif self.height > 1000:
            self.maxLength = random.randrange(100,270)
        elif self.width > 0 and self.width<=10:
            self.maxLength = random.randrange(5, 25)

        #DIRECTION AND BRANCH START LOCATION SETUP
        if direction == 'up':
            self.xLoc = self.middle - self.width//2
        if direction == 'diaLeft':
            self.xLoc = self.middle - self.width//2
        if direction == 'diaRight':
            self.xLoc = self.middle - self.width//2

        #TREE BRANCHES
        self.branches = []
        self.branchStyleChoices = 2
        self.branchStyle = random.randint(0,self.branchStyleChoices)

        #Leaves
        self.leafStart = None

        #handlers
        self.seasonHandler = seasonHandler
        self.branchHandler = branchHandler
        self.branchDone = False
        self.branchStarted = False



    #Grow current branch
    def grow(self, window):
        if self.branchStarted==False:
            self.branchStarted=True
            self.branchHandler.addBranch()


        #Stop branches growing out of the screen
        yCurrent = self.height + self.width // 2
        if yCurrent<=0:
            self.atMaxLength=True


        #ignore branch if it is at max length
        if not self.atMaxLength:

            #UP-FACING BRANCHES
            if self.direction=='up':
                #ONLY FIX CORNERS IF THE BRANCH IS WIDE ENOUGH TO HAVE A CORNER
                if self.width >self.branchShrink+1 and (self.branchStyle==0 or self.branchStyle==1):
                    if self.maxLength-self.distance<=self.branchShrink-1:
                        self.cornerFixer+=1
                #if up+right branches
                if self.branchStyle==0:
                    for x in range(self.xLoc+self.cornerFixer,self.xLoc+self.width):
                        treePixel = window.pixAtLocation(x, self.height)
                        if x == self.xLoc+self.cornerFixer or x == self.xLoc + self.width - 1:
                            treePixel.draw((0, 0, 0), x=x, y=self.height)
                        else:
                            treePixel.draw((self.color[0]-(self.xLoc+self.width-x), self.color[1]-(self.xLoc+self.width-x)//1.1, self.color[2]), x=x, y=self.height)
                        window.addActivePixel(x,self.height)
                        if self.height in window.grassPixelLines:
                            if treePixel in window.grassPixelLines[self.height]:
                                window.grassPixelLines[self.height].pop(treePixel)

                #elif up+left branches
                elif self.branchStyle == 1:
                    for x in range(self.xLoc,self.xLoc+self.width-self.cornerFixer):
                        treePixel = window.pixAtLocation(x, self.height)
                        if x == self.xLoc or x == self.xLoc + self.width - 1-self.cornerFixer:
                            treePixel.draw((0, 0, 0), x=x, y=self.height)
                        else:
                            treePixel.draw((self.color[0]-(self.xLoc+self.width-x), self.color[1]-(self.xLoc+self.width-x)//1.1, self.color[2]), x=x, y=self.height)
                        window.addActivePixel(x,self.height)
                        if self.height in window.grassPixelLines:
                            if treePixel in window.grassPixelLines[self.height]:
                                window.grassPixelLines[self.height].pop(treePixel)
                #Else fork branches
                else:
                    for x in range(self.xLoc+self.cornerFixer,self.xLoc+self.width):
                        treePixel = window.pixAtLocation(x, self.height)
                        if x == self.xLoc+self.cornerFixer or x == self.xLoc + self.width - 1:
                            treePixel.draw((0, 0, 0), x=x, y=self.height)
                        else:
                            treePixel.draw((self.color[0]-(self.xLoc+self.width-x), self.color[1]-(self.xLoc+self.width-x)//1.1, self.color[2]), x=x, y=self.height)
                        window.addActivePixel(x,self.height)
                        if self.height in window.grassPixelLines:
                            if treePixel in window.grassPixelLines[self.height]:
                                window.grassPixelLines[self.height].pop(treePixel)

                #REMEMBER: height is reversed because of how pixels are labeled (lower height = higher tree)
                if self.height>5:
                    self.height-=1
                    self.distance+=1
                    #Branch if at max branch length (chosen randomly for unique trees)
                    if self.distance == self.maxLength:
                        self.atMaxLength = True
                        # TREE BRANCH STYLE CHOICES
                        branchStylesUp = [      #Choice 0
                                                [Tree(self.xLoc+self.cornerFixer + (self.width - self.branchShrink) // 2, self.height,
                                                    self.width - self.branchShrink, self.screen, self.color,self.seasonHandler, self.branchHandler,
                                                    direction='up'),
                                                Tree(self.middle, self.height, self.width - self.branchShrink, self.screen, self.color,self.seasonHandler,self.branchHandler,
                                                    direction='diaRight')],
                                                # Choice 1
                                                [Tree(self.middle, self.height, self.width - self.branchShrink,
                                                      self.screen, self.color,self.seasonHandler, self.branchHandler,direction='diaLeft'),
                                                 Tree(self.xLoc + (self.width - self.branchShrink) // 2, self.height,
                                                      self.width - self.branchShrink, self.screen, self.color,self.seasonHandler,self.branchHandler,
                                                      direction='up')],
                                                 # Choice 2
                                                [Tree(self.middle, self.height, self.width - self.branchShrink,
                                                     self.screen, self.color, self.seasonHandler,self.branchHandler,direction='diaLeft'),
                                                Tree(self.middle, self.height, self.width - self.branchShrink, self.screen, self.color,self.seasonHandler,self.branchHandler,
                                                     direction='diaRight')],




                                                ]
                        if self.height<800:
                            #Choice 3 (only available at certain height to avoid massive low branch clustering)
                            branchStylesUp.append([Tree(self.middle, self.height, self.width - self.branchShrink,
                                                     self.screen, self.color, self.seasonHandler,self.branchHandler,direction='diaLeft'),
                                                Tree(self.middle, self.height, self.width - self.branchShrink, self.screen, self.color,self.seasonHandler,self.branchHandler,
                                                     direction='diaRight'),
                                                   Tree(self.xLoc + self.width + 1 - (self.width - (self.branchShrink+1)) // 2, self.height,
                                                        self.width - self.branchShrink, self.screen, self.color,self.seasonHandler,self.branchHandler,
                                                        direction='up')
                                                   ])
                            self.branchStylesChoices=3
                        if self.width>self.branchShrink:
                            self.branches=branchStylesUp[self.branchStyle]
                        else:
                            self.leafStart=Leaf(window.leafAtLocation(self.xLoc, self.height, scaled=True),window, self.seasonHandler,self.branchHandler)
                            window.addActivePixel(self.xLoc, self.height)
                    #Stop growing if branches are too small to see
                    if self.width<1:
                        self.atMaxLength=True

                else:
                    self.atMaxLength = True

            # DIAGONAL-LEFT-FACING BRANCHES
            if self.direction == 'diaLeft':
                if self.width>=self.branchShrink+1:
                    if self.maxLength-self.distance<=self.branchShrink+1:
                        self.cornerFixer+=1
                for x in range(self.xLoc+self.cornerFixer, self.xLoc + self.width):
                    if x == self.xLoc+self.cornerFixer or x == self.xLoc + self.width - 1:
                        window.pixAtLocation(x, yCurrent).draw((0, 0, 0), x=x, y=yCurrent)
                    else:
                        window.pixAtLocation(x, yCurrent).draw((self.color[0]-(self.xLoc+self.width-x), self.color[1]-(self.xLoc+self.width-x)//1.1, self.color[2]), x=x, y=yCurrent)
                    window.addActivePixel(x, yCurrent)



                self.height -= 1
                self.xLoc -= 1
                self.middle -= 1
                self.distance += 1
                # Branch if at max branch length (chosen randomly for unique trees)
                if self.distance == self.maxLength:
                    self.atMaxLength = True
                    if self.width>self.branchShrink:
                        self.branches = [Tree(self.xLoc+self.width+1- (self.width-6)//2, yCurrent, self.width - self.branchShrink, self.screen, self.color, self.seasonHandler,self.branchHandler,direction = 'up')]
                    else:
                        self.leafStart=Leaf(window.leafAtLocation(self.xLoc, self.height, scaled=True),window,self.seasonHandler,self.branchHandler)
                        window.addActivePixel(self.xLoc, self.height)
                # Stop growing if branches are too small to see
                if self.width < 1:
                    self.atMaxLength = True



            # DIAGONAL-RIGHT-FACING BRANCHES
            if self.direction == 'diaRight':
                if self.width>=self.branchShrink+1:
                    if self.maxLength-self.distance<=self.branchShrink-1:
                        self.cornerFixer+=1
                if yCurrent>0:
                    for x in range(self.xLoc, self.xLoc + self.width-self.cornerFixer):
                        if x==self.xLoc or x==self.xLoc+self.width-1-self.cornerFixer:
                            window.pixAtLocation(x, yCurrent).draw((0, 0, 0), x=x, y=yCurrent)
                        else:
                            window.pixAtLocation(x, yCurrent).draw((self.color[0]-(self.xLoc+self.width-x), self.color[1]-(self.xLoc+self.width-x)//1.1, self.color[2]), x=x, y=yCurrent)
                        window.addActivePixel(x, yCurrent)
                        yCurrent += 0


                    self.height -= 1
                    self.xLoc += 1
                    self.middle += 1
                    self.distance += 1
                    # Branch if at max branch length (chosen randomly for unique trees)
                    if self.distance == self.maxLength:
                        self.atMaxLength = True
                        if self.width>self.branchShrink:
                            self.branches = [
                                Tree(self.xLoc + (self.width-self.branchShrink)//2, yCurrent, self.width - self.branchShrink,
                                     self.screen, self.color, self.seasonHandler, self.branchHandler,direction='up')]
                        else:
                            self.leafStart=Leaf(window.leafAtLocation(self.xLoc, self.height, scaled=True),window, self.seasonHandler,self.branchHandler)
                            window.addActivePixel(self.xLoc, self.height)
                    # Stop growing if branches are too small to see
                    if self.width < 1:
                        self.atMaxLength = True

                else:
                    self.atMaxLength = True
        else:
            if(self.branchDone==False):
                self.branchHandler.finishBranch()
                self.branchDone=True
        #Recursively update all branches
        for branch in self.branches:
            branch.grow(window)
        if self.leafStart!=None and self.branchHandler.getNumBranches()==0:
            self.leafStart.grow()

