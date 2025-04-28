import threading
import pygame
import socket
import sys
import time
import random

# initial spawn locations
default_player_x = 300
default_player_y = 550  # closer to the bottom

playerPosX = default_player_x
playerPosY = default_player_y

# movement speed (increase to make user move faster)
MOVE_SPEED = 20

# first item spawn location
itemX = random.randint(100, 700)
itemY = 0

score = 0
lives = 3  # start with three lives
gameStarted = False
game_over = False
game_win = False  # track win state

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

characterImage = pygame.image.load('./assets/bucket.png')
characterImage = pygame.transform.scale(characterImage, (75, 75))

itemImage = pygame.image.load('./assets/sponge.png')
itemImage = pygame.transform.scale(itemImage, (75, 75))

def GameThread():
    pygame.init()
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)
    font = pygame.font.SysFont(None, 36)
    font_big = pygame.font.SysFont(None, 72, bold=True)
    font_small = pygame.font.SysFont(None, 36)

    fps = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Welcome to CCN games')

    global playerPosX, playerPosY, itemX, itemY, score, lives, game_over, game_win

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # restart logic on game over or win
            if (game_over or game_win) and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                score = 0
                lives = 3
                playerPosX = default_player_x
                playerPosY = default_player_y
                itemX = random.randint(100, 700)
                itemY = 0
                game_over = False
                game_win = False

        screen.fill(background)

        if not game_over and not game_win:
            rect1 = pygame.Rect(0, 0, 50, 50)
            rect2 = pygame.Rect(0, 0, 75, 75)

            rect1.center = (playerPosX, playerPosY)
            rect2.center = (itemX, itemY)

            screen.blit(characterImage, (rect1.x, rect1.y))
            screen.blit(itemImage, (rect2.x, rect2.y))

            collision = rect1.colliderect(rect2)
            #pygame.draw.rect(screen, shapeColor, rect1)

            if collision:
                pygame.draw.rect(screen, shapeColorOver, rect2, 6, 1)
                score += 1
                time.sleep(0.1)
                # check win condition
                if score > 9:
                    game_win = True
                else:
                    itemX = random.randint(100, 700)
                    itemY = 0
            else:
                #pygame.draw.rect(screen, shapeColor, rect2, 6, 1)
                # check if item passed bottom
                if itemY > SCREEN_HEIGHT:
                    lives -= 1
                    itemX = random.randint(100, 700)
                    itemY = 0
                    if lives <= 0:
                        game_over = True

            # draw score and lives
            score_surf = font.render(f"Score: {score}", True, (0, 0, 0))
            lives_surf = font.render(f"Lives: {lives}", True, (0, 0, 0))
            screen.blit(score_surf, (10, 10))
            screen.blit(lives_surf, (10, 50))

        elif game_over:
            # game over screen
            lost_surf = font_big.render("You Lost", True, (255, 0, 0))
            restart_surf = font_small.render("Press 'R' to Restart", True, (255, 0, 0))
            screen.blit(lost_surf, (SCREEN_WIDTH // 2 - lost_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_surf, (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        elif game_win:
            # win screen
            gold = (255, 215, 0)
            win_surf = font_big.render("You Win!", True, gold)
            restart_surf = font_small.render("Press 'R' to Restart", True, gold)
            screen.blit(win_surf, (SCREEN_WIDTH // 2 - win_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_surf, (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

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
        if data == 'w': playerPosY -= MOVE_SPEED
        if data == 's': playerPosY += MOVE_SPEED
        if data == 'a': playerPosX -= MOVE_SPEED
        if data == 'd': playerPosX += MOVE_SPEED

    conn.close()

#adjusts both player and item speed based on score
def itemSpeed():
    global gameStarted, itemY, game_over, game_win, score, MOVE_SPEED
    while True:
        if gameStarted and not game_over and not game_win:
            itemY += 15 # faster drop
            time.sleep(0.2-(score/70))
            MOVE_SPEED = 20 + score


t1 = threading.Thread(target=GameThread)
t2 = threading.Thread(target=ServerThread)
t3 = threading.Thread(target=itemSpeed)
t1.start(); t2.start(); t3.start()
