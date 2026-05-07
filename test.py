import pygame
import requests

pygame.init()

# =========================
# SCREEN
# =========================
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Snake Login")

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# =========================
# FONT
# =========================
font = pygame.font.SysFont(None, 40)

# =========================
# INPUT BOXES
# =========================
username_text = ""
password_text = ""

active_input = "username"

message = ""

mode = "login"

# =========================
# API FUNCTIONS
# =========================
def register(username, password):

    response = requests.post(
        "http://127.0.0.1:8000/register",
        json={
            "username": username,
            "password": password
        }
    )

    return response.json()


def login(username, password):

    response = requests.post(
        "http://127.0.0.1:8000/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response


# =========================
# MAIN LOOP
# =========================
running = True

clock = pygame.time.Clock()

logged_in = False

while running:

    screen.fill(WHITE)

    # =========================
    # EVENTS
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Switch inputs
            if event.key == pygame.K_TAB:

                if active_input == "username":
                    active_input = "password"

                else:
                    active_input = "username"

            # Backspace
            elif event.key == pygame.K_BACKSPACE:

                if active_input == "username":
                    username_text = username_text[:-1]

                else:
                    password_text = password_text[:-1]

            # Enter
            elif event.key == pygame.K_RETURN:

                if mode == "register":

                    data = register(
                        username_text,
                        password_text
                    )

                    message = data["message"]

                else:

                    response = login(
                        username_text,
                        password_text
                    )

                    if response.status_code == 200:

                        message = "Login successful"

                        logged_in = True

                        running = False

                    else:

                        message = "Invalid login"

            # Switch mode
            elif event.key == pygame.K_F1:

                mode = "login"

            elif event.key == pygame.K_F2:

                mode = "register"

            # Typing
            else:

                if active_input == "username":
                    username_text += event.unicode

                else:
                    password_text += event.unicode

    # =========================
    # DRAW TEXT
    # =========================
    title = font.render(
        f"{mode.upper()}",
        True,
        BLACK
    )

    screen.blit(title, (340, 50))

    # Username label
    username_label = font.render(
        "Username:",
        True,
        BLACK
    )

    screen.blit(username_label, (150, 180))

    # Password label
    password_label = font.render(
        "Password:",
        True,
        BLACK
    )

    screen.blit(password_label, (150, 280))

    # =========================
    # INPUT BOXES
    # =========================
    username_box = pygame.Rect(350, 170, 300, 50)

    password_box = pygame.Rect(350, 270, 300, 50)

    pygame.draw.rect(screen, GRAY, username_box)

    pygame.draw.rect(screen, GRAY, password_box)

    # Username text
    username_surface = font.render(
        username_text,
        True,
        BLACK
    )

    screen.blit(
        username_surface,
        (username_box.x + 10, username_box.y + 10)
    )

    # Hidden password
    hidden_password = "*" * len(password_text)

    password_surface = font.render(
        hidden_password,
        True,
        BLACK
    )

    screen.blit(
        password_surface,
        (password_box.x + 10, password_box.y + 10)
    )

    # Active border
    if active_input == "username":

        pygame.draw.rect(
            screen,
            GREEN,
            username_box,
            3
        )

    else:

        pygame.draw.rect(
            screen,
            GREEN,
            password_box,
            3
        )

    # =========================
    # MESSAGE
    # =========================
    message_surface = font.render(
        message,
        True,
        RED
    )

    screen.blit(message_surface, (250, 400))

    # =========================
    # HELP TEXT
    # =========================
    help_text = font.render(
        "F1 = Login | F2 = Register | ENTER = Submit",
        True,
        BLACK
    )

    screen.blit(help_text, (80, 500))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

# =========================
# RESULT
# =========================
if logged_in:

    print("Start Snake Game Here")
else:

    quit()