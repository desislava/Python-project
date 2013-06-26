import shelve
import pygame, sys, random, re
from pygame.locals import *
from datetime import datetime
from tkinter import *

img_back='back.jpg'
img_pointer='pointer_brick.png'
img_ball='ball.png'
img_common_brick= 'common_brick.png'
img_hard_brick= 'hard_brick.png'

SIZE_X=760 #max size 760x480
SIZE_Y=480

HANDL_POS = 0.8 * SIZE_Y


pygame.init()
screen = pygame.display.set_mode((SIZE_X,SIZE_Y),0,32)


class brick:
    def __init__(self,crush=False,points=10,line=0,column=0,x_brick=0,y_brick=0 \
                 ,color=pygame.image.load(img_common_brick).convert() \
                 ,fragile=1):
        self.crush=crush
        self.points=points
        self.line=line
        self.column=column
        self.x_brick=x_brick
        self.y_brick=y_brick
        #self.color=pygame.transform.scale(color,(int(SIZE_X*0.07),int(SIZE_Y*0.04)))
        self.color=color
        self.fragile=fragile

    def crushed(self):
        if self.fragile==0:
            self.crush=True

class hard_brick(brick):
    def __init__(self,crush=False,points=20,line=0,column=0,x_brick=0,y_brick=0 \
                 ,color=pygame.image.load(img_hard_brick).convert() \
                 ,fragile=2):
        brick.__init__(self,crush,line,column,x_brick,y_brick)
        self.points=points
        self.color=color
        self.fragile=fragile


class player:
    def __init__(self,lives=3,score=0,list_of_scores=[],name='UNNAMED_NEWBIE'):
        self.lives=lives
        self.score=score
        self.list_of_scores=list_of_scores
        self.name=name

    def __setattr__(self,attr_name, value):
        if attr_name is 'name' and value is '':
            self.name = 'UNNAMED_NEWBIE'
        else:
            object.__setattr__(self,attr_name, value)


current_player=player()

#current_player.name=input('enter player name:\n')


def GUI():
    
    def update_Database():
        current_player.name=yourName.get()
        #print(yourName.get())
        app.destroy()

    app=Tk()                    #window
    app.title("Bricks0.6")
    app.geometry('350x200')

    labelText=StringVar()       #Label
    labelText.set('Enter your name')
    label1 = Label(app,textvariable=labelText,height=4)
    label1.pack()

    Name=StringVar()        #TextBox
    yourName=Entry(app, textvariable=Name)
    yourName.pack()

    #button
    button1 = Button(app,text='Continue',width = 10, command=update_Database)
    button1.pack()

    app.mainloop()



#start_game=False



background=pygame.image.load(img_back).convert()
mouse_c=pygame.image.load(img_pointer).convert()
ball = pygame.image.load(img_ball).convert()


def load_brick():   #setting the bricks
    Array_of_bricks=[]
    f=open('1_level.txt','r')
    line =0
    for coords in f.readlines():
        list_coords= re.findall(r'\d+',coords)
        column=0
        for coord in list_coords:
            if int(coord) is 1:
                brick1=brick()
                brick1.crush=False
                brick1.line=line
                brick1.column=column
                brick1.x_brick=int(0.065*SIZE_X)+brick1.column*brick1.color.get_width()
                brick1.y_brick=int(0.1*SIZE_Y)+brick1.line*brick1.color.get_height()
                Array_of_bricks.append(brick1)
                #screen.blit(brick1.color,(50+column*brick1.color.get_width(),50+line*brick1.color.get_height()))           
            if int(coord) is 0:
                brick1=brick()
                brick1.crush=True
                brick1.line=line
                brick1.column=column
                brick1.x_brick=int(0.065*SIZE_X)+brick1.column*brick1.color.get_width()
                brick1.y_brick=int(0.1*SIZE_Y)+brick1.line*brick1.color.get_height()
                Array_of_bricks.append(brick1)

            if int(coord) is 2:
                brick1=hard_brick()
                brick1.crush=False
                brick1.line=line
                brick1.column=column
                brick1.x_brick=int(0.065*SIZE_X)+brick1.column*brick1.color.get_width()
                brick1.y_brick=int(0.1*SIZE_Y)+brick1.line*brick1.color.get_height()
                Array_of_bricks.append(brick1)
                
            column=column+1
        line=line+1
    return Array_of_bricks

bricks=load_brick()

GUI()
database = shelve.open('player')
    
if current_player.name in [player_name_encoded.decode() for player_name_encoded in database.dict.keys()]:
    print(current_player.name,'started the game')
    current_player.list_of_scores = database[current_player.name]
else:
    print(current_player.name,'started the game')

def move_handler(): #moving the handler
        x= pygame.mouse.get_pos()[0] #y is const
        x = x - mouse_c.get_width()/2
        screen.blit(mouse_c,(x,HANDL_POS))
        return x


#movex, movey = 0,0

def draw_bricks():              #drawing bricks
    for elem in bricks:
        if elem.fragile==1 and type(elem) is hard_brick:
            elem.color=pygame.image.load(img_common_brick).convert()
        if elem.crush is False:
            screen.blit(elem.color,(elem.x_brick ,elem.y_brick))
    

def endgame():               #quiting the game
    try:
        pygame.quit()
        sys.exit()
    except SystemExit:
        database.close()
        print('Bye-bye!')
    
def print_highscore():
    scores=[]
    for score in database[current_player.name]:
        scores.append(score)
    scores.sort(reverse=True)
    print(current_player.name,'high score is',scores[0][0],\
          'achieved at', scores[0][1])
        

def display(movex,movey):
    x_ball,y_ball=SIZE_X/2,SIZE_Y/2

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                endgame()
            
            
        screen.blit(background, (0,0))
        
        x_handler=move_handler()    #moving the handler

        screen.blit(ball,(x_ball,y_ball)) #moving the ball
        y_ball=y_ball+movey
        x_ball=x_ball+movex

        draw_bricks()
                
        pygame.display.update()
        
        if y_ball+ball.get_height()/2 >= HANDL_POS - mouse_c.get_height()/2 \
           and y_ball+ball.get_height()/2 < HANDL_POS - mouse_c.get_height()/2+1.5 \
           and x_ball + ball.get_width() > x_handler \
           and x_ball < x_handler + mouse_c.get_width(): #the condition of bouncing
            #print('The ball hits the handler')
            movey=-movey

        if y_ball < 0:
            #print('The ball hits the top')
            movey=-movey

        if x_ball < 0:
            #print('The ball hits the left wall')
            movex=-movex

        if x_ball+ball.get_width() > SIZE_X:
            #print('The ball hits the right wall')
            movex=-movex                

        if y_ball+ball.get_height()/2 > SIZE_Y:
            
            current_player.lives = current_player.lives - 1
            print('You lost 1 life',current_player.lives,'remain(s)')
            break

        current_bricks=[]
        
        for brick in bricks:
            if not brick.crush:       #condition of collision
                if y_ball < brick.y_brick + brick.color.get_height() and \
                   x_ball + ball.get_width() > brick.x_brick and \
                   x_ball < brick.x_brick + brick.color.get_width() and\
                   y_ball + ball.get_height() > brick.y_brick:
                    #print('4upq tuhla')
                    #brick.crush=True  #tuk popadnah na seriozna pre4ka
                    #to 4upi 2 tuhli i pravi movey=-movey=--movey=movey i zatova prodyljava
                    #kak da go opravq?

                    if (y_ball + ball.get_height()/2 < brick.y_brick or \
                       y_ball + ball.get_height()/2 > brick.y_brick + brick.color.get_height()) \
                       and not (x_ball + ball.get_width()/2 < brick.x_brick or \
                       x_ball + ball.get_width()/2 > brick.x_brick + brick.color.get_width()) :
                        movey=-movey
                        #print('crushes by y')
                        brick.fragile = brick.fragile - 1
                        brick.crushed()
                        current_player.score = current_player.score + brick.points
                        break

                    if (x_ball + ball.get_width()/2 < brick.x_brick or \
                       x_ball + ball.get_width()/2 > brick.x_brick + brick.color.get_width())\
                       and not(y_ball + ball.get_height()/2 < brick.y_brick or \
                       y_ball + ball.get_height()/2 > brick.y_brick + brick.color.get_height()):
                        movex=-movex
                        #print('crushes by x')
                        brick.fragile = brick.fragile - 1
                        brick.crushed()
                        current_player.score = current_player.score + brick.points
                        break
                    
            else:
                current_bricks.append(brick)
                if len(current_bricks)==len(bricks):
                    print('CONGRATULATION U WIN!!')
                    print('your score is',current_player.score)
                    current_player.list_of_scores.append((current_player.score,str(datetime.now())))
                    database[current_player.name]=current_player.list_of_scores
                    print_highscore()
                    endgame()
                    

                    
    

while True:
    
    try:
        for event in pygame.event.get():  #quiting the game
            if event.type == QUIT:
                endgame()
            if event.type == MOUSEBUTTONDOWN:
                #display(0.6,0.6) #max 5
                try:
                    display(0.01*random.randint(-150,150),0.01*random.randint(-150,150))
                except:
                    pass
                
            pygame.draw.line(background,(0,0,0),(0,0),(SIZE_X,0),5)
            pygame.draw.line(background,(0,0,0),(SIZE_X,0),(SIZE_X,SIZE_Y),5)
            pygame.draw.line(background,(0,0,0),(0,SIZE_Y),(0,0),5)

        if current_player.lives==0:
            print('GAME OVER')
            print('your score is',current_player.score)
            current_player.list_of_scores.append((current_player.score,str(datetime.now())))
            database[current_player.name]=current_player.list_of_scores
            print_highscore()
            endgame()
                
        
                           
        #setting the background
        screen.blit(background, (0,0))

    

        #setting the mouse
   
        x,y= pygame.mouse.get_pos()
        x = x - mouse_c.get_width()/2
        y = y - mouse_c.get_height()/2
        
        screen.blit(mouse_c,(x,HANDL_POS))
        
        #setting the ball
        screen.blit(ball,(SIZE_X/2,SIZE_Y/2))
 
        draw_bricks()
       
        pygame.display.update() #updating the screen
    except:
        pygame.quit()
        sys.exit()
    
    




