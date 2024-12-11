import pygame, sys
from pygame.locals import QUIT
import random
pygame.init()
screen = pygame.display.set_mode((800, 900))
background = pygame.image.load('background.png')
ground = pygame.image.load('groundpicture.png')
font = pygame.font.SysFont('sans',30)
#Restart = pygame.image.load('restart.png')
#screen.blit(background,(0,0))
starttime = pygame.time.get_ticks()
button = pygame.image.load('restart.png')
x=0
m = 0
start = 0
clicked = False
gameover = False
score = 0
scores = font.render('Score = ' +str(score),True,'black')
passed = False
stopscore = False
def restart():
    global start,score,angle
    start =0
    bird.rect.y = 450
    bird.rect.x = 25
    score = 0
    bird.velocity = 0
    pipes.empty()


class Bird(pygame.sprite.Sprite):#Bird is child class, sprite class is the parent class which is a template.
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.birdimages = []
        self.pictures = 0

        for i in range(1,4):
    
            self.birdimages.append(pygame.image.load('bird'+str(i)+'.png'))
        self.image = self.birdimages[self.pictures]
        self.rect = self.image.get_rect()
        self.delay = 0
        self.rect.center = x,y
        self.velocity = 0
    def update(self):
        global gameover,clicked,start
        #For the flying:
        #Introducing game physics
        
        if start == 1:
            self.velocity = self.velocity+0.3
            if self.velocity >=8:
                self.velocity = 8
            if self.rect.y <= 700:
                self.rect.y = self.rect.y+self.velocity
            self.delay = self.delay+1

            if self.delay>5:
                    self.delay = 0
                    self.pictures = self.pictures+1

                    if self.pictures == 3:
                        self.pictures = 0
        
       
        if gameover == False:

            if pygame.mouse.get_pressed()[0] == True and clicked == False:
                self.velocity = -6
                clicked = True
            elif pygame.mouse.get_pressed()[0] == False:
                
                clicked = False 
        #flapping the wings:

          
                
                    
                    
                self.image = self.birdimages[self.pictures]
                self.image = pygame.transform.rotate(self.birdimages[self.pictures],-2*self.velocity)
        else:
            
               
            self.image = pygame.transform.rotate(self.birdimages[self.pictures],-90)
        

class Button(pygame.sprite.Sprite):
    def __init__ (self,kx,ky):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('restart.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = kx,ky#missing step
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))#missing step#2
        
    

class Pipe(pygame.sprite.Sprite):
    def __init__ (self,x,y,position):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        if position == 0:#toppipe
            self.image = pygame.transform.flip(self.image,False,True)#to flip the pipe
            self.rect.bottomleft = x,y-100
        else:
            self.rect.topleft = x,y+100



    def update(self):
      self.rect.x = self.rect.x-5
      if self.rect.right <-10:
        self.kill()

    """def create(self):
        #pos = random.randint(0,400)
        #screen.blit(screen,(self.x,pos))"""
    """def move(self):
        pos = random.randint(0,400)
        screen.blit(screen,(self.x,pos))
        self.x  = self.x-5
        pygame.display.update()
        #if abs(self.x) == 35:
            #pos = random.randint(0,400)
            #self.x = 800"""

        

        
birdgroup = pygame.sprite.Group()
pipes  = pygame.sprite.Group()
button = Button(300,300)

bird = Bird(25,450)
birdgroup.add(bird)#now bird should have the properties of birgroups


pygame.display.set_caption('Flappy Bird')

print(birdgroup.sprites()[0].rect.left)

clock = pygame.time.Clock()
while True:
    screen.blit(background,(0,0))
    
    screen.blit(ground,(x,700))
    screen.blit(scores,(0,0))
    scores = font.render('Score = ' +str(score),True,'black')
    clock.tick(60)
   
    if gameover == False:
        x=x-1
        if abs(x) >35:
            
            x = 0
    birdgroup.draw(screen)
    
    birdgroup.update()
    if bird.rect.y <0 or pygame.sprite.groupcollide(birdgroup,pipes,False,False,):
        gameover = True
    if gameover == True:
        button.draw()
        pos = pygame.mouse.get_pos()
        if button.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True:
                restart()
                gameover = False

    if bird.rect.y >= 700:
        gameover = True
        start = 0 

        """if event.type == pygame.MOUSEBUTTONDOWN:
            nx, ny = pygame.mouse.get_pos()
                mouserect = pygame.Rect(nx,ny,10,10)
            if mouserect.colliderect():
                        restart()"""

    #birdgroup.update()
    currenttime = pygame.time.get_ticks()
    y = random.randint(-100,100)
    if gameover == False:#FIX PIPES,
        if currenttime-starttime >= 1500 and start ==1 :
            bottompipe = Pipe(800,350+y,1234567)
            toppipe = Pipe(800,350+y,0)
            pipes.add(toppipe)
            pipes.add(bottompipe)
            starttime = currenttime
    
#Whole update function behind the if condition. 
    
        if start == 1:
            pipes.update()
    pipes.draw(screen)
    """if len(pipes) >=1:
        if birdgroup.sprites()[0].rect.left > pipes.sprites()[m].rect.right and stopscore == False :
            passed = True
            stopscore = True

        if passed == True:
            score = score+0.5
            m=m+1
            passed = False
            stopscore = False
            print(score)
            #print('M is '+str(m))
        if birdgroup.sprites()[0].rect.left > pipes.sprites()[m].rect.right and stopscore == True:
            stopscore = False"""
    if len(pipes) >=1:
        if birdgroup.sprites()[0].rect.left > pipes.sprites()[0].rect.left and birdgroup.sprites()[0].rect.right < pipes.sprites()[0].rect.right and passed == False:
            passed = True

        if passed == True:
            
            if birdgroup.sprites()[0].rect.left > pipes.sprites()[0].rect.right:
                score = score+1
                m=m+1
                print(score)
                passed = False
        print(passed)
        print(birdgroup.sprites()[0].rect.left,pipes.sprites()[0].rect.left)
        print(birdgroup.sprites()[0].rect.right, pipes.sprites()[0].rect.right)



            
            
       



        




    for event in pygame.event.get():
        if event.type == QUIT:
           pygame.quit()
           sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and start == 0 and gameover == False:
            start = 1
            
        
        
           
        
    pygame.display.update()
