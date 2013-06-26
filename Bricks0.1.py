img_back='back.jpg'
img_pointer='pointer_brick.png'
img_ball='ball.png'
img_common_brick= 'common_brick.png'

start_game=False

SIZE_X=760 #max size 760x480
SIZE_Y=480

HANDL_POS = 0.8 * SIZE_Y

import pygame, sys, random, re
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((SIZE_X,SIZE_Y),0,32)

class brick:
    def __init__(self,crush=False,points=10,color=pygame.image.load(img_common_brick).convert()):
        self.crush=crush
        self.points=points
        #self.color=pygame.transform.scale(color,(int(SIZE_X*0.07),int(SIZE_Y*0.04)))
        self.color=color



background=pygame.image.load(img_back).convert()
mouse_c=pygame.image.load(img_pointer).convert()
ball = pygame.image.load(img_ball).convert()

def load_brick():   #setting the bricks
    Array_of_bricks=[]
    brick1=brick()
    f=open('sex.txt','r')
    line =0
    for coords in f.readlines():
        list_coords= re.findall(r'\d+',coords)
        column=0
        for coord in list_coords:
            if int(coord) is not 0:
                brick1.crush=False
                Array_of_bricks.append(brick1)
                screen.blit(brick1.color,(50+column*brick1.color.get_width(),50+line*brick1.color.get_height()))           
            if int(coord) is 0:
                brick1.crush=True
                Array_of_bricks.append(brick1)
                
            column=column+1
        line=line+1
        #screen.blit(brick1.color,(int(list_coords[0]),int(list_coords[1])))
        

def move_handler(): #moving the handler
        x= pygame.mouse.get_pos()[0] #y is const
        x = x - mouse_c.get_width()/2
        screen.blit(mouse_c,(x,HANDL_POS))
        return x


#movex, movey = 0,0

def display(movex,movey):
    x_ball,y_ball=SIZE_X/2,SIZE_Y/2

    while True:
        for event in pygame.event.get():  #quiting the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            
        screen.blit(background, (0,0))
        
        x_handler=move_handler()

        screen.blit(ball,(x_ball,y_ball))
        y_ball=y_ball+movey
        x_ball=x_ball+movex


        load_brick()        #drawing bricks
                
        pygame.display.update()
        #print('tova e x:: ',x)
        #print('tova e x_ball:: ',x_ball)
        #print('tova e mouse_c.get_width():: ', mouse_c.get_width())
        #if y_ball+ball.get_height()/2 == HANDL_POS - mouse_c.get_height()/2:
            #print('topcheto premina liniqta')
        if y_ball+ball.get_height()/2 >= HANDL_POS - mouse_c.get_height()/2 \
           and y_ball+ball.get_height()/2 < HANDL_POS - mouse_c.get_height()/2+1.5 \
           and x_ball + ball.get_width()/2 > x_handler \
           and x_ball < x_handler + mouse_c.get_width(): #the condition of bouncing
            print('topcheto se udrq v dryjkata')
            movey=-movey

        if y_ball < 0:
            print('topcheto se udrqrq v tavana')
            movey=-movey

        if x_ball < 0:
            print('topcheto se udrq v lqvata stena')
            movex=-movex

        if x_ball+ball.get_width() > SIZE_X:
            print('topcheto se udrq v dqsnata stena')
            movex=-movex                

        if y_ball+ball.get_height()/2 > SIZE_Y:
            
            print('Game Over')
            start_game = False
            break

    

while True:
    for event in pygame.event.get():  #quiting the game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            print('natisnal si mishkata, koeto znachi start na igrata')
            if not start_game:
                #start_game = False
                display(0,1.0) #max 5
                #display(0.01*random.randint(-150,150),0.01*random.randint(-150,150))
        pygame.draw.line(background,(0,0,0),(0,0),(SIZE_X,0),5)
        pygame.draw.line(background,(0,0,0),(SIZE_X,0),(SIZE_X,SIZE_Y),5)
        pygame.draw.line(background,(0,0,0),(0,SIZE_Y),(0,0),5)
        
                           
#setting the background
    screen.blit(background, (0,0)) 

#setting the mouse
    x,y= pygame.mouse.get_pos()
    x = x - mouse_c.get_width()/2
    y = y - mouse_c.get_height()/2
    
    screen.blit(mouse_c,(x,HANDL_POS))

#setting the ball
    screen.blit(ball,(SIZE_X/2,SIZE_Y/2))
      #  i=0
        #while pygame.mouse.get_pressed()==(1,0,0):
         #   screen.blit(ball,(size_x/2, size_y/2+i))
          #  i=i+1
           # pygame.display.update()        

#setting the bricks    
    brick1=brick()
    f=open('level1.txt','r')
    for coords in f.readlines():
        list_coords=re.findall(r'\d+',coords)
        screen.blit(brick1.color,(int(list_coords[0]),int(list_coords[1])))
    

    pygame.display.update() #updating the screen
    

