# A class containing info on a particular pixel on the screen at some given time
# Location, color, direction...
import GUI
import pygame
import random


class LeafPixel:

    # inits a matrix of all pixels, each pixel 1x1 real pixels (subject to change)
    def __init__(self, screen, x, y):
        self.scaleFactor = 5
        self.screenWidth, self.screenHeight = screen.get_size()
        self.screenWidth = self.screenWidth // self.scaleFactor
        self.screenHeight = self.screenHeight // self.scaleFactor
        self.x = x
        self.y = y
        self.screen = screen
        self.neighbors = []
        RedAndBlue = random.randint(12, 70)
        self.color=((50, random.randint(110,185), RedAndBlue))

    # RGB color
    def draw(self,x=0, y=0, pix=None,):
        if pix is not None:
            pygame.draw.rect(self.screen, self.color, (pix.x * self.scaleFactor, pix.y * self.scaleFactor, self.scaleFactor, self.scaleFactor))
        else:
            pygame.draw.rect(self.screen, self.color, (x * self.scaleFactor, y * self.scaleFactor, self.scaleFactor, self.scaleFactor))

    def getScreenHeight(self):
        return self.screenHeight

    def resetColor(self):
        RedAndBlue = random.randint(12, 70)
        self.color = ((50, random.randint(110, 185), RedAndBlue))


    # if pixel is touching the border, which border
    def isOnEdge(self, pixel,specialScale=1):
        if pixel.x == 0 and pixel.y == 0: return "tlc"
        if pixel.x == 0 and pixel.y + 1 == self.screenHeight: return "blc"
        if pixel.x + 1 == self.screenWidth and pixel.y == 0: return "trc"
        if pixel.x + 1 == self.screenWidth and pixel.y + 1 == self.screenHeight: return "brc"
        if pixel.x == 0: return "left"
        if pixel.y == 0: return "top"
        if pixel.x + 1 == self.screenWidth: return "right"
        if pixel.y + 1 == self.screenHeight: return "bottom"
        return None

    # returns all neighboring pixels of any pixel in an image
    def getNeighbors(self, pixel, window):
        if self.isOnEdge(pixel) is None: return [
                                                 window.leafAtLocation(pixel.x - 1, pixel.y),

                                                 window.leafAtLocation(pixel.x, pixel.y - 1),
                                                 window.leafAtLocation(pixel.x, pixel.y + 1),

                                                 window.leafAtLocation(pixel.x + 1, pixel.y),
                                                 ]

        if self.isOnEdge(pixel) == "left": return [window.leafAtLocation(pixel.x, pixel.y - 1),
                                                   window.leafAtLocation(pixel.x, pixel.y + 1),

                                                   window.leafAtLocation(pixel.x + 1, pixel.y),
                                                   ]

        if self.isOnEdge(pixel) == "right": return [
                                                    window.leafAtLocation(pixel.x - 1, pixel.y),

                                                    window.leafAtLocation(pixel.x, pixel.y - 1),
                                                    window.leafAtLocation(pixel.x, pixel.y + 1)]

        if self.isOnEdge(pixel) == "top": return [
                                                  window.leafAtLocation(pixel.x - 1, pixel.y),
                                                  window.leafAtLocation(pixel.x, pixel.y + 1),

                                                  window.leafAtLocation(pixel.x + 1, pixel.y)]

        if self.isOnEdge(pixel) == "bottom": return [window.leafAtLocation(pixel.x - 1, pixel.y),

                                                     window.leafAtLocation(pixel.x, pixel.y - 1),
                                                     window.leafAtLocation(pixel.x + 1, pixel.y),
                                                     ]

        if self.isOnEdge(pixel) == "tlc": return [window.leafAtLocation(pixel.x, pixel.y + 1),
                                                  window.leafAtLocation(pixel.x + 1, pixel.y),
                                                  ]

        if self.isOnEdge(pixel) == "blc": return [window.leafAtLocation(pixel.x, pixel.y - 1),
                                                  window.leafAtLocation(pixel.x + 1, pixel.y),
                                                  ]

        if self.isOnEdge(pixel) == "trc": return [window.leafAtLocation(pixel.x - 1, pixel.y),
                                                  window.leafAtLocation(pixel.x, pixel.y + 1),
                                                  ]

        if self.isOnEdge(pixel) == "brc": return [window.leafAtLocation(pixel.x, pixel.y - 1),
                                                  window.leafAtLocation(pixel.x - 1, pixel.y),
                                                  ]

    def isLive(self,cell):
        color = self.screen.get_at((cell.x * self.scaleFactor, cell.y * self.scaleFactor))[:3]
        if color[0]==50 and color[2]<=70:
            return True
        else:
            return False

    #find if neighboring leaf spots are currently inhabited with living leaves
    def getLiveNeighbors(self,leaf,window,allLeaves):
        neighbors = self.getNeighbors(leaf,window)
        numLive = 0
        for neighbor in neighbors:
            if neighbor in allLeaves:
                numLive+=1
        return numLive

    def isShownFallCore(self,core):
        color1 = self.screen.get_at((core.x * self.scaleFactor, core.y * self.scaleFactor))[:3]
        color2 = self.screen.get_at((core.x * self.scaleFactor +self.scaleFactor-1, core.y * self.scaleFactor))[:3]
        color3 = self.screen.get_at((core.x * self.scaleFactor, core.y * self.scaleFactor +self.scaleFactor-1))[:3]
        color4 = self.screen.get_at((core.x * self.scaleFactor +self.scaleFactor-1, core.y * self.scaleFactor +self.scaleFactor-1))[:3]
        if color1==core.color and color2==core.color and color3==core.color and color4==core.color:
            return True


    def resetColor(self):
        RedAndBlue = random.randint(12, 70)
        self.color = ((50, random.randint(110, 185), RedAndBlue))

        #mixes current pixel scaled by amount (how much should current pixel color dominate) with otherPixel
        #amount is between 0,80
    def mergePixels(self,otherPixel, amount):
        curColorScaled = ((round(self.color[0]*(amount//80))//2)-1,(round(self.color[1]*(amount//80))//2)-1,(round(self.color[2]*(amount//80))//2)-1)
        otherColor = (otherPixel.color[0]//2,otherPixel.color[1]//2,otherPixel.color[2]//2)
        mergedColor = (curColorScaled[0]+otherColor[0],curColorScaled[1]+otherColor[1],curColorScaled[2]+otherColor[2])

        fixMerge = [mergedColor[0],mergedColor[1],mergedColor[2]]
        for i in range(len(mergedColor)):
            if mergedColor[i]<0:
                fixMerge[i]=0
        mergedColor = (fixMerge[0],fixMerge[1],fixMerge[2])

        return mergedColor



