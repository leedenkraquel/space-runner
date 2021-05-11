# import libraries
import pygame
import math
import random
import time

# initialize variables
pygame.init()
pygame.mixer.init()
pygame.font.init()
width, height = 1020, 690
screen = pygame.display.set_mode((width, height))
spaceVel = 0.05
spacePos = 0
shipPos = [width / 2, height / 2]
shipVel = [0,0]
shipAcc = 0.01
shipMaxVel = 8
shipRot = 1
angle = 0
accel = False
left = False
right = False
brake = False
rocks = [[-width, 0, 10, 0, 0]]
rockVel = 1
rockRot = 0.2
rockTimerInit = 500
rockTimer = rockTimerInit
rockTimerEnd = 0
healthValue = 3

# load images
ship = pygame.image.load("assets/ship.png")
if width < height:
    scalar = int(width / 10)
else:
    scalar = int(height / 10)
player = pygame.transform.scale(ship, (scalar, scalar))
lives = pygame.transform.scale(ship, (10, 10))
comet = pygame.image.load("assets/comet.png")
space = pygame.image.load("assets/space.png")
controls = pygame.image.load("assets/wasd_keys.png")
controls = pygame.transform.scale(controls, (int(width / 3), int(height / 3)))

# load audio
damage = pygame.mixer.Sound("assets/explode.wav")
damage.set_volume(0.05)
pygame.mixer.music.load("assets/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# start menu
menu = 1
while menu:
    screen.fill(0)
    # move the background
    if spacePos < space.get_width():
        spacePos += spaceVel
    else:
        spacePos = 0
    # display the background
    for x in range(int(width / space.get_width() + 1 + space.get_width())):
        for y in range(int(height / space.get_height() + 1)):
            screen.blit(space, (x * space.get_width() + spacePos - space.get_width(), y * space.get_height()))
    # display introduction clause
    font = pygame.font.SysFont("comicsansms", 24)
    intro = font.render("Press Space to Start", True, (255, 255, 255))
    introRect = intro.get_rect()
    introRect.centerx = screen.get_rect().centerx
    introRect.centery = screen.get_rect().centery / 2
    screen.blit(intro, introRect)
    contRect = controls.get_rect()
    contRect.centerx = screen.get_rect().centerx
    contRect.centery = screen.get_rect().centery
    screen.blit(controls, contRect)
    instr = font.render("Avoid Getting Hit", True, (255, 255, 255))
    instrRect = instr.get_rect()
    instrRect.centerx = screen.get_rect().centerx
    instrRect.centery = screen.get_rect().centery * 1.5
    screen.blit(instr, instrRect)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            menu = 0
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()    
running = True
startTime = 0
while 1:
    startTime = time.time()
    # updates that run every tick
    while running:
        # decrement the rock spawn timer
        rockTimer -= 1
        # clear the screen between draws
        screen.fill(0)
        # move the background
        if spacePos < space.get_width():
            spacePos += spaceVel
        else:
            spacePos = 0
        # display the background
        for x in range(int(width / space.get_width() + 1 + space.get_width())):
            for y in range(int(height / space.get_height() + 1)):
                screen.blit(space, (x * space.get_width() + spacePos - space.get_width(), y * space.get_height()))
        # update ship position
        if left:
            angle = (angle + shipRot) % 360
        elif right:
            angle = (angle - shipRot) % 360
        if accel:
            if shipVel[0] < shipMaxVel:
                shipVel[0] += shipAcc
            else:
                shipVel[0] = shipMaxVel
            if shipVel[1] < shipMaxVel:
                shipVel[1] += shipAcc
            else:
                shipVel[1] = shipMaxVel
        elif brake:
            if shipVel[0] > 0:
                shipVel[0] -= shipAcc * 2
            else:
                shipVel[0] = 0
            if shipVel[1] > 0:
                shipVel[1] -= shipAcc * 2
            else:
                shipVel[1] = 0
        else:
            if shipVel[0] > 0:
                shipVel[0] -= shipAcc
            else:
                shipVel[0] = 0
            if shipVel[1] > 0:
                shipVel[1] -= shipAcc
            else:
                shipVel[1] = 0
        shipPos[0] -= math.sin(math.radians(angle)) * shipVel[0]
        shipPos[1] -= math.cos(math.radians(angle)) * shipVel[1]
        # wrap the screen
        if shipPos[0] < 0:
            shipPos[0] = width
        elif shipPos[0] > width:
            shipPos[0] = 0
        if shipPos[1] < 0:
            shipPos[1] = height
        elif shipPos[1] > height:
            shipPos[1] = 0
        player = pygame.transform.rotate(ship, angle)
        shipRect = ship.get_rect()
        shipRect.left = shipPos[0]
        shipRect.top = shipPos[1]
        shipPos1 = (shipPos[0] - player.get_rect().width / 2, shipPos[1] - player.get_rect().height / 2)
        # display ship
        screen.blit(player, shipPos1)
        # spawn a rock
        if rockTimer <= 0:
            start = random.randint(0, 3)
            if start == 0:
                rocks.append([random.randint(10, width - 10), -comet.get_height(), random.randint(scalar, scalar * 3), start, 0])
            elif start == 1:
                rocks.append([width + comet.get_width(), random.randint(10, height - 10), random.randint(scalar, scalar * 3), start, 0])
            elif start == 2:
                rocks.append([random.randint(10, width - 10), height  + comet.get_height(), random.randint(scalar, scalar * 3), start, 0])
            elif start == 3:
                rocks.append([-comet.get_width(), random.randint(10, height - 10), random.randint(scalar, scalar * 3), start, 0])
            rockTimer = rockTimerInit - rockTimerEnd
            if rockTimerEnd >= rockTimerInit:
                rockTimerEnd = rockTimerInit
            else:
                rockTimerEnd += 1
        # display rocks
        index = 0
        for rock in rocks:
            comet1 = pygame.transform.scale(comet, (rock[2], rock[2]))
            rock[4] += rockRot
            rockRect = comet1.get_rect()
            comet1 = pygame.transform.rotate(comet1, rock[4])
            rockRect.top = rock[1]
            rockRect.left = rock[0]
            dir = random.randint(1, 10)
            if rock[3] == 0:
                rock[0] += int(rock[4] / (height / dir)) * rockVel * (index % 3 - 1)
                rock[1] += rockVel
            elif rock[3] == 1:
                rock[0] -= rockVel
                rock[1] += int(rock[4] / (width / dir)) * rockVel * (index % 3 - 1)
            elif rock[3] == 2:
                rock[0] += int(rock[4] / (height / dir)) * rockVel * (index % 3 - 1)
                rock[1] -= rockVel
            elif rock[3] == 3:
                rock[0] += rockVel
                rock[1] += int(rock[4] / (width / dir)) * rockVel * (index % 3 - 1)
            if rock[1] > height + comet1.get_height() and rock[3] == 0:
                rocks.pop(index)
            elif rock[0] < 0 and rock[3] == 1:
                rocks.pop(index)
            elif rock[1] < 0 and rock[3] == 2:
                rocks.pop(index)
            elif rock[0] > width + comet1.get_width() and rock[3] == 3:
                rocks.pop(index)
            else:
                rockPos = (rock[0] - rockRect.width / 2, rock[1] - rockRect.height / 2)
                screen.blit(comet1, rockPos)
            # detect collision with rock
            if rockRect.colliderect(shipRect):
                healthValue -= 1
                rocks.pop(index)
                damage.play()
            index += 1
        # display health
        if healthValue >= 3:
            screen.blit(ship, (110, 5))
            screen.blit(ship, (60, 5))
            screen.blit(ship, (10, 5))
        elif healthValue == 2:
            screen.blit(ship, (60, 5))
            screen.blit(ship, (10, 5))
        elif healthValue == 1:
            screen.blit(ship, (10, 5))
        else:
            running = False
        # update the screen
        pygame.display.flip()
        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    accel = True
                if event.key == pygame.K_a:
                    left = True
                elif event.key == pygame.K_d:
                    right = True
                elif event.key == pygame.K_s:
                    brake = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    accel = False
                if event.key == pygame.K_a:
                    left = False
                elif event.key == pygame.K_d:
                    right = False
                elif event.key == pygame.K_s:
                    brake = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
    endTime = time.time()
    print("endTime: " + str(endTime) + " startTime: " + str(startTime))
    font = pygame.font.SysFont("comicsansms", 24)
    gameOver = font.render("Game Over", True, (255, 0, 0))
    timeSurvived = font.render("Time Survived: " + str(int((endTime - startTime) / 60)) + ":" + str(int((endTime - startTime) % 60)).zfill(2), True, (0,255,0))
    retry = font.render("Press Space to Retry", True, (255, 255, 255))
    gameOverRect = gameOver.get_rect()
    gameOverRect.centerx = screen.get_rect().centerx
    gameOverRect.centery = screen.get_rect().centery
    screen.blit(gameOver, gameOverRect)
    timeSurRect = timeSurvived.get_rect()
    timeSurRect.centerx = screen.get_rect().centerx
    timeSurRect.centery = screen.get_rect().centery + 50
    screen.blit(timeSurvived, timeSurRect)
    retryRect = retry.get_rect()
    retryRect.centerx = screen.get_rect().centerx
    retryRect.centery = screen.get_rect().centery - 50
    screen.blit(retry, retryRect)
    while running == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = True
                spaceVel = 0.05
                spacePos = 0
                shipPos = [width / 2, height / 2]
                shipVel = [0,0]
                shipAcc = 0.01
                shipMaxVel = 8
                shipRot = 1
                angle = 0
                accel = False
                left = False
                right = False
                brake = False
                rocks = [[-width, 0, 10, 0, 0]]
                rockVel = 1
                rockRot = 0.2
                rockTimerInit = 1000
                rockTimer = rockTimerInit
                rockTimerEnd = 0
                healthValue = 3
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()