import pygame
import random
import requests
import time

def register(username, password):
    response = requests.post(
        "http://127.0.0.1:8000/register",
        json={"username": username, "password": password}
    )
    print(response.json())

def login(username, password):
    response = requests.post(
        "http://127.0.0.1:8000/login",
        json={"username": username, "password": password}
    )
    print(response.json())
    return response.status_code == 200

def save_score(username, score):
    response = requests.post(
        "http://127.0.0.1:8000/save_score",
        json={"username": username, "score": score}
    )
    print(response.json())

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Snake-Game")

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()

        self.rect.center = (
            screen_width // 2,
            screen_height // 2
        )

        self.speed = 20
        self.dx = self.speed
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

class Apple(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.x = random.randint(0, screen_width - 40)
        self.rect.y = random.randint(0, screen_height - 40)

spike_size = 20

def draw_spikes():

    for x in range(0, screen_width, spike_size):
        pygame.draw.polygon(screen, (255, 0, 0), [(x, 0), (x + 10, 20), (x + 20, 0)])
        pygame.draw.polygon(screen, (255, 0, 0), [(x, screen_height), (x + 10, screen_height - 20), (x + 20, screen_height)])
    for y in range(0, screen_height, spike_size):
        pygame.draw.polygon(screen, (255, 0, 0), [(0, y), (20, y + 10), (0, y + 20)])
        pygame.draw.polygon(screen, (255, 0, 0), [(screen_width, y), (screen_width - 20, y + 10), (screen_width, y + 20)])

player = Player()
apple = Apple()
all_sprites = pygame.sprite.Group(player, apple)
snake_body = []
score = 0

font = pygame.font.SysFont(None, 40)

username = ""
password = ""
active_input = "username"

def switch_input():
    global active_input
    active_input = "password" if active_input == "username" else "username"

login_screen = True
logged_in = False
mode = "login"   
clock = pygame.time.Clock()

while login_screen:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                mode = "register" if mode == "login" else "login"
            if event.key == pygame.K_q:
                switch_input()
            elif event.key == pygame.K_BACKSPACE:
                if active_input == "username":
                    username = username[:-1]
                else:
                    password = password[:-1]
            elif event.key == pygame.K_F1:
                register(username, password)
            elif event.key == pygame.K_F2:
                if mode == "login":
                    logged_in = login(username, password)
                    if logged_in:
                        login_screen = False
                else:
                    register(username, password)
            else:
                if active_input == "username":
                    username += event.unicode
                else:
                    password += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(startbutton.pos):
                    running = True
                else:
                    running = False

    screen.blit(font.render("LOGIN SCREEN", True, (0, 0, 0)), (300, 100))
    screen.blit(
        font.render(f"MODE: {mode.upper()} (TAB)", True, (0, 0, 0)),
        (250, 150)
    )
    screen.blit(font.render("Username:", True, (0, 0, 0)), (150, 220))
    screen.blit(font.render(username, True, (0, 0, 0)), (350, 220))
    screen.blit(font.render("Password:", True, (0, 0, 0)), (150, 320))
    screen.blit(font.render("*" * len(password), True, (0, 0, 0)), (350, 320))
    startbutton = screen.blit(font.render("START GAME", True, (0, 0, 0)), (300, 350))
    pygame.display.flip()
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()

if not logged_in:
    quit()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT and player.dx == 0:
                player.dx = -player.speed
                player.dy = 0

            elif event.key == pygame.K_RIGHT and player.dx == 0:
                player.dx = player.speed
                player.dy = 0

            elif event.key == pygame.K_UP and player.dy == 0:
                player.dx = 0
                player.dy = -player.speed

            elif event.key == pygame.K_DOWN and player.dy == 0:
                player.dx = 0
                player.dy = player.speed

    if player.rect.colliderect(apple.rect):
        apple.randomize_position()
        snake_body.append(player.rect.copy())
        score += 1

    for i in range(len(snake_body) - 1, 0, -1):

        snake_body[i].x = snake_body[i - 1].x
        snake_body[i].y = snake_body[i - 1].y

    if len(snake_body) > 0:

        snake_body[0].x = player.rect.x
        snake_body[0].y = player.rect.y


    player.update()

    if (
        player.rect.x < 0 or
        player.rect.x >= screen_width or
        player.rect.y < 0 or
        player.rect.y >= screen_height
    ):

        save_score(username, score)
        running = False

    screen.fill((255, 255, 255))

    all_sprites.draw(screen)

    for segment in snake_body:
        pygame.draw.rect(screen, (0, 200, 0), segment)

    draw_spikes()

    screen.blit(
        font.render(f"Score: {score}", True, (0, 0, 0)),
        (10, 10)
    )

    pygame.display.flip()

    clock.tick(10)

pygame.quit()