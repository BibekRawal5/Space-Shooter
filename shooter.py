import pygame

pygame.font.init()

WINNER_FONT = pygame.font.SysFont('comicsans', 100)
HEALTH_FONT = pygame.font.SysFont('comicsans', 25)
MENU_FONT = pygame.font.SysFont('comicsans', 40)

FPS = 120
WIDTH, HEIGHT = 1000, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

S_WIDTH, S_HEIGHT = 70, 70
S_VEL = 7

BULLET_WIDTH, BULLET_HEIGHT = 25, 8
B_VEL = 15

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
MENU_CLOSE = pygame.USEREVENT + 3

RED_SPACESHIP_IMAGE = pygame.image.load('images/spaceship_red.png')
YELLOW_SPACESHIP_IMAGE = pygame.image.load('images/spaceship_yellow.png')
BACKGROUND1 = pygame.transform.scale(pygame.image.load('images/space1.png'), (WIDTH, HEIGHT))
BACKGROUND2 = pygame.transform.scale(pygame.image.load('images/space2.jpg'), (WIDTH, HEIGHT))
BACKGROUND3 = pygame.transform.scale(pygame.image.load('images/space3.jpg'), (WIDTH, HEIGHT))
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load('images/menu_background.jpg'), (WIDTH, HEIGHT))
BACKGROUND = BACKGROUND1.copy()
RED_SPACESHIP = pygame.transform.rotate(
    (pygame.transform.scale(RED_SPACESHIP_IMAGE, (S_WIDTH, S_HEIGHT))), 90)
YELLOW_SPACESHIP = pygame.transform.rotate(
    (pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (S_WIDTH, S_HEIGHT))), 270)

BG1 = pygame.Rect(0, HEIGHT/2, 250, 250)
BG2 = pygame.Rect(WIDTH/3, HEIGHT/2, 250, 250)
BG3 = pygame.Rect(WIDTH/1.42, HEIGHT/2, 250, 250)
BACKGROUND1_SCALED = pygame.transform.scale(BACKGROUND1, (250, 250))
BACKGROUND2_SCALED = pygame.transform.scale(BACKGROUND2, (250, 250))
BACKGROUND3_SCALED = pygame.transform.scale(BACKGROUND3, (250, 250))

BORDER = pygame.Rect(WIDTH/2, 0, 5, HEIGHT)

     
def menu_select_bacckground():
    
    clock = pygame.time.Clock()
    while(1):
        # WIN.blit(MENU_BACKGROUND, (0,0))
        WIN.fill((0,0,0))
        text = MENU_FONT.render("SELECT THE BACKGROUND", 1, WHITE)
        WIN.blit(text, (WIDTH/5, HEIGHT/2 - HEIGHT/3))

        WIN.blit(BACKGROUND1_SCALED, BG1)
        WIN.blit(BACKGROUND2_SCALED, BG2)
        WIN.blit(BACKGROUND3_SCALED, BG3)
        pygame.display.update()
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(MENU_CLOSE))
                return

        mouse_press = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
     
        if mouse_press[0] and BG1.collidepoint(pos):
            BACKGROUND.blit(BACKGROUND1, (0,0))
            break
        
        elif mouse_press[0] and BG2.collidepoint(pos):
            BACKGROUND.blit(BACKGROUND2, (0,0))
            break
        
        elif mouse_press[0] and BG3.collidepoint(pos):
            BACKGROUND.blit(BACKGROUND3, (0,0))
            break

def red_spaceship_move(red_spaceship, keys_pressed):
    if keys_pressed[pygame.K_s] and red_spaceship.y + S_VEL + RED_SPACESHIP.get_height() < HEIGHT:
            red_spaceship.y += S_VEL
    if keys_pressed[pygame.K_w] and red_spaceship.y - S_VEL > 0:
            red_spaceship.y -=  S_VEL
    if keys_pressed[pygame.K_d] and red_spaceship.x + S_VEL + RED_SPACESHIP.get_width() < WIDTH/2:
            red_spaceship.x += S_VEL 
    if keys_pressed[pygame.K_a] and red_spaceship.x - S_VEL > 0:
            red_spaceship.x -= S_VEL
        
def yellow_spaceship_move(yellow_spaceship, keys_pressed):
    if keys_pressed[pygame.K_DOWN] and yellow_spaceship.y + S_VEL + YELLOW_SPACESHIP.get_height() < HEIGHT :
            yellow_spaceship.y += S_VEL
    if keys_pressed[pygame.K_UP] and yellow_spaceship.y - S_VEL > 0:
            yellow_spaceship.y -= S_VEL
    if keys_pressed[pygame.K_RIGHT] and yellow_spaceship.x + S_VEL + YELLOW_SPACESHIP.get_width() < WIDTH:
            yellow_spaceship.x += S_VEL
    if keys_pressed[pygame.K_LEFT] and yellow_spaceship.x - S_VEL - 5 > WIDTH/2 :
            yellow_spaceship.x -= S_VEL

def handle_bullets(red_bullets, yellow_bullets, red_spaceship, yellow_spaceship):
    for bullet in red_bullets:
          bullet.x += B_VEL
          if yellow_spaceship.colliderect(bullet):
              pygame.event.post(pygame.event.Event(YELLOW_HIT))
              red_bullets.remove(bullet)
    
    for bullet in yellow_bullets:
          bullet.x -= B_VEL
          if red_spaceship.colliderect(bullet):
              pygame.event.post(pygame.event.Event(RED_HIT))
              yellow_bullets.remove(bullet)            

def draw(red_spaceship, yellow_spaceship, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    
    text = HEALTH_FONT.render(("LIVES :" + str(red_health)), 1, WHITE)
    WIN.blit(text, (10, 30))
    
    text = HEALTH_FONT.render(("LIVES :" + str(yellow_health)), 1, WHITE)
    WIN.blit(text, (WIDTH - 120, 30))
    
    WIN.blit(RED_SPACESHIP, (red_spaceship.x, red_spaceship.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow_spaceship.x, yellow_spaceship.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()
    
def game_finished(winner_text):
    if "RED" in winner_text:
        text = WINNER_FONT.render(winner_text, 1, RED)
    else:
         text = WINNER_FONT.render(winner_text, 1, YELLOW)
    WIN.blit(text, (WIDTH/2 - text.get_width() / 2, HEIGHT/2 - text.get_height()/2 ))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    
    clock = pygame.time.Clock()
    run = True
    red_spaceship = pygame.Rect(10, HEIGHT/2, S_WIDTH, S_HEIGHT)
    yellow_spaceship = pygame.Rect(WIDTH - 75, HEIGHT/2, S_WIDTH, S_HEIGHT)
    red_health = 3
    yellow_health = 3
    red_bullets = []
    yellow_bullets = []
    
    menu_select_bacckground()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == MENU_CLOSE:
                run = False
                pygame.QUIT
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(red_spaceship.x + red_spaceship.width, red_spaceship.y + red_spaceship.height/2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(yellow_spaceship.x , yellow_spaceship.y + yellow_spaceship.height/2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        keys_pressed = pygame.key.get_pressed()
        red_spaceship_move(red_spaceship, keys_pressed)
        yellow_spaceship_move(yellow_spaceship, keys_pressed)
        handle_bullets(red_bullets, yellow_bullets, red_spaceship, yellow_spaceship)
         
        draw(red_spaceship, yellow_spaceship, red_bullets, yellow_bullets, red_health, yellow_health)
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS"
        
        if yellow_health <= 0:
            winner_text = "RED WINS"
                                       
        if winner_text != "":
            game_finished(winner_text)
            break
        
    if run:       
        main()
    
    
if __name__ == "__main__":
    main()
    