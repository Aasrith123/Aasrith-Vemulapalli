#Final Project

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

#SCREEN AND TITLE
WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Monster Hunter!")
start_image = pygame.image.load(os.path.join('Pygame', 'start_background.jpg'))
start_image = pygame.transform.scale(start_image,(width,height))

gameover_image = pygame.image.load(os.path.join('Pygame', 'game_background.jpg'))
gameover_image = pygame.transform.scale(gameover_image,(width,height))


def winner(): 
    winner_font = pygame.font.SysFont("vivaldi", 100, True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()

        WIN.fill((255,255,255))

        winner_text = winner_font.render("You Have Won!", True, (0, 0, 0))
        quit_p = winner_font.render("Press 'Q' to quit", True, (0, 0, 0))
        WIN.blit(winner_text, (width // 2 - winner_text.get_width() // 2, 200))
        WIN.blit(quit_p, (width // 2 - quit_p.get_width() // 2, 300))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[K_q]:
            pygame.quit()
            quit()

        clock.tick(FPS)


def start():
    start_font = pygame.font.SysFont("vivaldi", 100,True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.blit(start_image, (0, 0)) 

        start_text = start_font.render("Monster Hunter!", True, (0, 0, 0))
        start = start_font.render("Press 'S' to start or 'Q' to quit", True, (0, 0, 0))

        WIN.blit(start_text, (width // 2 - start_text.get_width() // 2, 200))
        WIN.blit(start, (width // 2 - start.get_width() // 2, 300))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[K_s]:
            return  
        elif keys[K_q]:
            pygame.quit()
            quit()

        clock.tick(FPS)
def gameover():
    game_over_font = pygame.font.SysFont("vivaldi", 100, True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.blit(gameover_image, (0, 0))  

        game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
        retry = game_over_font.render("Press 'R' to retry or 'Q' to quit", True, (0, 0, 0))

        WIN.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, 200))
        WIN.blit(retry, (width // 2 - retry.get_width() // 2, 300))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[K_r]:
            return True  
        elif keys[K_q]:
            
            pygame.quit()
            quit()

        clock.tick(FPS)

def upgrade_screen(): 
    global bullet_damage, player_velocity, player_health

    upgrade_font = pygame.font.SysFont("blackadder", 50, True)

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        WIN.fill((0, 0, 0))
        upgrade_text = upgrade_font.render("Choose an Upgrade:", True, (255, 255, 255))
        bullet_text = upgrade_font.render(f"1. Increase Bullet Damage (Current: {bullet_damage})", True, (255, 255, 255))
        velocity_text = upgrade_font.render(f"2. Increase Player Velocity (Current: {player_velocity})", True, (255, 255, 255))
        health_text = upgrade_font.render(f"3. Increase Player Health (Current: {player_health})", True, (255, 255, 255))

        WIN.blit(upgrade_text, (width // 2 - upgrade_text.get_width() // 2, 100))
        WIN.blit(bullet_text, (width // 2 - bullet_text.get_width() // 2, 250))
        WIN.blit(velocity_text, (width // 2 - velocity_text.get_width() // 2, 350))
        WIN.blit(health_text, (width // 2 - health_text.get_width() // 2, 450))

        pygame.display.flip()
        player_health = 100
        keys = pygame.key.get_pressed()
        if keys[K_1]:
            bullet_damage += 5
            break
        elif keys[K_2]:
            player_velocity += 1
            break
        elif keys[K_3]:
            player_health += 20 
            break

        clock.tick(FPS)
        


def create_boss(width, height, mob_health, boss_velocity, mob_image, type1, player_position, mob_wave):
    hitbox_rect = pygame.Rect(0, 0, 250, 250)
    if mob_wave == 6 or mob_wave == 10:
        boss_velocity = 0
    else: 
        boss_velocity = 0.2
    boss = {
        "position": (width / 2, height / 2),
        "health": mob_health,
        "hitbox": hitbox_rect,
        "image_path": mob_image,
        "mob_velocity": boss_velocity,
        "mob_count": 1,
        "type1": type1,
        "direction": pygame.math.Vector2(0, 0),
    }
    dir_to_player = pygame.math.Vector2(player_position[0] - (width / 2), player_position[1] - (height / 2)).normalize()
    boss["direction"] = dir_to_player * boss_velocity   
    return boss

def wave(wave_count, width_mob, height_mob, new_wave_properties, mobs, player_position):
    global mob_wave, wave_properties

    mob_wave = wave_count
    wave_properties = {}
    boss = None
    if mob_wave == 3 or mob_wave == 6 or mob_wave == 10:
        mobs.clear()
        mob_health = 2500 
        boss_velocity = new_wave_properties['mob_velocity']
        type1= "boss"
        mob_image_path = os.path.join('Pygame', f'mob_wave_{mob_wave}.png')
        mob_image = pygame.transform.scale(pygame.image.load(mob_image_path), (200, 200))
        boss_velocity = new_wave_properties['mob_velocity']


        boss = create_boss(width, height, mob_health, boss_velocity, mob_image, type1, player_position, mob_wave)
        mobs.append(boss)
    else:
        mob_image_path = os.path.join('Pygame', f'mob_wave_{mob_wave}.png')
        mob_image = pygame.transform.scale(pygame.image.load(mob_image_path), (width_mob, height_mob))

        wave_properties = {
            'mob_count' : random.randint(6, 12),
            'mob_health' : 100 + (wave_count -1) * new_wave_properties['mob_health_increase'], 
            'mob_velocity' : new_wave_properties['mob_velocity'],
            'mob_image': mob_image,
        }
        mobs.clear() 
        mob_health = wave_properties['mob_health']
        hitbox_rect = pygame.Rect(0,0, width_mob, height_mob)

        for z in range(wave_properties['mob_count']):
            mob_x  = random.randint(0, width - width_mob)
            mob_y  = random.randint(0, height - height_mob)
            mobs.append({"position": (mob_x, mob_y), "health": mob_health, 
                        "image_path":mob_image, "hitbox":hitbox_rect, "type":"normal"})


def main(): 
    global mob_wave, wave_properties
    start()
    mob_wave = 1
    wave_properties = {}
    asteroids = []

    #BULLET VARIABLES 
    bullets = []
    bullet_image = pygame.image.load(os.path.join('Pygame' , 'bullet.png'))
    bullet_image = pygame.transform.scale(bullet_image,(20,10))
    explosion_image = pygame.image.load(os.path.join('Pygame', 'explosion.png'))
    explosion_image = pygame.transform.scale(explosion_image, (70,70))
    global space_pressed
    space_pressed = False

    #asteroid 
    asteroid_image = pygame.image.load(os.path.join('Pygame', 'asteroid.png'))
    asteroid_image = pygame.transform.scale(asteroid_image, (40, 40))
    spawn_cooldown = 0
    temp_a = 20


    global player_health
    damage_cooldown = 0

    x = 620
    y = 400
   
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
    
    mob_image_z = os.path.join('Pygame', f'mob_wave_{mob_wave}.png')
    mob_image = pygame.transform.scale(pygame.image.load(mob_image_z), (width_mob, height_mob))

    first_wave_properties = {
        'mob_count': random.randint(6, 12),
        'mob_health': 100,
        'mob_velocity': 0.5,
        'mob_image': 'f"Pygame", f"mob_wave_{mob_wave}.png"',
    }
    new_wave_properties = {
       'mob_health_increase':50,
       'mob_velocity':1, 

}
    wave_properties = first_wave_properties.copy()
    hitbox_rect = pygame.Rect(0,0, width_mob, height_mob)

    for z in range(wave_properties['mob_count']):
        mob_x = random.randint(0, width - width_mob)
        mob_y = random.randint(0, height - height_mob)
        mobs.append(
            {"position": (mob_x, mob_y), "health": wave_properties['mob_count'], "image_path": mob_image,
             "hitbox": hitbox_rect})
    player_dir = pygame.math.Vector2(1,0)

    while run: 
        #EXIT CODE
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()
        player_position = (x, y)
        global player_health
        #Refresh rate
        clock.tick(FPS)
        #Player hitboxing
        player_hitbox = pygame.Rect(x, y, width_player, height_player)
        wave_text = font_wave.render(f"Wave: {mob_wave}", True, (255, 255, 255))

        player_health_words = font_player_health.render("Player Health", True,(255,255,255))
        if mob_wave == 3 or mob_wave == 6 or mob_wave == 10:
            
            if mob_wave == 6 or mob_wave == 10: 
                mob_velocity = 2 
            else: 
                mob_velocity = 0.2
            wave_properties = {
                'mob_count': 1,
                'mob_health': 250,
                'mob_velocity': mob_velocity,
                'mob_image': mob_image,  
                'type1': "boss",
            }
        else:
            wave_properties = {
                'mob_count': random.randint(6, 12),
                'mob_health': 100 + (mob_wave - 1) * new_wave_properties['mob_health_increase'],
                'mob_velocity': new_wave_properties['mob_velocity'],
                'mob_image': mob_image,
            }

       


                
        
        #Bliting and things like that to make the background and player image show
        WIN.fill((0, 0, 0))  
        WIN.blit(bg,(0,0))
        WIN.blit(player_image, (x, y))
        WIN.blit(player_health_words,(20,40))
        WIN.blit(wave_text, (20, 85))
        for asteroid_info in asteroids: 
            WIN.blit(asteroid_image, asteroid_info["position"])



            #Mob Spawning
        for i, mob_info in enumerate(mobs): 
            if "position" in mob_info:
                mob_x, mob_y = mob_info["position"]
                mob_rect = pygame.Rect(mob_x, mob_y, width_mob, height_mob)
                mob_rect.x, mob_rect.y = mob_x,mob_y


                dir = pygame.math.Vector2(x - mob_x, y - mob_y).normalize()
                angle = dir.angle_to(pygame.math.Vector2(1,0))
                rotated_mob_image = pygame.transform.rotate(mob_info["image_path"], angle)
                rotated_mob_rect = rotated_mob_image.get_rect(center=(mob_x, mob_y))



                mob_x += dir.x * wave_properties['mob_velocity']
                mob_y += dir.y * wave_properties['mob_velocity']


                mobs[i]["position"] = (mob_x, mob_y)
            
                mob_rect.x, mob_rect.y = mob_x, mob_y
                WIN.blit(rotated_mob_image, rotated_mob_rect.topleft)

                if player_hitbox.colliderect(mob_rect) and damage_cooldown==0: 
                    player_health-= 10
                    damage_cooldown =60 
                #If mob health reaches or is under 0 pop em 
                if mobs[i]["health"] <= 0: 
                    mobs.pop(i)
                if not mobs and mob_wave < 10: 
                    wave(mob_wave + 1, 70, 60, new_wave_properties, mobs, player_position)
                    if mob_wave == 3 or mob_wave == 6 or mob_wave == 10:
                        upgrade_screen()
                if not mobs and mob_wave == 10: 
                    winner()
                if spawn_cooldown == 0:
                    if mob_info.get("type1") == "boss" and (mob_wave == 3 or mob_wave == 10):
                        if random.randint(1, 100) <= 5:
                            dir_to_player = pygame.math.Vector2(player_position[0] - mob_info["position"][0],
                                                                player_position[1] - mob_info["position"][1]).normalize()
                            asteroid_velocity = 3
                            asteroid_initial_direction = dir_to_player
                            asteroids.append({
                            "position": mob_info["position"],
                            "initial_direction": asteroid_initial_direction,
                            "velocity": asteroid_velocity})
                    if (mob_wave == 6 or mob_wave == 10 )and mob_info.get("type1") == "boss":
                               mobs[i]["mob_velocity"] = 30

                    spawn_cooldown = temp_a 
                else: 
                    spawn_cooldown -= 10
                for i, asteroid_info in enumerate(asteroids):
 
                        asteroid_x, asteroid_y = asteroid_info["position"]
                        asteroid_rect = pygame.Rect(asteroid_x, asteroid_y, 40, 40)
                        asteroid_rect.x, asteroid_rect.y = asteroid_x, asteroid_y

                        asteroid_x += asteroid_info["initial_direction"].x * 2
                        asteroid_y += asteroid_info["initial_direction"].y * 2


                        asteroids[i]["position"] = (asteroid_x, asteroid_y)

                        if player_hitbox.colliderect(asteroid_rect) and damage_cooldown == 0:
                            player_health -= 20
                            damage_cooldown = 60

                        if asteroid_x < 0 or asteroid_x > width or asteroid_y < 0 or asteroid_y > height:
                            asteroids.pop(i)

            
        #DAMAGE COOLDOWN 60 - 1 till its 0 to achieve a cooldown of 1 
        if damage_cooldown>0:
            damage_cooldown -=1
        #This creates a player health bar 
        pygame.draw.rect(WIN,(255,255,255), (18,18,204,24),2) # WHITE OUTLINE 
        pygame.draw.rect(WIN,(255,0,0),(20,20,200,20)) # RED BG OF HEALTH BAR 
        pygame.draw.rect(WIN, (0,255,0), (20,20, player_health * 2, 20)) # GREEN HEALTH BAR 
        # PLAYER MOVEMENT
        key_pressed_is = pygame.key.get_pressed()
        if key_pressed_is[K_LEFT] and x - player_velocity >= 0:
            x -= player_velocity
            player_image = pygame.transform.rotate(player_copy,180)
            player_dir = pygame.math.Vector2(-1,0)
        if key_pressed_is[K_RIGHT] and x + player_velocity + width_player <= width:
            x += player_velocity
            player_image = pygame.transform.rotate(player_copy,360)
            player_dir = pygame.math.Vector2(1,0)
        if key_pressed_is[K_UP] and y - player_velocity >= 0:
            y -= player_velocity
            player_image = pygame.transform.rotate(player_copy,90)
            player_dir = pygame.math.Vector2(0,-1)
        if key_pressed_is[K_DOWN] and y + player_velocity + height_player <= height:
            y += player_velocity
            player_image = pygame.transform.rotate(player_copy,270)
            player_dir = pygame.math.Vector2(0,1)
        player_hitbox.x = x
        player_hitbox.y = y

        # Bullet:
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
                        mobs[j]["health"] -= bullet_damage

                        WIN.blit(explosion_image, (mob_x - 10, mob_y - 10))
            

        if player_health <= 0:
            if gameover():
                mob_wave = 1   
                wave_properties = {}
                asteroids = []
                player_health = 100
                bullets = []
                start()
           
        pygame.display.flip()

    pygame.quit()

    
if __name__ == "__main__":
    start_time = pygame.time.get_ticks()
    font = pygame.font.SysFont("pristina",100,True)
    font_player_health = pygame.font.SysFont("comicsans", 30, True)
    font_wave = pygame.font.SysFont("gigi", 25, True)
    mobs = []
    bullet_damage = 10
    player_velocity = 3
    player_health = 100
    main()
