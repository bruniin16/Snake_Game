import pygame
from pygame.locals import *
import random
from time import sleep

up = 0
right = 1
down = 2
left = 3

def random_pos():
    x = random.randint(0,590)
    y = random.randint(0,590)
    return (x//10 * 10, y//10 * 10)

def collision(a, b):
    return (a[0] == b[0]) and (a[1] == b[1])

def snake_bloom(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    #pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.fill(color)
    surf.set_colorkey((0, 0, 0))
    return surf

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Snake")

# Snake
snake = [(500, 500), (510, 500), (520, 500)]
skin = pygame.Surface((10,10))
skin.fill((255,255,255))

# Apple
pos_apple = random_pos()
apple = pygame.Surface((10,10))
apple.fill((255,0,0))

# Bloom and Fog
fog = pygame.Surface((1000, 600))
fog.fill((20, 20, 20))
bloom = pygame.image.load(r"./images/bloom_soft.png").convert_alpha()
bloom = pygame.transform.scale(bloom, (15, 15))
bloom_rect = bloom.get_rect()


direction = right
clock = pygame.time.Clock()

# Game Over screen
font = pygame.font.Font('freesansbold.ttf', 64)
font2 = pygame.font.Font('freesansbold.ttf', 32)
font3 = pygame.font.Font('freesansbold.ttf', 25)

game_over = font.render('GAME OVER', True, (255, 0, 0), (0, 0, 0))
try_again = font2.render('press ESC to quit.', True, (255, 255, 255), (0, 0, 0))

game_overRect = game_over.get_rect()
game_overRect.center = (500, 200)

try_againRect = try_again.get_rect()
try_againRect.center = (500, 300)

ap = 0

# Game itself
while True:
    clock.tick(25)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                if direction == down:
                    continue
                direction = up
            
            if event.key == K_s or event.key == K_DOWN:
                if direction == up:
                    continue
                direction = down
            
            if event.key == K_d or event.key == K_RIGHT:
                if direction == left:
                    continue
                direction = right
            
            if event.key == K_a or event.key == K_LEFT:
                if direction == right:
                    continue
                direction = left
    
    if snake[0][1] == 600:
        snake[0][1] == 1
    if snake[0][0] == 1000:
        snake[0][0] == 1

    if direction == up:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if direction == down:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if direction == right:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if direction == left:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    if collision(snake[0], pos_apple):   
        ap += 1
        pos_apple = random_pos()
        pygame.mixer.music.load(r"./audios/apple_1.mp3")
        pygame.mixer.music.play()
        snake.append((0,0))

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    #def render_fog(pos):
       #fog.fill((20,20,20))
       #bloom_rect.center = pos
       #fog.blit(bloom, bloom_rect)
       #screen.blit(fog, (0, 0), special_flags=BLEND_MULT)

    for pos in snake:
        screen.blit(skin, pos)
        #render_fog(pos)
        #screen.blit(snake_bloom(6, (168, 168, 168)), (pos[0]-1, pos[1]-1), special_flags = BLEND_RGB_ADD)


    for i in range(len(snake) - 1, 2, -1):
        if collision(snake[0], snake[i]):
                pygame.mixer.music.load(r"./audios/game_over.mp3")
                pygame.mixer.music.play()
                
                ans = 0
                while ans == 0:
                    screen.blit(game_over, game_overRect)
                    screen.blit(try_again, try_againRect)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                exit()
    
    if snake[0][0] < 0 or snake[0][0] >= 1000 or snake[0][1] < 0 or snake[0][1] >= 600:
        pygame.mixer.music.load(r"./audios/game_over.mp3")
        pygame.mixer.music.play()
        
        ans = 0
        while ans == 0:
            screen.blit(game_over, game_overRect)
            screen.blit(try_again, try_againRect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                
    scrtxt = str(ap)
    score = font3.render(f"score: {scrtxt}", True, (255, 255, 255), (0, 0, 0))
    scoreRect = score.get_rect()
    scoreRect.center = (60, 25)
    screen.blit(score, scoreRect)

    screen.blit(apple, pos_apple)




    pygame.display.update()