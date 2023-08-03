# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 00:50:17 2021

@author: Huda Baig
"""

import pygame

import ImageBounds as coor
import ImageWriter

from classes import Player, Tile, Button
from makeMaze import maze

#the class app will be used to store variables that multiple classes and 
#functions must access

#adapted from cmu_112_graphics.py
class App(object):
    def __init__(self, width, height):
        
        #stores screen's width and height initially
        self.width = width
        self.height = height
        
############ interaction functions ############

#processes key events to move sprite with arrow keys, a helper function
#to condense keyPressed
def arrowKeys(event, app):
    #storing arrow keys' values for ease of access later
    keys = {"Up": 1073741906, "Down": 1073741905, "Right": 1073741903, 
            "Left": 1073741904}
    
    #changing player sprite's y coordinate according to arrow key presses
    #and loading correct directional image
    if event.key == keys["Down"]:
        
        #toggling walk checking variable to move back and forth between
        #walking images for animation
        app.walk = not(app.walk)
        
        move = app.player.makeMove(0, 50, app)
        
        #running walking animation in correct direction
        app.player.walk(app, "Down")
        
        #storing direction to load correct image when stopped
        app.stop = "Down"
        
        #try scrolling if successfully moved 
        if move == True:
            app.tile.scrollDown(app, app.scroll)
    
    elif event.key == keys["Up"]:
        app.walk = not(app.walk)
        
        move = app.player.makeMove(0, -50, app)
        
        app.player.walk(app, "Up")
        app.stop = "Up"
        
        if move == True:
            app.tile.scrollUp(app, app.scroll)
        
    #changing player sprite's x coordinate according to arrow key presses
    #and loading correct directional image
    elif event.key == keys["Right"]:
        
        #toggling walk checking variable to move back and forth between
        #walking images for animation
        app.walk = not(app.walk)
        
        move = app.player.makeMove(50, 0, app)
        
        #running walking animation in correct direction
        app.player.walk(app, "Right")
        
        #storing direction to load correct image when stopped
        app.stop = "Right"
        
        #try scrolling if successfully moved 
        if move == True:
            app.tile.scrollRight(app, app.scroll)
        
    elif event.key == keys["Left"]:
        app.walk = not(app.walk)
        
        move = app.player.makeMove(-50, 0, app)
        
        app.player.walk(app, "Left")
        app.stop = "Left"
        
        if move == True:
            app.tile.scrollLeft(app, app.scroll)
        
        
#keyPressed handles the game's reaction to a user's key presses

#This handling skeleton was taken from: 
    # pygamegame.py
    # created by Lukas Peraza
    
    #the code inside the function was written by me
    
def keyPressed(event, app):
    
    #process arrow keys
    arrowKeys(event, app)
    
    #toggle map view with v key
    if event.key == ord("v"):
        app.view = not(app.view)
        
    #end game and return to home screen with h key
    elif event.key == ord("h"):
        app.runGame = False
        menuScreen(app)
        
#mousePressed handles the game's reaction to a user's key presses

#This handling skeleton was taken from: 
    # pygamegame.py
    # created by Lukas Peraza
    
    #the code inside the function was written by me
    
def mousePressed(event, app):
    
    #store x and y of mouse presses for easy access
    x = event.pos[0]
    y = event.pos[1]
    
    #processing level buttons on home menu and closing menu
    if app.runMenu == True and app.play1.onClick(x, y) == True:
        app.lvl = 2
        app.runMenu = False
        
    elif app.runMenu == True and app.play2.onClick(x, y) == True:
        app.lvl = 1
        app.runMenu = False
        
    #toggling info slide with info button clicks
    elif app.runMenu == True and app.info.onClick(x, y) == True:
        app.viewInfo = not(app.viewInfo)
        
    #processing button clicks on game complete page
    elif (app.runGame == True and app.gameOver == True):
        
        #playing any level generates maze for that level again and shifts
        #to loading screen
        if app.playAgain1.onClick(x, y) == True:
            app.lvl = 2
            
            loadScreen(app)
            appStarted(app)
        
        if app.playAgain2.onClick(x, y) == True:
            app.lvl = 1
            
            loadScreen(app)
            appStarted(app)
            
        #home screen button ends game loop and runs home screen loop 
        if app.home.onClick(x, y) == True:
            app.runGame = False
            menuScreen(app) 
    

############ intialising game window ############
pygame.init()

#setting screen width and height
width = 624
height = 624
app = App(width, height)

app.runGame = False
app.gameOver = False

#creating game screen and timer
app.clock = pygame.time.Clock()

app.screen = pygame.display.set_mode((app.width, app.height))

    
    
############# make maze ############

#loading floor image that will be used for maze tiles
app.floor = pygame.image.load("main maze/floor 2.png")

############# main loop #############

#generating all the variables needed to start the game

#adapted from cmu_112_graphics.py 
def appStarted(app):
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    
    #inspired by this thread: 
        #https://stackoverflow.com/questions/20165492/pygame-window-not-responding-after-a-few-seconds
    pygame.event.pump()
    
    #generating the random maze depending on level chosen
    if app.lvl == 2:
        maze(2)
        
        #making tile according to 20 x 20 maze dimensions, for a 3 x 3 tile
        app.tile = Tile(app, 78, 78, 8)
        app.scroll = 75
        
    elif app.lvl == 1:
        maze(1)
        
        #making tile according to 25  x 25 maze dimensions, for a 3 x 3 tile
        app.tile = Tile(app, 63, 63, 10)
        app.scroll = 60
        
    pygame.event.pump()
    
    #loading random maze image for processing
    app.maze = ImageWriter.loadPicture("main maze/maze.jpg")
    
    #map toggle variable
    app.view = True
    
    app.gameOver = False
    
    #finding horizontal entrance, but if not found, need vertical entrance
    if coor.findHorizontalEntrance(app.maze) != False:
        app.posX, app.posY = coor.findHorizontalEntrance(app.maze)
    
    #find vertical entrance to maze
    else:
        app.posX, app.posY = coor.findVerticalEntrance(app.maze)

    #find exit of maze
    app.exitBounds, app.loc = coor.findExit(app.maze, (app.posX, app.posY))
    
    #generating the player's sprite to control at entrance
    app.player = Player(app)
    
    #variables for walking animation and still images
    app.walk = False
    app.stop = "Down"
    
    #end loading screen loop so that only game loop runs
    app.menuQuit = True

#draws the game complete screen 
def makeOverScreen(app):
    if app.gameOver == False:
        
        #only play game complete sound once, when app.gameOver is initially
        #False
        pygame.mixer.music.load("main maze/gameOver.wav") 
        pygame.mixer.music.play()
            
    app.gameOver = True
    
    #loading game complete background
    over = pygame.image.load("screens/game over.PNG")
    
    #making buttons to allow replay
    app.playAgain1 = Button(212, 270, "screens/play 1.png")
    app.playAgain2 = Button(212, 370, "screens/play 2.png")
    
    #making home screen button
    app.home = Button(10, app.height - 80, "screens/home.png")
    
    #rendering background and buttons to screen
    app.screen.blit(over, (0, 0))
    app.screen.blit(app.home.surf, (app.home.x, app.home.y))
    
    app.screen.blit(app.playAgain1.surf, (app.playAgain1.x, 
                                         app.playAgain1.y))
    
    app.screen.blit(app.playAgain2.surf, (app.playAgain2.x, 
                                         app.playAgain2.y))
    
#draws map view of maze
def drawView(app):
    
    #generating and filling and semi-transparent surface for map
    
    #transparency argument taken from:
        #https://riptutorial.com/pygame/example/23788/transparency
        
    app.map = pygame.Surface((100, 100), pygame.SRCALPHA)
    app.map.fill((204, 204, 204, 150))
    
    #drawing exit location in yellow
    pygame.draw.circle(app.map, (255, 251, 0, 200), 
                       (app.exitBounds[0] / 5, 
                        app.exitBounds[1] / 5), 5)
    
    #drawing player location in red
    pygame.draw.circle(app.map, (255, 0, 0, 200), 
                       (app.player.absX / 5, 
                        app.player.absY / 5), 5) 
    
    #rendering map onto the screen
    app.screen.blit(app.map, (20, 20))
    
#runs main game in its own loop
def mainGame(app):
    #used to activate and terminate game loop
    app.runGame = True
    
    #initialising necessary variables
    appStarted(app)
    
    while app.runGame == True:
        
        #applying floor and walls to screen
        app.screen.blit(app.floor, (0, 0))
        app.tile.drawTile(app)
                
        #when player's sprite meets exit bound requirement, game is over
        if app.player.mazeWon(app.exitBounds, app.loc) == True:
            
            makeOverScreen(app)
            
        else:
            #rendering player sprite onto screen 
            app.screen.blit(app.player.surf, (app.player.x, app.player.y))
        
        for event in pygame.event.get():
            
            #accounting for window close attempts
            if event.type == pygame.QUIT:
                app.runGame = False
                
            #sending keypresses to keyPressed function for processing
            if event.type == pygame.KEYDOWN:
                keyPressed(event, app)
               
            #if no key pressed, sprite is idle so should change to resting
            #image
            else:
                app.player.changeDirection(app.stop)
                
            #sending mousepresses to mousePressed function for processing
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed(event, app) 
        
        #only checking for view drawing if game not complete, to prevent
        #view from drawing on game complete screen
        if (app.player.mazeWon(app.exitBounds, app.loc) == False and
            app.runGame == True):
            
            #drawing at end so sprite can go under it
            if app.view == True:
                drawView(app)
                
        #updating screen
        pygame.display.flip()
    
#draws menu screen of game
def makeMenu(app):
    
    #loading play buttons for both levels
    app.play1 = Button(212, 270, "screens/play 1.png")
    app.play2 = Button(212, 370, "screens/play 2.png")
    
    #loading menu background
    menu = pygame.image.load("screens/menu.PNG")
    
    #loading information background
    app.info = Button(10, app.height - 80, "screens/info.png")
    
    #applying background and buttons to the screen
    app.screen.blit(menu, (0, 0))
    app.screen.blit(app.info.surf, (app.info.x, app.info.y))
    
    app.screen.blit(app.play1.surf, (app.play1.x, app.play1.y))
    app.screen.blit(app.play2.surf, (app.play2.x, app.play2.y))
    
#runs menu screen in its own loop 
def menuScreen(app):
    
    #used to activate and terminate menu loop
    app.runMenu = True
    
    #used to either direct to closing window or run loading screen loop
    app.menuQuit = False
    
    #variable for toggling info slide
    app.viewInfo = False
    
    while app.runMenu == True:
        for event in pygame.event.get():
            
            #accounting for window close attempts
            if event.type == pygame.QUIT:
                app.runMenu = False
                app.menuQuit = True
            
            #send mousepresses to mousePressed for processing
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed(event, app)
                
        makeMenu(app) 
        
        if app.viewInfo == True:
            
            #loading info slide
            app.infoSlide = pygame.image.load("screens/slide.png")
            
            #rendering info slide to screen
            app.screen.blit(app.infoSlide, (100, 100))
        
        #updating screen
        pygame.display.flip()
        
#draws the loading screen 
def loadScreen(app):
    
    #load and render loading image
    loading = pygame.image.load("screens/loading.PNG")
    app.screen.blit(loading, (0, 0))
    
    #update screen
    pygame.display.flip()

#run menu outside loop as in its own unconnected running loop
menuScreen(app)

#if user didn't try to quit window, then show loading screen
while app.menuQuit == False:
    
    #passing through events from pygame event queue to prevent main game
    #from crashing while maze renders
    pygame.event.pump()
    
    loadScreen(app)
    
    #main game refers back to loading screen for new game, so inside 
    #loading screen loop so that the outside loop can be reactivated as needed
    mainGame(app)

pygame.quit()