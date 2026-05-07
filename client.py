import pygame

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
        # Create a 50x50 green square
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0)) 
        
        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        elif keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            
        elif keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed

        elif keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += self.speed
# 4. Setup Game Objects
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# 5. Main Game Loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get Keys & Update Logic
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Drawing
    screen.fill((255, 255, 255))  # White background
    all_sprites.draw(screen)      # Draw all sprites in the group
    
    pygame.display.flip()         # Update display
    clock.tick(60)                # Limit to 60 FPS

pygame.quit()
