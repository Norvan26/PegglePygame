import pygame 
import sys
import os
import random
import math
#from debug import *

FPS = 60
image_folder = os.path.join("images")

PEG_RADIUS = 8
ball_radius = 8
clock = pygame.time.Clock()


pygame.init()
pygame.font.init()
pygame.mixer.init()

class Level:
    def __init__(self, display, map, monsters, playerHealth, fruits):
        #assigning the variables passed in to variables within the class
        self.display = display
        self.playerHealth = playerHealth
        self.pegMap = map
        self.fruits = fruits
        #random number to decide what fruit is given to the user
        self.rand = random.randint(0,5)
        
        
        #--------------Variables used as flags in the if statements---------------------------------
        self.exit = False
        self.canMove = False
        self.addedFruit = False
        self.H = 736
        self.emptyspace = False
        self.notShooting = True
        self.shot = False
        self.exist = True
        self.killed = False
        self.death = False
        self.firstenter = True
        #--------------------------Monster Positions and creating instance of monster class
        self.monster_list = []

        for monster in monsters:
            self.monster_list.append(Monster(monster, 100, 2))

        self.monsterNum = 1
        #all the possible positions of the enmey with the first position being filled with the first enemy
        self.positions = [[200, 'x'], [300, 'x'], [400, 'x'], [500, 'x'], [600, 'x'], [700, 'x'], [800, 'x'], [900, 'x'], [1000, 'x'], [1100, self.monster_list[0]], [1200, 'x']]
        #get the amount of monster depending on the length of the list
        self.monsterAmount = len(self.monster_list)
        #-----------------LOading images---------------------------------------------------

        self.scroll = pygame.image.load('./images/scroll.png')

        self.scroll = pygame.transform.scale(self.scroll, (850, 750))

        self.exitBTN = pygame.image.load('./images/exit.png')
        self.exit = Button(600, 600, self.exitBTN, 0.2)


        self.grassMidOG1 = pygame.image.load('./images/leaf.jpg')
        self.grassMid1 = pygame.transform.scale(self.grassMidOG1, (64, 64))

        self.finalFormForest = pygame.image.load('./images/forest.png')
        self.finalFormForest = pygame.transform.scale(self.finalFormForest, (275, 200))

        self.wall = pygame.image.load('./images/peglinwall.png')
        self.wall = pygame.transform.scale(self.wall, (64, 64))



        self.wood = pygame.image.load('./images/wooden.jpeg')

        self.wood = pygame.transform.scale(self.wood, (256, 128))

        self.reloadBtn = pygame.image.load('./images/reload.png')

        self.backdrop = pygame.image.load('./images/goated2.0.png')
        self.backdrop = pygame.transform.scale(self.backdrop, (800, 600))


        
        #------------------------------------------
        
        self.i = 0
        #gets the mouses position
        self.pos = pygame.mouse.get_pos()
        self.n = 0
        #list of all the balls shot
        self.ball_list = []
        #a temp variable to score the points of the player after hitting pegs
        self.temp = 0

        #defining different sprite groups
        self.projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        #used to contain only pegs to be used for checking collisions
        self.pegs = pygame.sprite.Group()

        #create an inital ball when the player first begins the level
        self.ball = Ball(800, 250)
        #adds it to all sprites to be drawn
        self.all_sprites.add(self.ball)
        self.opacitiy_list = pygame.sprite.Group()
        self.allowed_resets = 0
        self.idle_sprites = pygame.sprite.Group()
        self.aiming = pygame.sprite.Group()
        self.player = Player(100,65)
        self.idle_sprites.add(self.player)

        #sets the level to being initially not muted 
        self.muted = False




        #-----------LOADING SOUNDS--------------------
        self.entered = pygame.mixer.Sound('entersound.wav')
        self.music = pygame.mixer.Sound('mainmusic.wav')


        self.hurt = pygame.mixer.Sound('punch.mp3')
        self.ping = pygame.mixer.Sound('ping.wav')
        #-----------fruit controls--------------------


        #self.allFruits = ['potato', 'apple', 'plum']
       #cretiung the three fruit slots based on the fruit list passed in
        self.fruit1 = DevilFruit(self.fruits[0], 80, 630, 64, 64)

        self.fruit2 = DevilFruit(self.fruits[1], 150, 630, 64, 64)

        self.fruit3 = DevilFruit(self.fruits[2], 220, 630, 64, 64)

        #create list of all fruits
        self.devilFruits = [self.fruit1, self.fruit2, self.fruit3]


        #pygame.mixer.Sound.play(self.collide)
        #pygame.mixer.music.stop()

        #create instance of aim class
        self.aim = Aim()
        #add it to aiming sprite class so it can be drawn alter in the program
        self.aiming.add(self.aim)

        #creates surface for having the game being with a black screen and slowly fade in
        self.s = pygame.Surface((3000,2000))
        
        self.s.fill((0,0,0)) 
        #--------------------creates the layout for pegs------------------------
        #goes through each row in the list
        for i in range(len(self.pegMap)):
            #goes through each item in each row
            for j in range(len(self.pegMap[i])):
                #moves x over 40 pixels each time and down 40 pixels each time
                x = (40 + j * 20)+ 400
                y = (self.H - 40 - i * 20 ) - 20
                # if the value in the list is r then an instance of my peg is created and reset is passed in for type
                if self.pegMap[i][j] == 'r':
                    peg = Peg(x, y, 0, 'reset')
                    #an instance of peg class is created with normal for type so it is white but 40 passed in for some opacity
                    invisiPeg = Peg(x, y, 40, 'normal')
                    self.all_sprites.add(peg)
                    self.all_sprites.add(invisiPeg)
                    self.pegs.add(peg)

                # if the value in the list is r then an instance of my peg is created and bomb is passed in for type
                elif self.pegMap[i][j] == 'b':
                        peg = Peg(x, y, 0, 'bomb')
                        #an instance of peg class is created with normal for type so it is white but 40 passed in for some opacity
                        invisiPeg = Peg(x, y, 40, 'normal')
                        self.all_sprites.add(peg)
                        self.all_sprites.add(invisiPeg)
                        self.pegs.add(peg)
                    
                    
                # if the value in the list is r then an instance of my peg is created and normal is passed in for type
                elif self.pegMap[i][j] == 'x':
                    peg = Peg(x, y, 0, 'normal')
                    #an instance of peg class is created with normal for type so it is white but 40 passed in for some opacity
                    invisiPeg = Peg(x, y, 40, 'normal')
                    self.all_sprites.add(peg)
                    self.all_sprites.add(invisiPeg)
                    self.pegs.add(peg)
                

    def run(self):
        clock.tick(60)
        
        self.pos = pygame.mouse.get_pos()
        #-------------------------------------------------------------------------------------------------------------------
        keys = pygame.key.get_pressed()



        #------------plays the sound when level is first entered and the variable prevents the sound from repeatedly playing------------------------
        if self.firstenter == True:
            self.firstenter = False
            pygame.mixer.Sound.play(self.entered)
            pygame.mixer.music.stop()





        #pygame.mixer.Sound.play(self.music)
        #pygame.mixer.music.stop()
        
        
        self.display.fill((22,22,22,255))

        #blits the backdrop on the screen at coordinates 400,200
        self.display.blit(self.backdrop, (400,200))
        
        
        self.x = 0
        
        self.display.blit(self.finalFormForest, (0,0))
        
        #repeatedly draws the forest background as it is not long enough to cover the whole screen as well as the walls and the grass
        self.forested = 0
        for n in range(11):
            self.forested +=1
            self.display.blit(self.finalFormForest, (self.forested*275,0))
        self.walled = 2
        for n in range(15):
            self.walled += 1
            self.display.blit(self.wall, (336, self.walled*64))
            self.display.blit(self.wall, (1200, self.walled*64))
        self.grassYLoc = 168
        for n in range(39):
            #self.display.blit(self.grassMid, (self.x*32, self.grassYLoc))
            self.display.blit(self.grassMid1, (self.x*64, self.grassYLoc))
            self.x+=1


        #------------------------------side bar UI----------------------------------------------------------------------------

        #turns the players health to a string
        self.str = str(self.playerHealth)
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        #draws the players health as text above the health bar
        self.text_surface = my_font.render(self.str, True, (255, 255, 255))

        #draws the players health in green and has the width as the amount of health left and then a red bar behind it which dimensions dont change
        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(75, 300, 200, 25))
        pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(75, 300, self.playerHealth, 25))


        self.display.blit(self.text_surface, (110,250))


        if self.playerHealth <= 0:
            #self.gameStateManager.set_state('over')
            pass
            
        

        #-------------------------------------------------------------------------------------------------------------------
        
       
        if self.ball.check_reset():
            self.num1 = random.randint(0,7)
            self.num2 = random.randint(0,23)
            self.ye = False
           
            for peg in self.pegs:
                peg.kill()
            
            for i in range(len(self.pegMap)):
                for j in range(len(self.pegMap[i])):
                    x = (40 + j * 20 )+ 400
                    y = (self.H - 40 - i * 20 ) - 20

                    if self.num1 == i and self.num2 == j:
                        self.ye = True
                    if self.pegMap[i][j] == 'x' and self.ye:
                        peg = Peg(x, y, 0, 'reset')
                        self.all_sprites.add(peg)
                        self.pegs.add(peg)
                        self.ye = False

                    elif self.pegMap[i][j] == 'x' or self.pegMap[i][j] == 'r':
                        peg = Peg(x, y, 0, 'normal')
                        self.all_sprites.add(peg)
                        self.pegs.add(peg)

                    elif self.pegMap[i][j] == 'b':
                        peg = Peg(x, y, 0, 'bomb')
                        self.all_sprites.add(peg)
                        self.pegs.add(peg)

        #-------------------------------------------------------------------------------------------------------------------
        #checks keys pressed
        self.key = pygame.key.get_pressed()

#------------------------------------fruits-------------------------------------------------------------------

        #draws image of wood
        self.display.blit(self.wood, (50,600))
        
        #for the instances of the Devilfruits class in the fruits list it will call the draw method
        for fruit in self.devilFruits:
            fruit.draw()


           # if fruit.activated() == True:
            #    self.devilFruits[0].deactivate()
             #   self.devilFruits[1].deactivate()
             #   self.devilFruits[2].deactivate()
              #  fruit.activation()

            

        if self.notShooting == True and self.monsterAmount > 0:
            
            for fruit in self.devilFruits:
                fruit.get_click()


            if self.devilFruits[0].activated() == True:
                self.devilFruits[1].deactivate()
                self.devilFruits[2].deactivate()

            if self.devilFruits[1].activated() == True:
                self.devilFruits[0].deactivate()
                self.devilFruits[2].deactivate()

            if self.devilFruits[2].activated() == True:
                self.devilFruits[0].deactivate()
                self.devilFruits[1].deactivate()

#-----------------#player animations and update drawing sprites-----------------------------------------------------------------------------------------------------------------------------


        #print(self.rand)
        
        self.aiming.draw(self.display)
        self.aiming.update()


        self.aim.draw(self.display)


        self.idle_sprites.draw(self.display)

        self.idle_sprites.update(0.1)

        self.all_sprites.draw(self.display)

        self.all_sprites.update()

        

        self.n = self.n + 1.5

        self.s.set_alpha(255 - self.n)
        self.display.blit(self.s, (0,0)) 

        #---------------------------------------------------



        if self.monsterAmount <= 0:
            self.my_font = pygame.font.SysFont('Comic Sans MS', 20)
            addition = ['apple', 'potato', 'plum', 'blueberry', 'red', 'pear']
            self.aim.stop_shooting()

            self.display.blit(self.scroll, (250,-50))
            self.exit.draw()

            if self.addedFruit == False:
                self.rect1 = pygame.draw.rect(self.display, 'grey', pygame.Rect(550, 450, 60, 60))
                self.rect2 = pygame.draw.rect(self.display, 'grey', pygame.Rect(650, 450, 60, 60))
                self.rect3 = pygame.draw.rect(self.display, 'grey', pygame.Rect(750, 450, 60, 60))

            self.col1 = self.rect1.collidepoint(self.pos)
            self.col2 = self.rect2.collidepoint(self.pos)
            self.col3 = self.rect3.collidepoint(self.pos)


            if pygame.mouse.get_pressed()[0] and self.col1 and self.addedFruit == False:
                self.fruits[0] = addition[self.rand]
                self.addedFruit = True
                print(self.fruits)
                

            if pygame.mouse.get_pressed()[0] and self.col2 and self.addedFruit == False:
                self.fruits[1] = addition[self.rand]
                self.addedFruit = True
                print(self.fruits)

            if pygame.mouse.get_pressed()[0] and self.col3 and self.addedFruit == False:
                self.fruits[2] = addition[self.rand]
                self.addedFruit = True
                print(self.fruits)



            additionFruit = DevilFruit(addition[self.rand], 600, 200, 200, 200)
            additionFruit.draw()

            self.text_surface = self.my_font.render('Add/Replace a slot', True, (0, 0, 0))
            self.display.blit(self.text_surface, (590, 400))
 
            self.collidingExit = self.exit.rect.collidepoint(self.pos)
            if self.collidingExit and pygame.mouse.get_pressed()[0]:
                pygame.mixer.Sound.play(self.ping)
                pygame.mixer.music.stop()
                #self.gameStateManager.set_state('map')
                self.exit = True
                self.monsterAmount = 4






            
#-------------------collisions and moving enemies---------------------------------------------------------------------------------------------
       
        self.ball.collisionGoat(self.ball, self.pegs, self.all_sprites)

        if pygame.mouse.get_pressed()[0] and self.notShooting == True and (255-self.n) < 60 and self.pos[0] > 330 and self.monsterAmount > 0:
            self.ball.shoot()
            self.notShooting = False
            self.shot = True
            


        if self.notShooting == False:
            self.aim.stop_shooting()

        elif self.monsterAmount > 0:
            self.aim.start_shooting()

        #if self.key[pygame.K_z] == True and self.shot == True and self.exist == False:
        if self.killed == True and self.shot == True and self.exist == False:
            self.ball = Ball(800, 250)
            self.all_sprites.add(self.ball)
            self.shot = False
            self.exist = True
            self.notShooting = True
            self.killed = False
            self.aim.start_shooting

       # if self.key[pygame.K_k] == True:
           # self.gameStateManager.set_state('map')

        if self.ball.rect.y > 1000 and self.exist == True:
            #print('entered123213123')
            self.exist = False
            self.killed = True
            self.temp = self.ball.scoring()
            self.ball.kill()  
            self.canMove = True
            

        self.first = True

        for monster in self.positions:
                
                if monster[1] != 'x':
                    monster[1].draw_monster(monster[0])
                    self.none = False


                    if self.first == True:
                        monster[1].set_health(self.temp)
                        self.first = False  

                    self.temp = self.temp*0

        if self.canMove:
            self.canMove = False
            self.exist = False
            self.shot = True

            for i in range(len(self.positions)):
                if self.monsterNum < len(self.monster_list):
                    #print(self.positions[6])
                    if self.positions[10][1] == 'x':
                        self.positions[10][1] = self.monster_list[self.monsterNum]
                        self.monsterNum = self.monsterNum + 1
                
         

                if self.positions[i][1] != 'x':
                    #print(self.positions[i][1].get_health())
                    if self.positions[i][1].get_health() <= 0:    
                        self.positions[i][1] = 'x'
                        #print('killed')
                        self.monsterAmount = self.monsterAmount - 1

                    elif i != 0:    
                        if self.positions[i][1] != 'x':
                            
                            if self.positions[i-1][1] == 'x':
                                self.positions[i-1][1] = self.positions[i][1]
                                self.positions[i][1] = 'x'

            if self.positions[0][1] != 'x':
                    #print('yoooo')
                    self.playerHealth = self.playerHealth - 5
                    pygame.mixer.Sound.play(self.hurt)
                    self.hurt.set_volume(0.2)
                    pygame.mixer.music.stop()

            if self.playerHealth <= 0:
                self.death = True

    def exit_code(self):
        return[self.exit, self.playerHealth, self.death, self.fruits]
                        

                    


#----------------------------------------------------------------------------------------------------------------------------------------


class Button:
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        self.display_surface.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprites = []

        #loads images

        self.char1 = pygame.image.load('./images/IdleSwordOutline_01.png')
        self.char1 = pygame.transform.scale(self.char1, (150, 138))
        self.char2 = pygame.image.load('./images/IdleSwordOutline_02.png')
        self.char2 = pygame.transform.scale(self.char2, (150, 138))
        self.char3 = pygame.image.load('./images/IdleSwordOutline_03.png')
        self.char3 = pygame.transform.scale(self.char3, (150, 138))
        self.char4 = pygame.image.load('./images/IdleSwordOutline_04.png')
        self.char4 = pygame.transform.scale(self.char4, (150, 138))

        self.sprites.append(self.char1)
        self.sprites.append(self.char2)
        self.sprites.append(self.char3)
        self.sprites.append(self.char4)
        
        self.current = 0
        self.image = self.sprites[self.current]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def update(self, speed):
        self.current +=speed
        if True:
            if self.current >= len(self.sprites):
                self.current = 0
            self.image = self.sprites[int(self.current)]

        


class Monster:

    def __init__(self, type, health, level):
        #loading images
        self.slime = pygame.image.load('./images/blobLeft.png')
        self.orb = pygame.image.load('./images/blueOrb.png')
        self.spider = pygame.image.load('./images/spider.png')
        self.display_surface = pygame.display.get_surface()
        self.type = type
        self.health = health
        self.level = level
        self.spriteNum = 0


        self.str = str(health)
        self.my_font = pygame.font.SysFont('Comic Sans MS', 20)
        

        self.sprites = []

        self.sk1 = pygame.image.load('./images/eyeball1.png')
        self.sk2 = pygame.image.load('./images/eyeball2.png')
        self.sk3 = pygame.image.load('./images/eyeball3.png')
        self.sk4 = pygame.image.load('./images/eyeball4.png')

        self.sk1 = pygame.transform.flip(self.sk1, True, False) 
        self.sk2 = pygame.transform.flip(self.sk2, True, False) 
        self.sk3 = pygame.transform.flip(self.sk3, True, False) 
        self.sk4 = pygame.transform.flip(self.sk4, True, False) 

        self.sprites.append(self.sk1)
        self.sprites.append(self.sk2)
        self.sprites.append(self.sk3)
        self.sprites.append(self.sk4)



        #------------------------------------------------------------------------------------------

        self.slimeAnimation = []

        self.slimeNum = 0

        self.slime1 = pygame.image.load('./images/slime1.png')
        self.slime1 = pygame.transform.scale(self.slime1, (30, 28))
        self.slime2 = pygame.image.load('./images/slime2.png')
        self.slime2 = pygame.transform.scale(self.slime2, (30, 28))
        self.slime3 = pygame.image.load('./images/slime3.png')
        self.slime3 = pygame.transform.scale(self.slime3, (30, 28))
        self.slime4 = pygame.image.load('./images/slime4.png')
        self.slime4 = pygame.transform.scale(self.slime4, (30, 28))
        self.slime5 = pygame.image.load('./images/slime5.png')
        self.slime5 = pygame.transform.scale(self.slime5, (30, 28))
        self.slime6 = pygame.image.load('./images/slime6.png')
        self.slime6 = pygame.transform.scale(self.slime6, (30, 28))
        self.slime7 = pygame.image.load('./images/slime7.png')
        self.slime7 = pygame.transform.scale(self.slime7, (30, 28))
        self.slime8 = pygame.image.load('./images/slime8.png')
        self.slime8 = pygame.transform.scale(self.slime8, (30, 28))
        self.slime9 = pygame.image.load('./images/slime9.png')
        self.slime9 = pygame.transform.scale(self.slime9, (30, 28))
        self.slime10 = pygame.image.load('./images/slime10.png')
        self.slime10 = pygame.transform.scale(self.slime10, (30, 28))


        self.slimeAnimation.append(self.slime1)
        self.slimeAnimation.append(self.slime2)
        self.slimeAnimation.append(self.slime3)
        self.slimeAnimation.append(self.slime4)
        self.slimeAnimation.append(self.slime5)
        self.slimeAnimation.append(self.slime6)
        self.slimeAnimation.append(self.slime7)
        self.slimeAnimation.append(self.slime8)
        self.slimeAnimation.append(self.slime9)
        self.slimeAnimation.append(self.slime10)
        


        #-----------------------------------------------------------------------------------------------


        

    def draw_monster(self, n):

        self.n = n
        # draws health if it is less than 100 bu greater than 0
        if self.health < 100 and self.health > 0:
            pygame.draw.rect(self.display_surface, (255, 0, 0), pygame.Rect(self.n - 10, 136, 50, 5))
            pygame.draw.rect(self.display_surface, (0, 255, 0), pygame.Rect(self.n - 10, 136, self.health/2, 5))
            self.text_surface = self.my_font.render(str(self.health)+'/'+self.str, True, (255, 255, 255))
            self.display_surface.blit(self.text_surface, (self.n - 20, 106))

            
        #draw monster depending on what string is passed in for self.type
        if self.type == 'eye':
            self.spriteNum = self.spriteNum + 0.05
            if self.spriteNum >= 3:
                self.spriteNum = 0
            self.display_surface.blit(self.sprites[int(self.spriteNum)], (self.n, 140))
                    
            

        if self.type == 'slime':
            self.slimeNum = self.slimeNum + 0.1
            if self.slimeNum >= 9:
                self.slimeNum = 0
            self.display_surface.blit(self.slimeAnimation[int(self.slimeNum)], (self.n, 140))

        if self.type == 'orb':
            self.display_surface.blit(self.orb, (self.n, 136))

    def get_health(self):
        return(self.health)



    def set_health(self, health):
        self.health = self.health - health

#--------------------------------------------------


class DevilFruit:

    def __init__(self, type, x, y, sx, sy):
        #loads images
        self.apple = pygame.image.load('./images/apple.png')
        self.apple = pygame.transform.scale(self.apple, (sx, sy))
        self.potato = pygame.image.load('./images/potato.png')
        self.potato = pygame.transform.scale(self.potato, (sx, sy))
        self.plum = pygame.image.load('./images/plum.png')
        self.plum = pygame.transform.scale(self.plum, (sx, sy))
        self.blueberry = pygame.image.load('./images/blueberry.png')
        self.blueberry = pygame.transform.scale(self.blueberry, (sx, sy))
        self.red = pygame.image.load('./images/red.png')
        self.red = pygame.transform.scale(self.red, (sx-10, sy))
        self.pear = pygame.image.load('./images/pear.png')
        self.pear = pygame.transform.scale(self.pear, (sx, sy))


        self.display_surface = pygame.display.get_surface()
        self.type = type
        #sets pos to the x and y value passed in
        self.pos =[x, y]
        self.activate = False
        self.text = False
        self.active = False
               
        self.my_font = pygame.font.SysFont('Comic Sans MS', 20)
        
        
    

    def draw(self):
        self.mousepos = pygame.mouse.get_pos()
        #draws the fruit depending on the type passed in

        if self.type == 'apple':
            self.rect = self.apple.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])
            self.display_surface.blit(self.apple, (self.rect))   
            if self.text == True:
                self.name = self.my_font.render('Celestia Apple', True, (255, 255, 255))
                self.text_surface = self.my_font.render('This was taken from a god', True, (255, 255, 255))
                self.display_surface.blit(self.text_surface, (70, 400))  
                self.display_surface.blit(self.name, (70, 350))  

        if self.type == 'potato':
            self.rect = self.potato.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])
            self.display_surface.blit(self.potato, (self.rect))
            if self.text == True:
                self.name = self.my_font.render('Potato', True, (255, 255, 255))
                self.text_surface = self.my_font.render('This is a potato.', True, (255, 255, 255))
                self.display_surface.blit(self.text_surface, (70, 400))
                self.display_surface.blit(self.name, (70, 350))


        if self.type == 'plum':
            self.rect = self.plum.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])
            self.display_surface.blit(self.plum, (self.rect))
            if self.text == True:
                self.name = self.my_font.render('Shadowmoss Melon', True, (255, 255, 255))
                self.text_surface = self.my_font.render('Found in the darkest depths', True, (255, 255, 255))
                self.display_surface.blit(self.text_surface, (70, 400))
                self.display_surface.blit(self.name, (70, 350))

        if self.type == 'blueberry':
            self.rect = self.blueberry.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])
            self.display_surface.blit(self.blueberry, (self.rect))
            if self.text == True:
                self.name = self.my_font.render('Sapphireberry', True, (255, 255, 255))
                self.text_surface = self.my_font.render('This is a freeze fruit', True, (255, 255, 255))
                self.display_surface.blit(self.text_surface, (70, 400))
                self.display_surface.blit(self.name, (70, 350))


        if self.type == 'red':
            self.rect = self.red.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])
            self.display_surface.blit(self.red, (self.rect))
            if self.text == True:
                self.name = self.my_font.render('Enchanted Seraphberry', True, (255, 255, 255))
                self.text_surface = self.my_font.render('This is a flame fruit', True, (255, 255, 255))
                self.display_surface.blit(self.text_surface, (70, 400))
                self.display_surface.blit(self.name, (70, 350))
                

        if self.type == 'pear':
            self.rect = self.pear.get_rect()
            self.rect.topleft = (self.pos[0], self.pos[1])
            self.display_surface.blit(self.pear, (self.rect))
            if self.text == True:
                self.name = self.my_font.render('Elderglow Citrus', True, (255, 255, 255))
                self.text_surface = self.my_font.render('This is a mythical zoan type', True, (255, 255, 255))
                self.display_surface.blit(self.text_surface, (70, 400))
                self.display_surface.blit(self.name, (70, 350))

        

    
    def get_click(self):
        #gets the users click and then displays appropriate text
        self.active = False
        if self.type == 'apple':
            self.collision = self.rect.collidepoint(self.mousepos)

            #print(rect)
            if self.collision and pygame.mouse.get_pressed()[0]:
              self.text = True
              self.active = True



        if self.type == 'potato':
            self.collision = self.rect.collidepoint(self.mousepos)

            if self.collision and pygame.mouse.get_pressed()[0]:
              self.text = True
              self.active = True
              

        if self.type == 'plum':
            self.collision = self.rect.collidepoint(self.mousepos)

            if self.collision and pygame.mouse.get_pressed()[0]:
              self.text = True
              self.active = True

        if self.type == 'blueberry':
            self.collision = self.rect.collidepoint(self.mousepos)

            if self.collision and pygame.mouse.get_pressed()[0]:
              self.text = True
              self.active = True

        if self.type == 'red':
            self.collision = self.rect.collidepoint(self.mousepos)

            if self.collision and pygame.mouse.get_pressed()[0]:
              self.text = True
              self.active = True


        if self.type == 'pear':
            self.collision = self.rect.collidepoint(self.mousepos)

            if self.collision and pygame.mouse.get_pressed()[0]:
              self.text = True
              self.active = True
        

              


    def activated(self):
        return(self.active)

    def deactivate(self):
        self.active = False
        self.text = False






class Aim(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800, 600), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.pos = pygame.mouse.get_pos()
        self.direction = [self.pos[0] - 800, self.pos[1] - 250]
        self.magnitude = max(1, math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2))
        self.direction = [self.direction[0] / self.magnitude, self.direction[1] / self.magnitude]
        self.velocity = [self.direction[0] * 10, self.direction[1] * 10]
        self.shooting = True
        self.points = []

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.direction = [self.pos[0] - 800, self.pos[1] - 250]
        self.magnitude = max(1, math.sqrt(self.direction[0] ** 2 + self.direction[1] ** 2))
        self.direction = [self.direction[0] / self.magnitude, self.direction[1] / self.magnitude]
        self.velocity = [self.direction[0] * 10, self.direction[1] * 10]
        self.calculate_trajectory()

    def calculate_trajectory(self):
        if self.shooting:
            self.points.clear()
            pos = [800, 250]
            velocity = list(self.velocity)  # Copy velocity
            gravity = 0.4
            friction = 0.995
            for x in range(45):  # Adjust iterations as needed
                self.points.append(pos.copy())
                pos[0] += velocity[0]
                pos[1] += velocity[1]
                velocity[1] += gravity
                velocity[0] *= friction
                velocity[1] *= friction

    def start_shooting(self):
        self.shooting = True

    def stop_shooting(self):
        self.shooting = False

    
    def draw(self, surface):
        if self.shooting:
            pygame.draw.lines(surface, (255, 255, 255), False, self.points)
        

class Peg(pygame.sprite.Sprite):
    def __init__(self, x, y, n, name):
        super().__init__()
        self.image = pygame.Surface((PEG_RADIUS*2, PEG_RADIUS*2), pygame.SRCALPHA)
        self.name = name
        self.numCol = 0
        if n > 0:
            self.image.set_alpha(n)
        if self.name == 'normal':
            pygame.draw.circle(self.image, (255,255,255), (PEG_RADIUS, PEG_RADIUS), PEG_RADIUS)

        if self.name == 'reset':
            pygame.draw.circle(self.image, (197,228,61,255), (PEG_RADIUS, PEG_RADIUS), PEG_RADIUS)

        if self.name == 'bomb':
            pygame.draw.circle(self.image, (0, 0, 255), (PEG_RADIUS, PEG_RADIUS), PEG_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))
    
    def get_name(self):
        return(self.name)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #creates the image of the ball
        self.image = pygame.Surface((ball_radius*2, ball_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (ball_radius, ball_radius), ball_radius)
        #gets the balls rect
        self.rect = self.image.get_rect(center=(x, y))
        #creates initial ball values
        self.velocity = [0,0]
        self.gravity = 0.4
        self.friction = 0.9999
        self.reflect_friction = 10
        self.display_surface = pygame.display.get_surface()
        #print('hello')
        #flag to check if the ball has been shot
        self.isShot = False
        self.score = 0
        self.reset = False
        self.score = 0
        #loads the sounds
        self.collide = pygame.mixer.Sound('collide.wav')
        self.bomb = pygame.mixer.Sound('bomb.wav')
        self.rem = False

    def update(self):
        self.pos = pygame.mouse.get_pos()
        # if the ball is shot it applies the friction and gravity
        if self.isShot:
            self.velocity[1] = (self.velocity[1] + self.gravity)*0.9999
        #self.velocity[0] = self.velocity[0]*self.friction
        #print(self.velocity)
        # moves the ball according to values of velocity
        self.rect.move_ip(self.velocity)
        self.check_boundaries()

    def check_boundaries(self):
        self.num = random.uniform(-0.1, 0.1)

        #checks if ball collides with the side of the walls then flips the value of the velocity so it is reflected
        if self.rect.left < 400:
            self.velocity[0] = self.velocity[0]*-1 + self.num

            if self.rect.left < 400:
                self.rect.left = 400


        
        if self.rect.right > 1200:
            self.velocity[0] = self.velocity[0]*-1 + self.num

            if self.rect.right > 1200:
                self.rect.right = 1200

        if self.rect.top < 215:
            self.velocity[1] = self.velocity[1]*-1 + self.num

        #if self.rect.bottom > 700:
         #  self.velocity[1] = self.velocity[1]*-1

    
    def shoot(self):
        self.score = 0
        self.isShot = True
        self.pos = pygame.mouse.get_pos()
        #self.direction = [self.pos[0] - self.rect.centerx, self.pos[1]- self.rect.centerx]
        #calculates the direction from the users mouse position
        self.direction = [self.pos[0] - 800, self.pos[1]- 250]

        self.magnitude = math.sqrt(self.direction[0]**2 + self.direction[1]**2)
        self.direction = [self.direction[0] / self.magnitude, self.direction[1] / self.magnitude]
        self.velocity[0] = self.direction[0]*10
        self.velocity[1] = self.direction[1]*10

    #if the reset peg has been hit it returns true whihc then controls the if statement that deletes all the pegs and redraws the peg layout
    def check_reset(self):
        if self.reset == True:
            self.reset = False
            return(True)
        
    def check_bomb(self):

        if self.rem == True:
            self.rem = False
            return(True)
        
    def scoring(self):
        #returns the score
        return(self.score)
    
    def collisionGoat(self, ball, pegs, sprites):

        self.colliding = pygame.sprite.spritecollide(ball, pegs, False)

        self.num1 = random.uniform(-0.1, 0.1)
        self.num2 = random.uniform(-0.1, 0.1)

        if self.colliding:
            pygame.mixer.Sound.play(self.collide)
            pygame.mixer.music.stop()
            self.reflect_friction = self.reflect_friction*self.friction
            self.score = self.score + 3

            for peg in self.colliding:
                self.checkdir = [self.rect.centerx - peg.rect.centerx, self.rect.centery - peg.rect.centery]
                self.checkmagnitude = math.sqrt(self.checkdir[0]**2 + self.checkdir[1]**2)
                self.checkdir = [self.checkdir[0] / self.checkmagnitude, self.checkdir[1] / self.checkmagnitude]

                num = random.randint(0,2)

                if peg.get_name() == 'reset':
                    self.reset = True

                elif peg.get_name() == 'bomb':
                    self.direction = [self.rect.centerx - peg.rect.centerx, self.rect.centery - peg.rect.centery]
                    self.direction[0] = self.direction[0] + self.num1
                    self.direction[1] = self.direction[1] + self.num2
                    self.magnitude = math.sqrt(self.direction[0]**2 + self.direction[1]**2)
                    self.direction = [self.direction[0] / self.magnitude, self.direction[1] / self.magnitude]
                    self.velocity[0] = self.direction[0]*15
                    self.velocity[1] = self.direction[1]*15
                    pygame.mixer.Sound.play(self.bomb)
                    pygame.mixer.music.stop()
                    self.score = self.score + 10
                    self.rem = True
                    peg.kill()

                

                elif self.checkdir[0] == 0 and (self.velocity[0] > 0.6 or self.velocity[0] < -0.6):
                    self.velocity[0] = -(self.velocity[0] - 0.005)
                    #self.velocity[1] = -self.velocity[1]
                    peg.kill()

                else:
                    self.direction = [self.rect.centerx - peg.rect.centerx, self.rect.centery - peg.rect.centery]
                    self.direction[0] = self.direction[0] + self.num1
                    self.direction[1] = self.direction[1] + self.num2
                    self.magnitude = math.sqrt(self.direction[0]**2 + self.direction[1]**2)
                    self.direction = [self.direction[0] / self.magnitude, self.direction[1] / self.magnitude]
                    self.velocity[0] = self.direction[0]*self.reflect_friction
                    self.velocity[1] = self.direction[1]*int(9)
                    peg.kill()           