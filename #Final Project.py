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
player_health = 100

#SCREEN AND TITLE
WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Monster Hunter!")


def main(): 
    
    
    
    global player_health
    damage_cooldown = 0

    x = 620
    y = 400
   
    velocity = 5
    mob_velocity = 0.5
    run = True
    
    width_mob = 70
    height_mob = 60

    width_player = 50  
    height_player = 50

    player_image = pygame.image.load(os.path.join('Pygame', 'player_image.png'))
    player_image = pygame.transform.scale(player_image, (width_player, height_player))
    player_copy = player_image.copy()
    
    bg = pygame.image.load(os.path.join('Pygame', 'Backround_layer.jpg'))
    bg = pygame.transform.scale(bg, (width, height))
           
    mob_image = pygame.image.load(os.path.join('Pygame','mob_wave_1.png'))
    mob_image = pygame.transform.scale(mob_image,(70,60))
    
    mob_count = random.randint(6, 12)
    mob_health = 100 
    mobs = [] 
    
    
    for i in range(0,mob_count+1):
        x_mob = random.randint(0,width - width_mob)
        y_mob = random.randint(0,height - height_mob)
        mobs.append((x_mob, y_mob))
    
    
    while run: 
        #EXIT CODE
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()

        global player_health
        #Refresh rate
        clock.tick(FPS)
        #Player hitboxing
        player_hitbox = pygame.Rect(x, y, width_player, height_player)
        
        player_health_words = font_player_health.render("Player Health", True,(255,255,255))
        #Bliting and things like that to make the background and player image show
        WIN.fill((0, 0, 0))  
        WIN.blit(bg,(0,0))
        WIN.blit(player_image, (x, y))
        WIN.blit(player_health_words,(20,40))
        #Mob Spawning
        for i, mob_pos in enumerate(mobs): 
            mob_x, mob_y = mob_pos
            mob_rect = pygame.Rect(mob_x,mob_y,70,60)

            dir = pygame.math.Vector2(x - mob_x, y - mob_y).normalize()
            angle = dir.angle_to(pygame.math.Vector2(1,0))

            rotated_mob_image = pygame.transform.rotate(mob_image,angle)
            rotated_mob_rect = rotated_mob_image.get_rect(center=(mob_x,mob_y))


            mob_x += dir.x * mob_velocity
            mob_y += dir.y * mob_velocity

            mobs[i] = (mob_x, mob_y)
            
            
            WIN.blit(rotated_mob_image, rotated_mob_rect.topleft)
        for i in 
        #If playerhitbox colides with the mobs hitbox damage is taken
            if player_hitbox.colliderect(mob_rect) and damage_cooldown==0: 
                player_health-= 10
                damage_cooldown =60 # 60 change after you test the game over screen
        #DAMAGE COOLDOWN 60 - 1 till its 0 to achieve a cooldown of 0 
        if damage_cooldown>0:
            damage_cooldown -=1
        #This creates a player health bar 
        pygame.draw.rect(WIN,(255,255,255), (18,18,204,24),2) # WHITE OUTLINE 
        pygame.draw.rect(WIN,(255,0,0),(20,20,200,20)) # RED BG OF HEALTH BAR 
        pygame.draw.rect(WIN, (0,255,0), (20,20, player_health * 2, 20)) # GREEN HEALTH BAR 
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

        if player_health <=0:
            game_over = font.render("Game Over!", True,(200,0,0))
            WIN.blit(game_over,(450, 250))
            pygame.display.flip()
            pygame.time.delay(5000)
            if pygame.time.get_ticks() - start_time > 5000:  # 5000 change after testing game over screen
                run = False
           
            

    
if __name__ == "__main__":
    start_time = pygame.time.get_ticks()
    font = pygame.font.SysFont("pristina",100,True)
    font_player_health = pygame.font.SysFont("comicsans", 30, True)
    main()
    
