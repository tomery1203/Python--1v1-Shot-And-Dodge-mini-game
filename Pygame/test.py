from string import whitespace
import os
#from pyvidplayer import Video

import pygame as pyg
pyg.font.init()
pyg.mixer.init()
#from pygame import display,movie


WIDTH , HIGHT = 780,420
WIN = pyg.display.set_mode((WIDTH , HIGHT))
### setting up window with a size i choose before
pyg.display.set_caption("First Game!") ##s set the windwos name
WHITE = (255,255,255)
GREEN = (0,204,102)
BLACK = (0,0,0)
CARCH_WHIDTH , CARCH_HIGHT = 100,70
BULLET_WHIDTH , BULLET_HIGHT = 40,40
BORDER = pyg.Rect(WIDTH//2-5,0,10,HIGHT)
HEALTH_FONT = pyg.font.SysFont('comicsans',20)
WINNER_FONT=pyg.font.SysFont('comicsans',70)
VEL = 5
MAX_BULELETS = 3
BULLETS_VEL = 8
FPS = 60
TOMER_IMAGE = pyg.image.load(os.path.join('Assets','tomer.png'))
IDAN_IMAGE = pyg.image.load(os.path.join('Assets','idan.png'))        ## loads png images for carchters
BULLET_IMAGE = pyg.image.load(os.path.join('Assets','bullet.png'))
TOMER_IMAGE = pyg.transform.scale(TOMER_IMAGE,(CARCH_WHIDTH,CARCH_HIGHT))
IDAN_IMAGE = pyg.transform.scale(IDAN_IMAGE,(CARCH_WHIDTH,CARCH_HIGHT))                  ## resize the images.
BACKGROUND_IMAGE = pyg.image.load(os.path.join('Assets','background.png'))
BACKGROUND_IMAGE = pyg.transform.scale(BACKGROUND_IMAGE,(WIDTH , HIGHT)) 
BULLET_IMAGE = pyg.transform.scale(BULLET_IMAGE,(BULLET_WHIDTH , BULLET_HIGHT)) 
TOMER_HIT = pyg.USEREVENT +1
IDAN_HIT  =  pyg.USEREVENT +2    #create a new unieq event id
BULLET_SOUND_HIT = pyg.mixer.Sound(os.path.join('Assets','hit.mp3'))
BULLET_SOUND_FIRE = pyg.mixer.Sound(os.path.join('Assets','fire.mp3'))
SEROUND_SOUND = pyg.mixer.Sound(os.path.join('Assets','back.mp3'))
SEROUND_SOUND.set_volume(0.1)
#VID = Video ('intro.mp4')
#VID.set_size((WIDTH , HIGHT)) 






def drew_window (tomer,idan,idan_bullets,tomer_bullets,tomer_health,idan_health): 

    WIN.blit(BACKGROUND_IMAGE,(0,0))   
    pyg.draw.rect(WIN,BLACK,BORDER) 
    WIN.blit(TOMER_IMAGE,(tomer.x,tomer.y)) 
    WIN.blit(IDAN_IMAGE,(idan.x,idan.y))      ## blit func uses to drew surface on the screen like texts or images.
    tomer_health_text = HEALTH_FONT.render("stoned :"+ str (tomer_health) + "%",1,WHITE)
    idan_health_text = HEALTH_FONT.render("stoned :"+ str (idan_health) + "%",1,WHITE)
    WIN.blit(tomer_health_text,(10,10))
    WIN.blit(idan_health_text,(WIDTH-tomer_health_text.get_width()-10,10))
    for bullet in tomer_bullets : 
        WIN.blit(BULLET_IMAGE,(bullet.x,bullet.y))
    for bullet in idan_bullets : 
        WIN.blit(BULLET_IMAGE,(bullet.x,bullet.y))

    pyg.display.update() ## update the display
    
def tomer_handle_movement (keys_pressed,tomer) :
    if keys_pressed [pyg.K_a] and tomer.x - VEL+25 >0 :  #tomer left
            tomer.x -= VEL    
    if keys_pressed [pyg.K_d] and tomer.x + VEL + tomer.width < BORDER.x+25 :  #tomer right
            tomer.x += VEL          
    if keys_pressed [pyg.K_w] and tomer.y - VEL >0:  #tomer up
            tomer.y -= VEL  
    if keys_pressed [pyg.K_s] and tomer.y + VEL + tomer.height < HIGHT - 5 :  #tomer down
            tomer.y += VEL      

def idan_handle_movement (keys_pressed,idan) :
    if keys_pressed [pyg.K_LEFT]and idan.x - VEL+25 >BORDER.x + BORDER.width:  #idan left
            idan.x -= VEL   
    if keys_pressed [pyg.K_RIGHT] and idan.x + VEL + idan.width < WIDTH+20 :  #idan right
            idan.x += VEL              
    if keys_pressed [pyg.K_UP]and idan.y - VEL >0:       #idan up
            idan.y -= VEL  
    if keys_pressed [pyg.K_DOWN]and idan.y + VEL + idan.height < HIGHT - 5:  #idan down
            idan.y += VEL        

def handle_bullets(tomer_bullets,idan_bullets,tomer,idan):

    for bullet in tomer_bullets :
        bullet.x += BULLETS_VEL
        if idan.colliderect(bullet):
            pyg.event.post(pyg.event.Event(IDAN_HIT))
            tomer_bullets.remove(bullet)
        elif bullet.x> WIDTH :
            tomer_bullets.remove(bullet) 

    for bullet in idan_bullets :
        bullet.x -= BULLETS_VEL
        if tomer.colliderect(bullet):
            pyg.event.post(pyg.event.Event(TOMER_HIT))
            idan_bullets.remove(bullet)        
        elif bullet.x < 0 :
            idan_bullets.remove(bullet) 

def draw_winner (text):

    draw_text =  WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2-draw_text.get_width()//2,HIGHT//2-draw_text.get_height()//2))
    pyg.display.update()
    pyg.time.delay(5000)

#def intro():
    
#        VID.draw(WIN,(0,0))
 #       pyg.display.update()
  #      for event in pyg.event.get():
   #         if event.type==pyg.MOUSEBUTTONDOWN:
    #            VID.close()
     #           main()


def main () : 
    run = True
    SEROUND_SOUND.play()
    tomer = pyg.Rect(100,150,CARCH_WHIDTH , CARCH_HIGHT)
    idan = pyg.Rect(700,150,CARCH_WHIDTH , CARCH_HIGHT)   
    clock = pyg.time.Clock()   #make sure the we run the loop 60 times per second MAX
    tomer_bullets = []
    idan_bullets =  []
    tomer_health = 0
    idan_health = 0

    while run :
        clock.tick(FPS)
        
        for event in  pyg.event.get():  ##checks a list of event that acered and react to them.

            if event.type == pyg.QUIT :
                run = False #basicly quits the game.
               
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_LCTRL and len (tomer_bullets)< MAX_BULELETS :
                    bullet = pyg.Rect(tomer.x+tomer.width,tomer.y+tomer.height//2,10,5)
                    tomer_bullets.append(bullet)
                    BULLET_SOUND_FIRE.play()

                if event.key == pyg.K_RCTRL and len (idan_bullets)< MAX_BULELETS  :   
                    bullet = pyg.Rect(idan.x,idan.y+tomer.height//2,10,5)
                    idan_bullets.append(bullet) 
                    BULLET_SOUND_FIRE.play()
        
            if event.type == TOMER_HIT:
                tomer_health += 10
                BULLET_SOUND_HIT.play()

            if event.type == IDAN_HIT:  
                idan_health += 10  
                BULLET_SOUND_HIT.play()
        winner_text = ""
        if tomer_health >= 100 :
            winner_text = "Tomer got WASTED!"    
        if idan_health >= 100 :
            winner_text = "Zavzi got WASTED!"   
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pyg.key.get_pressed()
        tomer_handle_movement(keys_pressed,tomer)
        idan_handle_movement(keys_pressed,idan)    
        handle_bullets (tomer_bullets,idan_bullets,tomer,idan)
        drew_window(tomer,idan,idan_bullets,tomer_bullets,tomer_health,idan_health)

    pyg.quit()


if __name__ == "__main__":
    main ()  #makes sure the game will open only when we want it to run