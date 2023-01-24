import pygame

pygame.font.init()

WINNER_FONT = pygame.font.SysFont('comicsans', 100)
HEALTH_FONT = pygame.font.SysFont('comicsans', 25)

FPS = 60
WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

S_WIDTH, S_HEIGHT = 50, 50
S_VEL = 7

B_VEL = 14

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

RED_SPACESHIP_IMAGE = pygame.image.load('spaceship_red.png')
YELLOW_SPACESHIP_IMAGE = pygame.image.load('spaceship_yellow.png')
BACKGROUND = pygame.transform.scale(pygame.image.load('space.png'), (WIDTH, HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(
    (pygame.transform.scale(RED_SPACESHIP_IMAGE, (S_WIDTH, S_HEIGHT))), 90)
YELLOW_SPACESHIP = pygame.transform.rotate(
    (pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (S_WIDTH, S_HEIGHT))), 270)


BORDER = pygame.Rect(WIDTH/2, 0, 5, HEIGHT)
        
        
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
    text = WINNER_FONT.render(winner_text, 1, RED)
    WIN.blit(text, (WIDTH/2 - text.get_width() / 2, HEIGHT/2 - text.get_height()/2 ))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    clock = pygame.time.Clock()
    run = True
    red_spaceship = pygame.Rect(10, HEIGHT/2, S_WIDTH, S_HEIGHT)
    yellow_spaceship = pygame.Rect(WIDTH - 75, HEIGHT/2, S_WIDTH, S_HEIGHT)
    red_health = 3
    yellow_health = 3
    red_bullets = []
    yellow_bullets = []
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(red_spaceship.x + red_spaceship.width, red_spaceship.y + red_spaceship.height/2 - 2, 10, 5)
                    red_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(yellow_spaceship.x , yellow_spaceship.y + yellow_spaceship.height/2 - 2, 10, 5)
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
    