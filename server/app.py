import threading
import pygame
import socket
import sys
import time
import random

#player spawn location (moved closer to bottom)
playerPosX = 300
playerPosY = 550

#first item spawn location
itemX = random.randint(100,700)
itemY = 0

score = 0
gameStarted = False

def GameThread():
    pygame.init()
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)
    font = pygame.font.SysFont(None, 36)

    fps = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Welcome to CCN games')

    global playerPosX, playerPosY, itemX, itemY, score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background)
        rect1 = pygame.Rect(0, 0, 25, 25)
        rect2 = pygame.Rect(0, 0, 75, 75)
        rect1.center = (playerPosX, playerPosY)
        rect2.center = (itemX, itemY)

        collision = rect1.colliderect(rect2)
        pygame.draw.rect(screen, shapeColor, rect1)

        if collision:
            pygame.draw.rect(screen, shapeColorOver, rect2, 6, 1)
            score += 1
            time.sleep(0.1)
            itemX = random.randint(100, 700)
            itemY = 0
        else:
            pygame.draw.rect(screen, shapeColor, rect2, 6, 1)

        # draw score
        score_surf = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))

        pygame.display.update()
        fps.tick(60)

def ServerThread():
    global gameStarted, playerPosX, playerPosY
    host = '127.0.0.1'
    print('Server listening on', host)
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    print("Server enabled...")
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from:", address)
    gameStarted = True

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        if data == 'w': playerPosY -= 10
        if data == 's': playerPosY += 10
        if data == 'a': playerPosX -= 10
        if data == 'd': playerPosX += 10

    conn.close()

def itemDrop():
    global gameStarted, itemY
    while True:
        if gameStarted:
            itemY += 15    # increased drop speed
            time.sleep(0.2)  # shorter delay for faster fall

t1 = threading.Thread(target=GameThread)
t2 = threading.Thread(target=ServerThread)
t3 = threading.Thread(target=itemDrop)
t1.start(); t2.start(); t3.start()
