# A class containing info on a particular pixel on the screen at some given time
# Location, color, direction...
import GUI
import pygame


class Pixel:

    # inits a matrix of all pixels, each pixel 10x10 real pixels (subject to change)
    # EDGES: Left, top: 0,0  --  bottom,right: 104, 192
    def __init__(self, screen, x, y):
        self.scaleFactor = 1
        self.screenWidth, self.screenHeight = screen.get_size()
        self.screenWidth = self.screenWidth // self.scaleFactor
        self.screenHeight = self.screenHeight // self.scaleFactor
        self.x = x
        self.y = y
        self.screen = screen
        self.neighbors = []
        self.color=(0,0,0)
        self.curColor = (0,0,0)

    # RGB color
    def draw(self, color, x=0, y=0, pix=None,resetColor=True):
        if pix is not None:
            pygame.draw.rect(self.screen, color, (pix.x * self.scaleFactor, pix.y * self.scaleFactor, self.scaleFactor, self.scaleFactor))
            if resetColor:
                self.color=color
            self.curColor = color
        else:
            pygame.draw.rect(self.screen, color, (x * self.scaleFactor, y * self.scaleFactor, self.scaleFactor, self.scaleFactor))
            if resetColor:
                self.color=color
            self.curColor = color



    # if pixel is touching the border, which border
    def isOnEdge(self, pixel):
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
        if self.isOnEdge(pixel) is None: return [window.pixAtLocation(pixel.x - 1, pixel.y - 1),
                                                 window.pixAtLocation(pixel.x - 1, pixel.y),
                                                 window.pixAtLocation(pixel.x - 1, pixel.y + 1),
                                                 window.pixAtLocation(pixel.x, pixel.y - 1),
                                                 window.pixAtLocation(pixel.x, pixel.y + 1),
                                                 window.pixAtLocation(pixel.x + 1, pixel.y - 1),
                                                 window.pixAtLocation(pixel.x + 1, pixel.y),
                                                 window.pixAtLocation(pixel.x + 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "left": return [window.pixAtLocation(pixel.x, pixel.y - 1),
                                                   window.pixAtLocation(pixel.x, pixel.y + 1),
                                                   window.pixAtLocation(pixel.x + 1, pixel.y - 1),
                                                   window.pixAtLocation(pixel.x + 1, pixel.y),
                                                   window.pixAtLocation(pixel.x + 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "right": return [window.pixAtLocation(pixel.x - 1, pixel.y - 1),
                                                    window.pixAtLocation(pixel.x - 1, pixel.y),
                                                    window.pixAtLocation(pixel.x - 1, pixel.y + 1),
                                                    window.pixAtLocation(pixel.x, pixel.y - 1),
                                                    window.pixAtLocation(pixel.x, pixel.y + 1)]

        if self.isOnEdge(pixel) == "top": return [window.pixAtLocation(pixel.x - 1, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y),
                                                  window.pixAtLocation(pixel.x, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y)]

        if self.isOnEdge(pixel) == "bottom": return [window.pixAtLocation(pixel.x - 1, pixel.y),
                                                     window.pixAtLocation(pixel.x - 1, pixel.y - 1),
                                                     window.pixAtLocation(pixel.x, pixel.y - 1),
                                                     window.pixAtLocation(pixel.x + 1, pixel.y),
                                                     window.pixAtLocation(pixel.x + 1, pixel.y - 1)]

        if self.isOnEdge(pixel) == "tlc": return [window.pixAtLocation(pixel.x, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "blc": return [window.pixAtLocation(pixel.x, pixel.y - 1),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y),
                                                  window.pixAtLocation(pixel.x + 1, pixel.y - 1)]

        if self.isOnEdge(pixel) == "trc": return [window.pixAtLocation(pixel.x - 1, pixel.y),
                                                  window.pixAtLocation(pixel.x, pixel.y + 1),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y + 1)]

        if self.isOnEdge(pixel) == "brc": return [window.pixAtLocation(pixel.x, pixel.y - 1),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y),
                                                  window.pixAtLocation(pixel.x - 1, pixel.y - 1)]

    def isLive(self,cell):
        if self.screen.get_at((cell.x * self.scaleFactor, cell.y * self.scaleFactor))[:3] != (0,0,0):
            return True
        else:
            return False

    def makeCopy(self):
        copyPixel = Pixel(self.screen,self.x,self.y)
        copyPixel.neighbors = self.neighbors
        copyPixel.color = self.color
        return copyPixel


    #in the event the pixel color is overwritten with a temp state like a snowflake
    def getCurColor(self, x,y):
        color = self.screen.get_at((x * self.scaleFactor, y * self.scaleFactor))[:3]
        return color



