# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 22:53:56 2021

@author: Huda Baig
"""

import ImageWriter

#draws bottom and right borders on grid of given height
def remainingBorders(pic, size):
    width = ImageWriter.getWidth(pic)
    height = ImageWriter.getHeight(pic)
    
    for w in range(width):
        #draws bottom border
        drawLines(pic, w, width - size, size, [0xf9, 0x61, 0xc6])
        
    for h in range(height):
        #draws right border 
        drawOtherLines(pic, height - size, h, size, [0xf9, 0x61, 0xc6])

#draws a vertical line of given height, cols, from given x,y coordinate
#in a given colour
def drawLines(pic, x, y, cols, colour):
    
    #going from y to the the correct y coordinate to achieve given height
    for h in range(y, y + cols):
        ImageWriter.setColor(pic, x, h, colour) 
        
#draws a horizontal line of given width, cols, from given x,y coordinate
#in a given colour
def drawOtherLines(pic, x, y, cols, colour):
    
    #going from x to the the correct x coordinate to achieve given height
    for w in range(x, x + cols):
        ImageWriter.setColor(pic, w, y, colour)

#takes a blank white picture and draws a 25 x 25 square grid on it, hardcoded
#for a 503 x 503 image
def drawGrid():
    base = ImageWriter.loadPicture("main maze/base.jpg")

    width = ImageWriter.getWidth(base)
    height = ImageWriter.getHeight(base)

    for h in range(3, width, 20):
        for w in range(height):
            drawLines(base, w, h, 2, [7, 76, 99])
            
    #drawing horizontal lines at correct intervals
    for w in range(3, height, 20):
        for h in range(width):
            drawOtherLines(base, w - 3, h, 3, [0xf9, 0x61, 0xc6])
            drawOtherLines(base, w, h, 2, [38, 62, 70])
            
    #drawing vertical lines at correct intervals
    for h in range(3, width, 20):
        for w in range(height):
            drawLines(base, w, h - 3, 3, [0xf9, 0x61, 0xc6])
    
    remainingBorders(base, 5)
    
    ImageWriter.savePicture(base, "main maze/grid made.png")
    
#takes a blank white picture and draws a 20 x 20 square grid on it, hardcoded
#for a 503 x 503 image
def drawGrid2():
    base = ImageWriter.loadPicture("main maze/base.jpg")

    width = ImageWriter.getWidth(base)
    height = ImageWriter.getHeight(base)

    #drawing horizontal line shadows at correct intervals
    for h in range(3, height, 25):
        for w in range(width):
            drawLines(base, w, h, 2, [7, 76, 99])
            
    #drawing vertical lines and shadows at correct intervals
    for w in range(3, width, 25):
        for h in range(height):
            drawOtherLines(base, w - 3, h, 3, [0xf9, 0x61, 0xc6])
            drawOtherLines(base, w, h, 2, [38, 62, 70])
    
    #drawing horizontal lines at correct intervals 
    for h in range(3, height, 25):
        for w in range(width):
            drawLines(base, w, h - 3, 3, [0xf9, 0x61, 0xc6])
    
    remainingBorders(base, 5)
    ImageWriter.savePicture(base, "main maze/grid made.png")