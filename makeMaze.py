# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 17:33:03 2021

@author: Huda Baig
"""

import ImageWriter
import ImageBounds as img
import mazeGrid as grid

import random
import time
import pygame

start = time.time()

#takes a picture of a grid and returns the measurement of the square's
#inner width/height, excluding its outline measurement
def boxSize(pic):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    
    #inspired by this thread: 
        #https://stackoverflow.com/questions/20165492/pygame-window-not-responding-after-a-few-seconds
        
    pygame.event.pump()
    
    width = ImageWriter.getWidth(pic)
    height = ImageWriter.getHeight(pic)
    
    #identify and store first white pixel with variables
    firstWhite = False
    firstWhiteLoc = 0
    
    for w in range(width):
        for h in range(height):
            colour = ImageWriter.getColor(pic, w, h)
            
            #end of outline so can check for inner size
            if (firstWhite == False and 
                img.isCloseColor(colour, [255, 255, 255], 50) == True):
                
                firstWhite = True
                firstWhiteLoc = h
            
            #start of next outline (which is not white), so end of inner size
            elif (img.isCloseColor(colour, [255, 255, 255], 50) == False
                  and firstWhite == True):
                
                #remove outline measurement incorporated
                return h - firstWhiteLoc
            
#takes a picture of a grid and returns the width of the line outlining each
#square
def lineSize(pic):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    width = ImageWriter.getWidth(pic)
    height = ImageWriter.getHeight(pic)
    
    for w in range(width):
        for h in range(height):
            colour = ImageWriter.getColor(pic, w, h)
            
            #outline starts from edge so just need to find where inner box
            #starts
            if img.isCloseColor(colour, [255, 255, 255], 50) == True:
                return h

#takes the top right coordinates of a box and removes the box's right outline
#within its inner limits only
def removeRightLine(pic, org, x, y):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    box = boxSize(org)
    line = lineSize(org)
    
    #finding coordinate bounds of box's right line
    x0 = x + box
    
    x1 = x0 + line
    y1 = y + box 
    
    #setting all pixels in coordinate bounds to white, which is same as
    #background colour
    for w in range(x0, x1):
        for h in range(y, y1):
            ImageWriter.setColor(pic, w, h, [255, 255, 255])
  
#takes the top right coordinates of a box and removes the box's bottom outline
#within its inner limits only
def removeBottomLine(pic, org, x, y):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    box = boxSize(org)
    line = lineSize(org)
    
    #finding coordinate bounds of box's bottom line
    y0 = y + box
    
    x1 = x + box
    y1 = y0 + line
    
    #setting all pixels in coordinate bounds to white, which is same as
    #background colour
    for w in range(x, x1):
        for h in range(y0, y1):
            ImageWriter.setColor(pic, w, h, [255, 255, 255])
            
#takes the top right coordinates of a box and removes the box's top outline
#within its inner limits only
def removeTopLine(pic, org, x, y):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    box = boxSize(org)
    line = lineSize(org)
    
    #finding coordinate bounds of box's top line, don't need x0 and y1 
    #as these are top right coordinate which is given
    y0 = y - line
    x1 = x + box
    
    #setting all pixels in coordinate bounds to white, which is same as
    #background colour
    for w in range(x, x1):
        for h in range(y0, y):
            ImageWriter.setColor(pic, w, h, [255, 255, 255])

#takes the top right coordinates of a box and removes the box's left outline
#within its inner limits only    
def removeLeftLine(pic, org, x, y):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    box = boxSize(org)
    line = lineSize(org)
    
    #finding coordinate bounds of box's left line, don't need y0 and x1 
    #as these are top right coordinate which is given
    x0 = x - line
    
    y1 = y + box
    
    #setting all pixels in coordinate bounds to white, which is same as
    #background colour
    for w in range(x0, x):
        for h in range(y, y1):
            ImageWriter.setColor(pic, w, h, [255, 255, 255])

#takes a picture of a grid and creates a path from the top right box to a
#random box in the rightmost column or bottom row
def digMazePath(pic, org):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    r = 0 
    c = 0
    direction = ""
    
    line = lineSize(org)
    
    #storing some boxes part of path for later comparison when adjusting
    #remaining boxes to look like a maze
    path = set((line, line))
    
    #only boundary box has an extra line on the left so remaining boxes
    #have only one outline
    fullBox = boxSize(org) + line
    
    boxNo = ImageWriter.getWidth(pic) // fullBox
    
    while r < boxNo and c < boxNo:
        pygame.event.pump()
        
        #can only move down or right in top row
        if r == 0:
            direction = random.choice(["Right", "Bottom"])
            
        #if prev direction is up, don't want to reverse path by moving down
        elif direction == "Top":
            direction = random.choice(["Right", "Top"])
            
        #if prev direction is down, don't want to reverse path by moving up
        elif direction == "Bottom":
            direction = random.choice(["Right", "Bottom"])
            
        else:
            direction = random.choice(["Right", "Bottom", "Top"])
            
        #a box's top right coordinate changes by same amount from one row
        #or column to next, so can just multiply by row/column no.
        x = c * fullBox + line
        y = r * fullBox + line
        
        if direction == "Right":
            removeRightLine(pic, org, x, y)
                
            c += 1
            
        elif direction == "Bottom":
            removeBottomLine(pic, org, x, y)

            r += 1
            
            #need to preserve boxes going down to maintain path turns
            path.add((x, y))
            
        elif direction == "Top":
            removeTopLine(pic, org, x, y)
             
            r -= 1
            
            #need to preserve boxes going up to maintain path turns 
            path.add((x, y))
    
    path.add((x, y))
    
    #opening a possible horizontal isolated section while maintaining 
    #entrance wall
    if direction == "Right":
        c -= 2
        x = c * fullBox + line
        
        removeBottomLine(pic, org, x, y)
    
    return path

#takes a picture of a grid with a maze path created and randomly removes 
#lines from remaining cell to form a maze-like picture 
def likeMaze(pic, org, path):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    direction = ""
    line = lineSize(org)
    
    fullBox = boxSize(org) + line
    
    boxNo = ImageWriter.getWidth(pic) // fullBox
    
    #going over each cell
    for r in range(boxNo):
        for c in range(boxNo):
            pygame.event.pump()
            
            #choose a random direction from left or bottom in last column 
            #to minimise isolated sections
            if c == boxNo - 1:
                direction = random.choice(["Left", "Bottom"])
                
            #choose a direction from right and left to minimise isolated 
            #sections in last row
            elif r == boxNo - 1:
                direction = random.choice(["Right",  "Left"])
            
            #choose right or bottom in remaining cells to prevent line
            #removal overlap
            else:
                direction = random.choice(["Right", "Bottom"])
            
            x = c * fullBox + line
            y = r * fullBox + line
            
            #don't want to change top right cell which is always the start of 
            #the maze and any turning cells part of the path
            if (r, c) != (0, 0) and (x, y) not in path:
                
                #excluding cells that would result in border remove
                if direction == "Right" and c != boxNo - 1:
                    removeRightLine(pic, org, x, y)
                    
                elif direction == "Bottom" and r != boxNo - 1:
                    removeBottomLine(pic, org, x, y)
                    
                elif direction == "Top" and c != 0:
                    removeTopLine(pic, org, x, y)
                
                elif direction == "Left" and c != 0:
                    removeLeftLine(pic, org, x, y) 
       
#takes a maze picture and opens up any isolated sections remaining
def openIslands(pic, org, path):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    line = lineSize(org)
    fullBox = boxSize(org) + line
    
    boxNo = ImageWriter.getWidth(pic) // fullBox
    const = (boxNo - 1) * fullBox + lineSize(org)
    
    for i in range(boxNo):
        pygame.event.pump()
        
        coor = i * fullBox + lineSize(org)
        
        #because of use of right and bottom directions, isolated sections
        #connected to last row and col only, so clearing these while 
        #maintaining turns frees these sections
        
        if i < boxNo - 1 and (const, coor) not in path:
            removeBottomLine(pic, org, const, coor)
            
        #include boxes in last row to ensure bottom exits don't create
        #isolated sections
        if i < boxNo - 1:
            removeRightLine(pic, org, coor, const)
  
#generates a grid of 20 x 20 or 25 x 25 depending on inputted difficulty 
#and forms a maze from the grid
def maze(lvl):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    if lvl == 1:
        #25 x 25 grid
        grid.drawGrid()
        
    else:
        #20 x 20 grid
        grid.drawGrid2()
    
    pygame.event.pump()
    
    #need a copy of image to extract correct line and box sizes while lines
    #are removed
    base = ImageWriter.loadPicture("main maze/grid made.png")
    copy = ImageWriter.loadPicture("main maze/grid made.png")
         
    loc = digMazePath(base, copy)
    
    likeMaze(base, copy, loc)
    openIslands(base, copy, loc)
    
    #creating entrance at top right cell 
    removeTopLine(base, copy, lineSize(copy), lineSize(copy))
    
    ImageWriter.savePicture(base, "main maze/maze.jpg")
