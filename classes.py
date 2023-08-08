# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 16:01:36 2021

@author: Huda Baig
"""
import pygame
from ImageBounds import isCloseColor
from makeMaze import boxSize, lineSize
import ImageWriter

################## collison check ################

#returns True if any coordinate within sprite's area is touching a black pixel
def touchingWall(rect, app):
    
    #get bounds of sprite
    x0 = rect[0]
    y0 = rect[1]
    
    x1 = x0 + rect[2]
    y1 = y0 + rect[3]
    
    #loop over each coordinate in sprite bounds to check it
    for w in range(x0, x1 + 1):
        for h in range(y0, y1 + 1):
            
            #check colour of pixel at current location 
            currentColour = app.screen.get_at((w, h))
            
            #only detecting collisions with actual wall colour, not shadows
            if isCloseColor(currentColour, [101, 154, 173], 30) == True:
                return True
            
    return False

################### Sprite Class ###################

#the Player class loads up a sprite picture and sets up functions to 
#allow it to move around
class Player(pygame.sprite.Sprite):
    
    def __init__(self, app):
        super(Player, self).__init__()
        
        #the sprite's game surface is built from the designated image
        self.surf = pygame.image.load("Sprites/Walk down.png")
        
        #height and width taken according to image's 
        #rectangular area coverage
        self.width = self.surf.get_rect()[-2]
        self.height = self.surf.get_rect()[-1]
        
        #always starting at top right cell in first tile, so position fixed
        self.x = app.width / 4
        self.y = self.height
        
        #absolute position relative to tile position on maze
        self.absX = app.tile.x + (self.x // app.tile.enlarge)
        self.absY = app.tile.y + (self.y // app.tile.enlarge)
    
    #returns the pygame-based rectangle of the sprite
    def rect(self):
        
        #the sprite's rectangle is the coordinate rectangle it covers, which
        #will be useful for detecting collisions and other location changes
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    #updates the the absolute position of the sprite, relative to the entire
    #maze, depending on its location on the current tile, and the tile
    #location
    def setAbs(self, app):
        
        self.absX = app.tile.x + (self.x // app.tile.enlarge)
        self.absY = app.tile.y + (self.y // app.tile.enlarge)
        
    #makeMove changes the x and y coordinate of the player sprite by the
    #indicated amount, returns True if move made and False if move not 
    #made due to collision
    def makeMove(self, dx, dy, app):
        
        #must calculate bottom of sprite to check bottom screen bound
        xBottom = self.x + self.width
        
        yBottom = self.y + self.height
        

        #check if resulting position is within screen bounds:
        if 0 <= (self.x + dx) and (xBottom + dx) <= app.width:
            self.x += dx
        
            
        if 0 <= (self.y + dy) and (yBottom + dy) <= app.height:
            self.y += dy
        
        #check for wall collisions on new position, if colliding, 
        #don't make move
        if touchingWall(self.rect(), app) == True:
            
            #play 'injury' sound when collision occurs
            pygame.mixer.music.load("main maze/collide.wav")
            pygame.mixer.music.play()
            
            self.x -= dx
            self.y -= dy
            
            return False
        
        #update absolute position when moving
        self.setAbs(app)
        
        return True
    
    #update sprite image to a walking image depending on the value assigned
    #to the walk variable - used to create walking animation
    def walk(self, app, direction):
        
        #toggles between images
        if app.walk == True:
            self.surf = pygame.image.load(f"Sprites/Walk {direction}1.png")
            
        elif app.walk == False:
            self.surf = pygame.image.load(f"Sprites/Walk {direction}2.png")
            
    #changeDirection loads the up an image with the sprite facing in a 
    #particular direction depending on the direction indicated
    def changeDirection(self, direction):
        
        if direction == "Up":
            #load new image
            self.surf = pygame.image.load("Sprites/Walk up.png")
            
            #set new height and width according to image
            self.width = self.surf.get_rect()[-2]
            self.height = self.surf.get_rect()[-1]
        
        elif direction == "Down":
            self.surf = pygame.image.load("Sprites/Walk down.png")
            
            self.width = self.surf.get_rect()[-2]
            self.height = self.surf.get_rect()[-1]
            
        elif direction == "Right":
            self.surf = pygame.image.load("Sprites/Walk right.png")
            
            self.width = self.surf.get_rect()[-2]
            self.height = self.surf.get_rect()[-1]
            
        elif direction == "Left":
            self.surf = pygame.image.load("Sprites/Walk left.png")
            
            self.width = self.surf.get_rect()[-2]
            self.height = self.surf.get_rect()[-1]
            
    #checks if sprite's current position is at maze exit, based on exit 
    #bounds passed in and the location of exit bounds
    def mazeWon(self, bounds, loc):
        
        #at top and bottom, flag for exit is y coordinate level
        #at right and left, flag for exit is x coordinate level 
        
        #at top, needs to go before y coordinate of bound
        if loc == "top" and (self.absY) <= bounds[1]:
            return True
        
        #at left, needs to go before x coordinate of bound
        elif loc == "left" and (self.absX) <= bounds[0]:
            return True
        
        #at right and bottom, needs to go after relevant coordinate bound
        elif loc == "bottom" and (self.absY) >= bounds[1]:
            return True
        
        elif loc == "right" and (self.absX) >= bounds[0]:
            return True
        
        #if no exit bound met, maze is not complete
        return False
    
#a class for tracking the maze tile being shown to be used when scrolling 
#view is implemented later
class Tile(object):
    def __init__(self, app, w, h, n):
        #tile always at beginning of image
        self.x = 0
        self.y = 0
        
        #extracting box and line sizes used to make maze for tile width
        #adjustment
        self.grid = ImageWriter.loadPicture("main maze/grid made.png")
        self.box = boxSize(self.grid)
        self.line = lineSize(self.grid) 
        
        self.width = w
        self.height = h
        
        #factor tile view will enlarge by
        self.enlarge = n
        
        #pygame.mixer.music.load("main maze/newTile.wav")
        
    #scrolls tile up based on input magnitude
    def scrollUp(self, app, dy):
        
        #only scroll when player is at 2/3 of tile
        if app.player.y <= 50:
            
            #if at top edge, shouldn't scroll
            if self.y > 0:
                
                #play tile switching sound
                pygame.mixer.music.load("main maze/newTile.wav")
                pygame.mixer.music.play()
                
                self.y -= dy
                
                #wrap sprite position when moving tiles
                app.player.y = (app.height - app.player.y) - app.player.height
                
            #going up will always have 3 cells to look at, so height should 
            #cover 3 tiles, which is inner width and a line, 
            #with remaining border on the end
            self.height = ((self.box + self.line) * 3) + 3
                
    #scrolls tile down based on input magnitude
    def scrollDown(self, app, dy):
        picH = ImageWriter.getHeight(app.maze)
        
        #only scroll when player is at 1/3 of tile
        if (app.player.y + app.player.height) >= (app.height - 50):
            
            #if at bottom edge, shouldn't scroll
            if self.y < picH:
                
                #play tile switching sound
                pygame.mixer.music.load("main maze/newTile.wav")
                pygame.mixer.music.play()
                
                self.y += dy
                
                #wrap sprite position when moving tiles
                app.player.y = app.height - app.player.y
                
            #at end of maze, there may not be three cells remaining, so
            #adjust tile height to only draw remaining cells without crash
            if picH - self.y < self.height:
                self.height = picH - self.y
            
            #if not at end, should draw 3 cells
            else:
                self.height = ((self.box + self.line) * 3) + 3
    
    #scrolls tile down based on input magnitude
    def scrollLeft(self, app, dx):
         
        #only scroll when player is at 1/3 of tile
        if app.player.x <= 50:
            
            #if at left edge, shouldn't scroll
            if self.x > 0:
                
                #play tile switching sound
                pygame.mixer.music.load("main maze/newTile.wav")
                pygame.mixer.music.play()
                
                self.x -= dx
                
                #wrap sprite position when moving tiles
                app.player.x = (app.width - app.player.x) - app.player.width
                
            #going up will always have 3 cells to look at, so width should 
            #cover 3 tiles
            self.width = ((self.box + self.line) * 3) + 3
            
    #scrolls tile down based on input magnitude 
    def scrollRight(self, app, dx):
        picW = ImageWriter.getWidth(app.maze)
        
        #only scroll when player is at 2/3 of tile
        if (app.player.x + app.player.width) >= (app.width - 50):
            
            #if at right edge, shouldn't scroll
            if self.x < picW:
                
                #play tile switching sound
                pygame.mixer.music.load("main maze/newTile.wav")
                pygame.mixer.music.play()
                
                self.x += dx
                
                #wrap sprite position when moving tiles
                app.player.x = (app.width - app.player.x) 
                
            #at end of maze, there may not be three cells remaining, so
            #adjust tile width to only draw remaining cells without crash
            if picW - self.x < self.width:
                self.width = picW - self.x
            
            #if not at end, should draw 3 cells
            else:
                self.width = ((self.box + self.line) * 3) + 3
             
    #draws the stored tile from the maze image, enlarged to fit the screen
    def drawTile(self, app):
        
        #going over tile pixels in image
        for w in range(self.x, self.x + self.width):
            for h in range(self.y, self.y + self.height):
                
                #each pixel spans across enlarge magnitude so adjusting
                #starting location of expanded rectangle representing pixel
                pixelX = (w - self.x) * self.enlarge
                pixelY = (h - self.y) * self.enlarge
        
                colour = tuple(ImageWriter.getColor(app.maze, w, h))
                
                #only draw walls
                if isCloseColor(colour, [255, 255, 255], 50) == False:
                    
                    #draw a bigger rectangle representing the pixel
                    pygame.draw.rect(app.screen, colour, (pixelX, pixelY,
                                                          self.enlarge, 
                                                          self.enlarge))

#a class that creates button surfaces and stores relevant values for click
#checking          
class Button(object):
    
    def __init__(self, x, y, filename):
        
        #making pygame surface of button 
        self.surf = pygame.image.load(filename)
        
        #height and width taken according to image's 
        #rectangular area coverage
        self.width = self.surf.get_rect()[-2]
        self.height = self.surf.get_rect()[-1]
        
        self.x = x
        self.y = y
        
    #returns True if given coordinates are in button bounds, and False 
    #otherwise
    def onClick(self, clickX, clickY):
        
        #if within button's full location, is a click
        if (self.x <= clickX <= (self.x + self.width) and
            self.y <= clickY <= (self.y + self.height)):
            
            #play button click sound
            pygame.mixer.music.load("screens/click.wav")
            pygame.mixer.music.play()
            
            return True
        
        return False
        
        