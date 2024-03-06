import pygame
import random
import time
import math

pygame.init()

#Settup
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')
pygame.display.set_caption('Space invader')
pygame.display.set_icon(pygame.image.load("spaceship.png"))


##Speed of the game, if variable "times" is changed, the game becomes faster
times = 1
n = 3000

### Boss

bossImg = pygame.image.load('boss.png')
bossX = 500 + n
bossY = 50
bossX_change = 0.3
bossStatus = 'dead'
waitTimeBoss = 0
bossAppearTime = 0
hp = 5

### Boss bullets
bulletBImg2 = pygame.image.load('bossbullet2.png')
bulletBImg = pygame.image.load('bossbullet.png')
bulletBImages = [bulletBImg, bulletBImg2]
costume = 0
bulletBX = 0
bulletBY = 480
bulletBX_change = 0
bulletBY_change = 1
bulletB_state = "ready"
bulletTime = 1 # sekunde
shootingTime = 0 # laiks kurā bija izšauts
bulletAnimantion = 0
g = 5

###skerlis

skerslisImg = pygame.image.load('skerslis.png')
skerslisX = random.randint(50, 750)
skerslisY = 300

###Player

playerImg = pygame.image.load('player.png')
playerX_change = 0
playerX = 370
playerY = 480

###Enemies

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
d = 1

for i in range(num_of_enemies):
  enemyImg.append( pygame.image.load('enemy.png') )
  enemyX.append( random.randint(0,735) )
  enemyY.append( random.randint(50,150) )
  enemyX_change.append(0.3)
  enemyY_change.append(40)

x_enemyrand = random.uniform(0.5, 2)

###Bullets
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

### Result

score = 0

font = pygame.font.Font('Starjedi.ttf', 32)

textX = 10
textY = 10

### Game Over
over_font = pygame.font.Font('Starjedi.ttf', 64)

### Name FOnt
n_font = pygame.font.Font('Starjedi.ttf', 16)

#####funkcijas

def game_over_text():
    over_text = over_font.render("Game over", True, (255, 255, 0))
    screen.blit(over_text, (200, 250))

def bossComing():
    bossComingB = over_font.render("Boss is coming...", True, (255, 255, 0))
    screen.blit(bossComingB, (100, 250))


def show_score(x, y):
    scoreValue = font.render("Score : "  +  str(score), True, (255, 255, 0))
    screen.blit(scoreValue, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 30:
        return True
    else:
        return False
    
def isCollisionSkerslis(skerslisX, skerslisY, bulletX, bulletY):
    distance = math.sqrt(math.pow(skerslisX - bulletX, 2) + math.pow(skerslisY - bulletY, 2))
    if distance < 30:
        return True
    else:
        return False
def isCollisionBoss(bossX, bossY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bossX - bulletX, 2) + math.pow(bossY - bulletY, 2))
    if distance < 30:
        return True
    else:
        return False

def isCollisionPlayer(playerX, playerY, bulletBX, bulletBY):
    distance = math.sqrt(math.pow(playerX - bulletBX, 2) + math.pow(playerY - bulletBY, 2))
    if distance < 30:
        return True
    else:
        return False

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x , y))
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def boss(x, y):
    screen.blit(bossImg, (x, y))

def fire_bulletB(x, y, img):
    global bulletB_state
    bulletB_state = "fire"
    screen.blit(img, (x - 16, y - 10))

#Game Loop
running = True
while running:

    collision4 = isCollisionPlayer(playerX, playerY, bulletBX, bulletBY)

    if collision4 == True:
        game_over_text()

    current_time = time.time()
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ### Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2 * times
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2 * times
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
    playerX += playerX_change
    
    ###Boundaries

    screen.blit(skerslisImg, (skerslisX, skerslisY))
    collision2 = isCollisionSkerslis(skerslisX, skerslisY, bulletX, bulletY)
    if collision2:
        bulletY = 480
        bullet_state = "ready"


    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    ###Enemy movment
    if bossStatus == 'dead':
        for i in range(num_of_enemies):

            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.2 * x_enemyrand * times * d
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.2 * x_enemyrand * times * d
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score += 1
                print(score)

                enemyX[i] = random.randint(0, 735)
                enemyY[i]  = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

    ###Player redraw
    player(playerX, playerY)                                                                

    ###bullet movment
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    ###Score output
    show_score(textX, textY)

    ### Name
    n_text = n_font.render("SpaceInvader", True, (255, 255, 0))
    screen.blit(n_text, (10, 550))

    if score == g and bossStatus != 'alive':
        bossAppearTime = current_time
        bossStatus = 'alive'
        n = 0
        g = g + 5

    if bossStatus == 'alive':

        collision4 = isCollisionPlayer(playerX, playerY, bulletBX, bulletBY)
        if collision4:
            game_over_text()
            break

        hp_text = n_font.render("HP: " + str(hp), True, (255, 255, 0))
        screen.blit(hp_text, (600, 10))

        # d = 0
        for u in range(num_of_enemies):
            enemyY[u] = random.randint(50,100)

        ###Boss
        bossX += bossX_change

        if bossX <= 0+n:
            bossX_change =  0.3 * times
        elif bossX > 700 + n:
            bossX_change =  -0.3 * times

        if bossAppearTime + 5 > current_time and bossStatus == 'alive':
            bossComing()
        
        ###Boss damage

        collision3 = isCollisionBoss(bossX, bossY, bulletX, bulletY)
        if collision3:
            hp = hp - 1
            bulletY = 480
            bullet_state = "ready"

        if hp == 0:
            hp = 5
            bossStatus = "dead"
            bossX = 3500
            bulletBX = 3500

        boss(bossX, bossY)

        ###Boss bullet

        if bulletBY >= 600:
            bulletBY = 50
            bulletB_state = "ready"
        if bulletB_state == "fire":
            fire_bulletB(bulletBX, bulletBY, bulletBImages[costume])
            # fire_bulletB(bulletBX, bulletBY, bulletBImg2)
            bulletBY += bulletBY_change * 0.1 * times
        
        if shootingTime + 1 < current_time and bulletB_state == "ready":
            bulletBX = bossX
            bulletB_state = "fire"
            shootingTime = current_time
            # costume = random.randint(0,2)
        
        if bulletAnimantion + .25 < current_time:
            costume += 1
            if costume > 1:
                costume = 0
            bulletAnimantion = current_time

    ### Refresh
    
    x_enemyrand = random.uniform(0.5, 2)
    
    pygame.display.update()