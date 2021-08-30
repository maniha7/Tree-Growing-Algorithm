import pygame
import Pixel
import LeafPixel
import tkinter as tk
import random
import TreeMaker
import GenLeaves
import threading
import time
from SeasonHandler import SeasonHandler
from BranchHandler import BranchHandler
from Brain import memory




sysInfo = tk.Tk()

class window:
    def __init__(self):
        #init display settings
        pygame.init()
        pygame.display.set_caption("Generative Trees")
        self.width = sysInfo.winfo_screenwidth()
        self.height = sysInfo.winfo_screenheight()
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.frozen = False
        self.color = (142, 176, 232)
        self.scaleFactor = 1
        #init pixel grid
        self.pixels = {}
        self.activePixels = {}

        # grass
        self.grassPixels = {}
        self.grassPixelLines = {}
        for y in range(self.height//self.scaleFactor-((self.height//self.scaleFactor)//12)*11,self.height//self.scaleFactor):
            self.grassPixelLines[y]={}

        # handlers
        self.branchHandler = BranchHandler()
        self.seasonHandler = SeasonHandler(self.branchHandler)

        # leaf grid
        self.leafPixels = {}
        self.leafScaleFactor = 5
        self.cleanSlate()
        self.cleanSlateLeaf()
        self.treeStartWidth = 51
        self.treeInitColor = (random.randrange(70, 250), random.randrange(70, 250), random.randrange(70, 250))
        self.tree = TreeMaker.Tree(self.width // 2, self.height - 1, self.treeStartWidth, self.screen,
                                   self.treeInitColor,self.seasonHandler, self.branchHandler)



        #season start signal
        self.startSeason = False

        #Memory
        self.memory = memory()

    #blank pixel setup
    def cleanSlate(self):
        for x in range(self.width//self.scaleFactor):
            for y in range(self.height//self.scaleFactor):
                cPix = Pixel.Pixel(self.screen,x,y)
                self.pixels[(x, y)] = cPix
                if y < ((self.height//self.scaleFactor)//12)*11:
                    #make a blue gradient
                    cPix.draw((self.color[0]//(self.height/(y+1)),self.color[1]//(self.height/(y+1)),self.color[2]),x=x, y=y)

                else:
                    cPix.draw((30, 71+(y-((self.height//self.scaleFactor)//12)*11)//2, 6), x=x, y=y)
                    self.grassPixelLines[y][cPix]=cPix
                    self.grassPixels[cPix]=cPix

    # blank leaf setup
    def cleanSlateLeaf(self):
        for x in range(self.width // self.leafScaleFactor):
            for y in range(self.height // self.leafScaleFactor):
                cPix = LeafPixel.LeafPixel(self.screen, x, y)
                self.leafPixels[(x, y)] = cPix

    #track actively changed pixels so that only altered pixels need to be reset upon sim refresh
    def addActivePixel(self,x,y):
        pix = self.pixAtLocation(x,y)
        self.activePixels[pix]=pix

    def removeActivePixel(self,x,y):
        pix = self.activePixels.pop(self.pixAtLocation(x,y))



    def clearActivePixels(self):
        for pixel in self.activePixels:
            if pixel.y < ((self.height // self.scaleFactor) // 12) * 11:
                pixel.draw((self.color[0]//(self.height/(pixel.y+1)),self.color[1]//(self.height/(pixel.y+1)),self.color[2]), pix=pixel)
            else:
                pixel.draw((30, 71, 6), pix=pixel)


    #return current keyboard/mouse input
    def getEvent(self):
        return pygame.event.get()

    #Get pixel at x,y
    def pixAtLocation(self,x,y):
        return self.pixels[(x,y)]

    # Get leaf at x,y
    def leafAtLocation(self, x, y,scaled=False):
        if scaled:
            return self.leafPixels[(x//self.leafScaleFactor, y//self.leafScaleFactor)]
        else:
            return self.leafPixels[(x,y)]

    # Start/Pause animation
    def freeze(self):
        self.frozen = not self.frozen

    def initSeasonChange(self):
        self.startSeason=True

    #update screen graphics
    def update(self, window):
        if self.startSeason==False:
            self.tree.grow(window)
        else:
            self.seasonHandler.changeSeason()
        self.memory.updateGUI(window)
        self.seasonHandler.updateGUI(window)
        pygame.display.flip()

    #reset sim
    def reset(self):
        self.seasonHandler.restartSnow()
        self.clearActivePixels()
        self.resetLeafColors()

        self.startSeason = False
        self.activePixels = {}
        self.treeInitColor = (random.randrange(70, 250), random.randrange(70, 250), random.randrange(70, 250))
        self.seasonHandler.restartFallers()

        self.branchHandler = BranchHandler()
        self.seasonHandler = SeasonHandler(self.branchHandler)
        self.tree = TreeMaker.Tree(self.width // 2, self.height - 1, self.treeStartWidth, self.screen,
                                   self.treeInitColor, self.seasonHandler, self.branchHandler)


    def resetLeafColors(self):
        for leaf in self.leafPixels:
            RedAndBlue = random.randint(12, 70)
            self.leafPixels[leaf].color = ((50, random.randint(110, 185), RedAndBlue))