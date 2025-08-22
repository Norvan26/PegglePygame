import pygame
import sys
from settings import *


class Map:

    def __init__(self, screen, gameStateManager):
        #defines screen and gamestatemanger
        self.display = screen
        self.gameStateManager = gameStateManager
        self.my_font = pygame.font.SysFont('Comic Sans MS', 60)
        self.my_font_small = pygame.font.SysFont('Comic Sans MS', 20)
        
        #sets tile size to 32
        self.tile = 32
        #sets player size to 18
        self.player_size = 18
        #sets the speed to 10
        self.speed = 10
        #loads in the png of the map
        self.map = pygame.image.load('./images/pegglev4.png')
        self.map = pygame.transform.scale(self.map, (self.map.get_width()*2, self.map.get_height()*2))
        #sets the variable layout to the 2D array in settings
        self.layout = BIGMAP
        #sets the players pos to the center of the screen
        self.player_pos = [self.display.get_width() // 2, self.display.get_height() // 2]
        self.offset_x, self.offset_y = 0, 0
        #sets all the levels being completed to false
        self.level1completed = False
        self.level2completed = False
        self.level3completed = False
        self.level4completed = False
        self.movement = self.my_font_small.render('Click A or D to choose direction', True, (255, 255, 255))
        
        self.level1 = pygame.Rect((600, 60, 70, 70))
        
        self.level2 = pygame.Rect((400, 160, 70, 70))
        self.level3 = pygame.Rect((800, 160, 70, 70))

        self.level4 = pygame.Rect((400, 260, 70, 70))
        self.level5 = pygame.Rect((700, 260, 70, 70))
        self.level6 = pygame.Rect((900, 260, 70, 70))


        self.xLoc = 600

        self.yLoc = 60

        
        
    

    def run(self):

            self.display.fill((0,255,60))
            self.playerSprite = pygame.Rect((self.xLoc, self.yLoc, 40, 40))


            pygame.draw.rect(self.display, (255, 0, 0), self.level1)

            pygame.draw.rect(self.display, (255, 0, 0), self.level2)

            pygame.draw.rect(self.display, (255, 0, 0), self.level3)
            pygame.draw.rect(self.display, (255, 0, 0), self.level4)
            pygame.draw.rect(self.display, (255, 0, 0), self.level5)
            pygame.draw.rect(self.display, (255, 0, 0), self.level6)

            pygame.draw.rect(self.display, (0, 0, 0), self.playerSprite)

            self.display.blit(self.movement, (100, 100))


            self.player()

           # self.levels = CreateLevels(self.display, 4)

           # self.levels.run()




            


    def player(self):
        self.keys = pygame.key.get_pressed()
        #print('Hewwo')
        if self.keys[pygame.K_a] == True:
            print('Hewwo')
            self.xLoc = 300

        elif self.keys[pygame.K_d] == True:
            print('Hewwo')
            

class CreateLevels:
    def __init__(self, display, numberOfLevels:int):
        self.originX = 600
        self.originY = 60
        self.display = display

        i = 1

        self.locations = [(600, 60)]

        while i < numberOfLevels+1:
            length = len(self.locations)
            for j in range(length):
                self.locations.append((self.locations[j][0]+(100*i), self.locations[j][1]+120))
                self.locations.append((self.locations[j][0]-(100*i), self.locations[j][1]+120))
            i+=1
            
    
    def run(self):
        print(self.locations)


        for item in self.locations:
            pygame.draw.rect(self.display, (255, 0, 0), (item[0], item[1], 70, 70))
        
