import threading
import pygame
import socket
import sys
import time
import random

name = "test"

#player spawn location
playerPosX = 300
playerPosY = 200

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
    
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 800, 600
    rect2 = pygame.Rect(0, 0, 75, 75)
    rect1 = pygame.Rect(0, 0, 25, 25)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')
    
    colorRect = (shapeColor)
    colorRect2 = (shapeColorOver)
    global playerPosX
    global playerPosY

    global itemX
    global itemY
    global score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background)
        rect1.center = (playerPosX, playerPosY)
        rect2.center = (itemX, itemY)
        collision = rect1.colliderect(rect2)
        pygame.draw.rect(screen, colorRect, rect1)
        if collision:
            pygame.draw.rect(screen, colorRect2, rect2, 6, 1)
            time.sleep(0.1)
            itemX = random.randint(100, 700)
            itemY = 0
        else:
            pygame.draw.rect(screen, colorRect, rect2, 6, 1)
        pygame.display.update()
        fps.tick(60)


    pygame.quit()


def ServerThread():
    global gameStarted
    global playerPosY
    global playerPosX
    # get the hostname
    # host = socket.gethostbyname(socket.gethostname())
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # host = s.getsockname()[0]
    # s.close()

    host = '127.0.0.1'
    print('Server listening on', host)

    port = 5000  # initiate port no above 1024
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    gameStarted = True
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            playerPosY -= 10
        if(data == 's'):
            playerPosY += 10
        if(data == 'a'):
            playerPosX -= 10
        if(data == 'd'):
            playerPosX += 10
    conn.close()  # close the connection

def itemDrop():
    global gameStarted
    global itemY
    while True:
        if gameStarted:
            itemY += 10
            time.sleep(0.3)



t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t3 = threading.Thread(target=itemDrop, args=[])
t1.start()
t2.start()
t3.start()


