import pygame 
import sys
import random
import math
from level import Level
#from map import Map
from levelllayout import Map
from settings import *

screenWidth = 1280
screenHeight = 736
FPS = 60

click = False


#img = pygame.image.load('cloud_1.png')
img_pos = [160, 260]

obstacle = pygame.Rect((300, 400, 100, 50))


screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

class Game:
    def __init__(self):
        pygame.init()
        #creates the screen
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))

        self.clock = pygame.time.Clock()

        #creates an instance of gamestatemanager and passes in 'start' initially
        self.gameStateManager = GameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        #self.level = Level(self.screen, self.gameStateManager)
        #self.level = 0
        #creates an instance of all the class which I want my gamnestatemanager to be able to switch between
        self.map = Map(self.screen, self.gameStateManager)
        self.death = Death(self.screen, self.gameStateManager)
        self.selector = LevelSelector(self.screen, self.gameStateManager)
        self.howto = HowTO(self.screen, self.gameStateManager)

        #dictionary of all the class instances so a string is able to access them
        self.states = {'start':self.start, 'map':self.map, 'over':self.death, 'selector':self.selector, 'how':self.howto}



    def run(self):
        while True:
            for event in pygame.event.get():
                #if the event type is clicking the x button then the game quits
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #gets the mouses coordinates
                pos = pygame.mouse.get_pos()

                #Checks collisions for all the different buttons withbthe corrdinates of the mouse
                self.collidingStart = start_button.rect.collidepoint(pos)

                self.collidingEnd = stop_button.rect.collidepoint(pos)

                self.collidingGuide = help_button.rect.collidepoint(pos)

                self.collidingBack = back_button.rect.collidepoint(pos)

                self.collidingOver = quit_btn.rect.collidepoint(pos)

                #if the mouse collides with any of the buttons then change their cursor
                if self.collidingStart or self.collidingEnd or self.collidingGuide and self.gameStateManager.get_state() == 'start':
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW )


            
                #checks if the player has clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    #checks the if the player clicks the quit button on the game over screen
                    if self.gameStateManager.get_state() == 'over':
                        if self.collidingOver:
                            pygame.quit()
                            sys.exit()

                    
                    if  self.gameStateManager.get_state() == 'start':
                        #if the player has clciked and is colliding with the start button then change the scene to the map using gamestatemanager
                        if self.collidingStart:
                            self.gameStateManager.set_state('map')
                        
                        #quit since player has clicked the quit button
                        elif self.collidingEnd:
                            pygame.quit()
                            sys.exit()

                        elif self.collidingGuide:
                            self.gameStateManager.set_state('how')

                    if  self.gameStateManager.get_state() == 'how':

                        if self.collidingBack:
                            self.gameStateManager.set_state('start')


                           


            #this runs the class in the dictionary according to what string is currently held in the game state manager 
            self.states[self.gameStateManager.get_state()].run()
            #print(click)
            #updates display and use clock tick to prevent things from happening faster if they have a higher framerate
            pygame.display.update()
            self.clock.tick(FPS)

#level selector creates a new instance of level class whenever it is called
class LevelSelector:
    def __init__(self, screen, gamestatemanager):
        #defines screen surface and gamestatemanager so that it can be called
        self.gamestatemanager = gamestatemanager
        self.screen = screen
        #creates first initial level with the enemies being passed in and no fruits and full health
        self.lvl1 = Level(self.screen, MAPS[3], ['eye', 'slime', 'eye', 'eye'], 200, ['empty', 'empty', 'empty'])

        #number which is incrimented to control which level in the list of levels is being run
        self.lvlNum = 0
        #list containing all the levels
        self.levels = [self.lvl1]
        self.over = pygame.mixer.Sound('over.wav')


    def run(self):


        #runs the level which is in the list at the specified position of self.lvlnum
        self.levels[self.lvlNum].run()


        #returns a list which has either a true or false in the first position of the list if it is True then the level has beeen completed
        if self.levels[self.lvlNum].exit_code()[0] == True:
            
            self.levels.append(Level(self.screen, MAPS[self.lvlNum], ENEMIES[self.lvlNum], self.levels[self.lvlNum].exit_code()[1], self.levels[0].exit_code()[3]))


            self.lvlNum = self.lvlNum + 1
            self.gamestatemanager.set_state('map')

        if self.lvlNum <= len(self.levels)-1:
            if self.levels[self.lvlNum].exit_code()[1] <= 0:
                self.gamestatemanager.set_state('over')
                pygame.mixer.Sound.play(self.over)
                pygame.mixer.music.stop()




class HowTO:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #draws forrest background
        self.forestBackground = pygame.image.load('./images/forest1.png')
        self.forestBackground = pygame.transform.scale(self.forestBackground, (1280, 736))
        #creates the font for text to use(comic sans is not ugly...to me at least)
        my_font = pygame.font.SysFont('Comic Sans MS', 60)
        my_font_small = pygame.font.SysFont('Comic Sans MS', 20)
        #self.text_surface = my_font.render('Search For The Lost Skibidi', True, (255, 255, 255))
        #text about how to play the game for the uesr
        self.text_surface = my_font.render('How to Play', True, (255, 255, 255))
        self.text_surface1 = my_font_small.render('To play you must shoot the pegs which are the circles with your ball.', True, (255, 255, 255))
        self.text_surface2 = my_font_small.render('The amount of pegs you hit determines the amount of damage done', True, (255, 255, 255))
        self.text_surface2cont = my_font_small.render('to the wave of oncoming enemies.', True, (255, 255, 255))
        self.text_surface3 = my_font_small.render('The ball is aimed by using your mouse and the ball is shot by clicking.', True, (255, 255, 255))
        self.text_surface4 = my_font_small.render('To reset the pegs hit the green peg with your ball.', True, (255, 255, 255))
        self.text_surface5 = my_font_small.render('The blue pegs are bombs and do more damage to enemies when hit.', True, (255, 255, 255))
        self.text_surface6 = my_font_small.render('To enter levels tou must find enterances throughout the map,', True, (255, 255, 255))
        self.text_surface7 = my_font_small.render('these are marked by crystals, and must be completed in the order: orange, ', True, (255, 255, 255))
        self.text_surface8 = my_font_small.render('blue, purple green.', True, (255, 255, 255))
        self.text_surface9 = my_font_small.render('Now have fun!', True, (255, 255, 255))

        

    def run(self):
        #gets the width of the screen
        w, h = pygame.display.get_surface().get_size()
        #scales the background to the dimensions of the screen
        self.forestBackground = pygame.transform.scale(self.forestBackground, (w, h))
        self.display.fill('black')
        self.display.blit(self.forestBackground, (0,0))
        #draws all the text on the screen
        pygame.draw.rect(self.display, 'black', pygame.Rect(80, 200, 750, 400))
        screen.blit(self.text_surface, (100, 100))
        screen.blit(self.text_surface1, (100, 200))
        screen.blit(self.text_surface2, (100, 240))
        screen.blit(self.text_surface2cont, (100, 280))
        screen.blit(self.text_surface3, (100, 320))
        screen.blit(self.text_surface4, (100, 360))
        screen.blit(self.text_surface5, (100, 400))
        screen.blit(self.text_surface6, (100, 440))
        screen.blit(self.text_surface7, (100, 480))
        screen.blit(self.text_surface8, (100, 520))
        screen.blit(self.text_surface9, (100, 560))
        back_button.draw()
        

            

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #draws the background forest image
        self.forestBackground = pygame.image.load('./images/forest1.png')
        self.forestBackground = pygame.transform.scale(self.forestBackground, (1280, 736))
        pygame.font.init() 
        my_font = pygame.font.SysFont('Comic Sans MS', 60)
        #self.text_surface = my_font.render('Search For The Lost Skibidi', True, (255, 255, 255))
        self.text_surface = my_font.render('Search for the lost ark', True, (255, 255, 255))
        
        

    def run(self):
        w, h = pygame.display.get_surface().get_size()
        self.forestBackground = pygame.transform.scale(self.forestBackground, (w, h))
        self.display.fill('black')
        self.display.blit(self.forestBackground, (0,0))
        screen.blit(self.text_surface, (w/2-400,h/2-200))
        #draws all the buttons
        start_button.draw()
        stop_button.draw()
        help_button.draw()
        #print(pygame.mouse.get_pos())

class Death:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        #draws game over inmage
        self.over = pygame.image.load('./images/gameover2.jpg')
        self.over = pygame.transform.scale(self.over, (1280, 736))

    def run(self):
        w, h = pygame.display.get_surface().get_size()
        self.over = pygame.transform.scale(self.over, (w, h))
        self.display.fill('black')
        self.display.blit(self.over, (0,0))
        
        quit_btn.draw()

        

#-----------------Loading images for the buttons-----------------------------------------------------------------


start_img = pygame.image.load('./images/start.png').convert_alpha()

quit_img = pygame.image.load('./images/quit.png').convert_alpha()

end_img = pygame.image.load('./images/quit2.0.png').convert_alpha()

exit_img = pygame.image.load('./images/exit.png').convert_alpha()

back_img = pygame.image.load('./images/back.png').convert_alpha()

help_img = pygame.image.load('./images/help4.png').convert_alpha()


#----------------------------------------------------------------------------------------------------------------


#THis class takes in coordinates(x and y), and then rescales an image to the specified size
class Button:
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))



#--------------Buttons With Screen Width and Height----------------------------
w, h = pygame.display.get_surface().get_size()

start_button = Button(w*0.20, h*0.6, start_img, 0.2)

stop_button = Button(w*0.60, h*0.6, end_img, 0.2)

help_button = Button(w*0.40, h*0.6, help_img, 0.2)

quit_btn = Button(w*0.4, h*0.8, quit_img, 0.2)

back_button = Button(w*0.45, h*0.83, back_img, 0.25)
#----------------------------------------------------------------------------------

class GameStateManager:
    #sets the current state to whatever has been passed in 
    def __init__(self, currentState):
        self.currentState = currentState
    #returns whatever is set to current state
    def get_state(self):
        return self.currentState 
    # sets the current state to the new state passed in
    def set_state(self, state):
        self.currentState = state


if __name__ == '__main__':
    game = Game()
    game.run()