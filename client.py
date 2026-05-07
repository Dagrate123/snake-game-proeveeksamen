import pygame
import random

# 1. Initialize Pygame
pygame.init()

# 2. Create the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake-Game")

# 3. Define the Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0)) 
        
        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
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
        self.rect.x = random.randint(0, screen_width - 20)
        self.rect.y = random.randint(0, screen_height - 20)
    
# 4. Setup Game Objects
player = Player()
apple = Apple()
all_sprites = pygame.sprite.Group()
all_sprites.add(player, apple)


# 5. Main Game Loop
running = True
clock = pygame.time.Clock()

snake_body = []


while running:
    # Handle Events
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

    for i in range(len(snake_body) - 1, 0, -1):
        snake_body[i].x = snake_body[i - 1].x
        snake_body[i].y = snake_body[i - 1].y

    if len(snake_body) > 0:
        snake_body[0].x = player.rect.x
        snake_body[0].y = player.rect.y

    player.update()

    # Get Keys & Update Logic
    keys = pygame.key.get_pressed()

    # Drawing
    screen.fill((255, 255, 255))  # White background
    all_sprites.draw(screen)      # Draw all sprites in the group

    for segment in snake_body:
        pygame.draw.rect(screen, (0, 200, 0), segment)

    pygame.display.flip()         # Update display
    clock.tick(60)                # Limit to 60 FPS


pygame.quit()
