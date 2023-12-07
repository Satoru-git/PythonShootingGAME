import pygame
from pygame import mixer #音声出力のためのインポート
import random
import math
pygame.init() # pygame初期化

screen = pygame.display.set_mode((800,600)) # スクリーンサイズ
# screen.fill((150,150,150)) # 背景色の設定
pygame.display.set_caption("Invaders Game") # window Title変更


# Player
playerImg = pygame.image.load('player.png') # 使用画像の設定
playerX, playerY= 370, 480 # 画像配置 X, Y 座標
playerX_change = 0


# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 4, 40

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 3
bullet_state = 'ready'

def player(x, y):
    screen.blit(playerImg, (x, y)) # 画像表示

def enemy(x, y):
    screen.blit(enemyImg, (x, y)) # 画像表示

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Score 
score_value = 0 

# mixer.Sound('laser.wav').play() # 音声出力
mixer.Sound('background.wav').play() # 音声出力


running = True
while running:
    
    screen.fill((0, 0, 0))

    for event in pygame.event.get(): # ユーザーのアクションを常に取得
        if event.type == pygame.QUIT:
            running = False # ×ボタンが押されたらwhile文を終了

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    mixer.Sound('laser.wav').play() # 音声出力
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy
    if enemyY > 440:
        break
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX = 736
        enemyX_change = -4
        enemyY += enemyY_change

    # Bullete Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision 
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # Score
    font = pygame.font.SysFont(None, 80) # フォント設定
    score = font.render(f"Score : {str(score_value)}" , True, (255, 255, 255)) #メッセージ設定
    screen.blit(score, (20, 50)) # メッセージ設定

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update() # 画像、音声、メッセージを表示するために必要