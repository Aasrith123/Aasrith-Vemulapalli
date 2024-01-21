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
player_health = 100

#SCREEN AND TITLE
WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Monster Hunter!")


def main(): 
    #BULLET VARIABLES 
    bullets = []
    bullet_image = pygame.image.load(os.path.join('Pygame', 'bullet.png'))
    bullet_image = pygame.transform.scale(bullet_image,(10,10))
    explosion_image = pygame.image.load(os.path.join('Pygame', 'explosion.png'))
    explosion_image = pygame.transform.scale(explosion_image, (70,70))
    global space_pressed
    space_pressed = False


    global player_health
    damage_cooldown = 0

    x = 620
    y = 400
   
    velocity = 5
    run = True
    
    width_mob = 70
    height_mob = 60

    width_player = 50  
    height_player = 50

    mobs = [] 

    player_image = pygame.image.load(os.path.join('Pygame', 'player_image.png'))
    player_image = pygame.transform.scale(player_image, (width_player, height_player))
    player_copy = player_image.copy()
    
    bg = pygame.image.load(os.path.join('Pygame', 'Backround_layer.jpg'))
    bg = pygame.transform.scale(bg, (width, height))
           
    mob_image_path = os.path.join('Pygame', f'mob_wave_{mob_wave}.png')
    mob_image = pygame.transform.scale(pygame.image.load(mob_image_path), (width_mob, height_mob))
    old_wave_properties = {
    'mob_count' : random.randint(6, 12),
    'mob_health' : 100, 
    'mob_velocity' : 0.5,
    'mob_image': 'f"Pygame", "mob_wave_{mob_wave}.png"',
}
    new_wave_properties = {
       'mob_health_increase':50,
       'mob_velocity':1, 

}
    
    wave_properties = old_wave_properties.copy()
    
    def start_new_wave( ): 
        global mobs, mob_wave
        mob_wave +=1
        mob_count = random.randint(6,12)
        mobs = []

        wave_properties['mob_image'] = os.path.join('Pygame', f'mob_wave_{mob_wave}.png')
        wave_properties['mob_health'] += new_wave_properties['mob_health_increase']
        wave_properties['mob_velocity'] = new_wave_properties['mob_velocity']

        for z in range(mob_count): 
            mob_x = random.randint(0, width - width_mob)
            mob_y = random.randint(0, height - height_mob)
            mobs.append({"position": (mob_x, mob_y), "health": wave_properties['mob_health'], "image_path": wave_properties['mob_image']})


    for z in range(wave_properties['mob_count']):
        mob_x  = random.randint(0, width - width_mob)
        mob_y  = random.randint(0, height - height_mob)
        mobs.append({"position": (mob_x, mob_y), "health": wave_properties['mob_count'], "image_path":mob_image})

    player_dir = pygame.math.Vector2(1,0)

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
        wave_text = font_wave.render(f"Wave: {mob_wave}", True, (255, 255, 255))

        player_health_words = font_player_health.render("Player Health", True,(255,255,255))
        #Bliting and things like that to make the background and player image show
        WIN.fill((0, 0, 0))  
        WIN.blit(bg,(0,0))
        WIN.blit(player_image, (x, y))
        WIN.blit(player_health_words,(20,40))

        WIN.blit(wave_text, (20, 85))
            #Mob Spawning
        for i, mob_info in enumerate(mobs): 
            if "position" in mob_info:
                mob_x, mob_y = mob_info["position"]
                mob_rect = pygame.Rect(mob_x, mob_y, 70, 60)

                dir = pygame.math.Vector2(x - mob_x, y - mob_y).normalize()
                angle = dir.angle_to(pygame.math.Vector2(1,0))
                rotated_mob_image = pygame.transform.rotate(mob_info["image_path"], angle)
                rotated_mob_rect = rotated_mob_image.get_rect(center=(mob_x, mob_y))



                mob_x += dir.x * wave_properties['mob_velocity']
                mob_y += dir.y * wave_properties['mob_velocity']

                mobs[i]["position"] = (mob_x, mob_y)
            
            
                WIN.blit(rotated_mob_image, rotated_mob_rect.topleft)

                    #If playerhitbox colides with the mobs hitbox damage is taken
                if player_hitbox.colliderect(mob_rect) and damage_cooldown==0: 
                    player_health-= 10
                    damage_cooldown =60 # 60 change after you test the game over screen
                #If mob health reaches or is under 0 pop em 
                if mobs[i]["health"] <= 0: 
                    mobs.pop(i)

            if not mobs: 
                start_new_wave()
 
        #DAMAGE COOLDOWN 60 - 1 till its 0 to achieve a cooldown of 1 
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
            player_dir = pygame.math.Vector2(-1,0)
        if key_pressed_is[K_RIGHT] and x + velocity + width_player <= width:
            x += velocity
            player_image = pygame.transform.rotate(player_copy,360)
            player_dir = pygame.math.Vector2(1,0)
        if key_pressed_is[K_UP] and y - velocity >= 0:
            y -= velocity
            player_image = pygame.transform.rotate(player_copy,90)
            player_dir = pygame.math.Vector2(0,-1)
        if key_pressed_is[K_DOWN] and y + velocity + height_player <= height:
            y += velocity
            player_image = pygame.transform.rotate(player_copy,270)
            player_dir = pygame.math.Vector2(0,1)
        player_hitbox.x = x
        player_hitbox.y = y

        # MOVE ALL THE BULLET SHIT HERE, YOUVE SPENT LIKE 3 HOURS GETTING THE BASE SO NOW FINISH IT UP AND GET MATH DONE
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and not space_pressed:
            bullet_dir = player_dir.copy()
            bullets.append([(x + width_player // 2, y + height_player // 2), bullet_dir])
            space_pressed = True
        if not keys[K_SPACE]:
            space_pressed = False

        for i in range(len(bullets)):
            bullet_pos, bullet_dir = bullets[i]
            WIN.blit(bullet_image, bullet_pos)
            bullets[i] = [(bullet_pos[0] + 10 * bullet_dir.x, bullet_pos[1] + 10 * bullet_dir.y), bullet_dir]

            # Bullet-mob collision
            for j, mob_info in enumerate(mobs):
                if "position" in mob_info:
                    mob_x, mob_y = mob_info["position"]
                    mob_rect = pygame.Rect(mob_x, mob_y, 70, 60)

                    if pygame.Rect(bullet_pos[0], bullet_pos[1], 10, 10).colliderect(mob_rect):
                        mobs[j]["health"] -= 10

                        WIN.blit(explosion_image, (mob_x - 10, mob_y - 10))


        pygame.display.flip()

        if player_health <= 0:
            game_over = font.render("Game Over!", True, (200, 0, 0))
            WIN.blit(game_over, (450, 250))
            pygame.display.flip()
            pygame.time.delay(5000)
            if pygame.time.get_ticks() - start_time > 5000:
                run = False

        WIN.blit(bg, (0, 0))

    pygame.quit()

    
if __name__ == "__main__":
    mob_wave = 1 
    start_time = pygame.time.get_ticks()
    font = pygame.font.SysFont("pristina",100,True)
    font_player_health = pygame.font.SysFont("comicsans", 30, True)
    font_wave = pygame.font.SysFont("gigi", 25, True)
    main()

    
