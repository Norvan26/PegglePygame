import pygame
import sys
from settings import *


class Map:

    def __init__(self, screen, gameStateManager):
        #defines screen and gamestatemanger
        self.display = screen
        self.gameStateManager = gameStateManager
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
        
    

    def run(self):
            #pygame.time.Clock().tick(60)
            #draws all the rectangles for the level colliding
            self.level1 = pygame.Rect((2290 + self.offset_x, 1595+ self.offset_y, 70, 70))

            self.level2 = pygame.Rect((4097 + self.offset_x, 579+ self.offset_y, 30, 30))

            self.level3 = pygame.Rect((2020 + self.offset_x, 2600+ self.offset_y, 50, 30))

            self.level4 = pygame.Rect((3875 + self.offset_x, 2920+ self.offset_y, 60, 30))

            pygame.draw.rect(self.display, (0, 0, 255), self.level1)

            pygame.draw.rect(self.display, (0, 0, 255), self.level2)

            pygame.draw.rect(self.display, (0, 0, 255), self.level3)

            pygame.draw.rect(self.display, (0, 0, 255), self.level4)

            #draws the map with the inital offset which is 0,0
            self.display.fill((0,0,0))
            self.display.blit(self.map, (self.offset_x, self.offset_y))



            #draws the player rect in the middle of the screen
            rect = pygame.Rect(self.player_pos[0], self.player_pos[1], self.player_size, self.player_size)
            pygame.draw.rect(self.display, (255, 0, 0), rect)



            keys = pygame.key.get_pressed()
            #creates a temporary offset
            new_offset_x, new_offset_y = self.offset_x, self.offset_y

            #checks if the player has collided with a level and check if the player has completed it yet
            self.collide = pygame.Rect.colliderect(rect, self.level1)
            if self.collide and self.level1completed == False:
                self.gameStateManager.set_state('selector')
                self.level1completed = True

            self.collide2 = pygame.Rect.colliderect(rect, self.level2)
            if self.collide2 and self.level2completed == False and self.level1completed == True:
                self.gameStateManager.set_state('selector')
                self.level2completed = True

            self.collide3 = pygame.Rect.colliderect(rect, self.level3)
            if self.collide3 and self.level3completed == False and self.level1completed == True and self.level2completed == True:
                self.gameStateManager.set_state('selector')
                self.level3completed = True

            self.collide4 = pygame.Rect.colliderect(rect, self.level4)
            if self.collide4 and self.level4completed == False and self.level1completed == True and self.level2completed == True and self.level2completed == True:
                self.gameStateManager.set_state('selector')
                self.level4completed = True

            #check user inputs and changes the offset accordingly
            if keys[pygame.K_w]:
                new_offset_y += self.speed
                if self.collision(new_offset_x, new_offset_y):
                    new_offset_y -= self.speed

            if keys[pygame.K_s]:
                new_offset_y -= self.speed
                if self.collision(new_offset_x, new_offset_y):
                    new_offset_y += self.speed

            if keys[pygame.K_a]:
                new_offset_x += self.speed
                if self.collision(new_offset_x, new_offset_y):
                    new_offset_x -= self.speed

            if keys[pygame.K_d]:
                new_offset_x -= self.speed
                if self.collision(new_offset_x, new_offset_y):
                    new_offset_x += self.speed
            #sets the offset to the new offset so that it can be applied ot the map
            self.offset_x, self.offset_y = new_offset_x, new_offset_y
    
    def collision(self, new_offset_x, new_offset_y):
        for y, row in enumerate(self.layout):
            for x, col in enumerate(row):
                if col == 1134:
                    #draws the boxs with the added offset
                    wall_rect = pygame.Rect(x * self.tile + new_offset_x, y * self.tile + new_offset_y, self.tile, self.tile)
                    player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], self.player_size, self.player_size)
                    #checks if they have collided
                    if wall_rect.colliderect(player_rect):
                        return True
        return False
