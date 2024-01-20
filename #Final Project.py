#Final Project
#imports
import pygame
import os
import random
from pygame.locals import *
#initialize pygame
pygame.init()
#Variable Initialization
clock = pygame.time.Clock() 
FPS = 60
width, height = 1280,800
direction = True
#SCREEN AND TITLE
WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Monster Hunter!")


def main(): 
    x = 620
    y = 400
   
    velocity = 5
    mob_velocity = 0.5
    run = True
    
    player_image = pygame.image.load(os.path.join('Pygame', 'player_image.png'))
    width_player = 50  
    height_player = 50

    player_image = pygame.transform.scale(player_image, (width_player, height_player))
    player_copy = player_image.copy()
    
    bg = pygame.image.load(os.path.join('Pygame', 'Backround_layer.jpg'))
    bg = pygame.transform.scale(bg, (width, height))
           
    mob_image = pygame.image.load(os.path.join('Pygame','mob_wave_1.png'))
    mob_image = pygame.transform.scale(mob_image,(70,60))
    
    mob_count = random.randint(6, 12)

    mobs = [] 
    for i in range(0,mob_count+1):
        x_mob = random.randint(0,width - 70)
        y_mob = random.randint(0,height - 60)
        mobs.append((x_mob, y_mob))
    
    
    while run: 


        clock.tick(FPS)
        player_hitbox = pygame.Rect(x, y, width_player, height_player)
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()

        WIN.fill((0, 0, 0))  

        WIN.blit(bg,(0,0))

        WIN.blit(player_image, (x, y))  
        
        for i, mob_pos in enumerate(mobs): 
            mob_x, mob_y = mob_pos
            mob_rect = pygame.Rect(mob_x,mob_y,70,60)

            dir = pygame.math.Vector2(x - mob_x, y - mob_y).normalize()

            mob_x += dir.x * mob_velocity
            mob_y += dir.y * mob_velocity

            mobs[i] = (mob_x, mob_y)
            
            
            WIN.blit(mob_image, mob_pos)


        
        # PLAYER MOVEMENT
        key_pressed_is = pygame.key.get_pressed()
        if key_pressed_is[K_LEFT] and x - velocity >= 0:
            x -= velocity
            player_image = pygame.transform.rotate(player_copy,180)
        if key_pressed_is[K_RIGHT] and x + velocity + width_player <= width:
            x += velocity
            player_image = pygame.transform.rotate(player_copy,360)
        if key_pressed_is[K_UP] and y - velocity >= 0:
            y -= velocity
            player_image = pygame.transform.rotate(player_copy,90)
        if key_pressed_is[K_DOWN] and y + velocity + height_player <= height:
            y += velocity
            player_image = pygame.transform.rotate(player_copy,270)

        player_hitbox.x = x
        player_hitbox.y = y

        pygame.display.flip()  

    
if __name__ == "__main__":
    
    main()
