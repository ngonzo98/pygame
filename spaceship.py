"""
Created on 11/13/19
starship.py
@author: Natalia Gonzalez
"""
# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for acess to key coordinates
from pygame.locals import (
        RLEACCEL,
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        QUIT
)

# Define the screen width and height
screenWidth = 800
screenHeight = 600

# Define a player object
# using the pygame.sprite.Sprite
# and use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("ship.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on pressed keys
    def update(self, pressed):
        if pressedKeys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressedKeys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressedKeys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressedKeys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        
        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screenWidth:
            self.rect.right = screenWidth
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screenHeight:
            self.rect.bottom = screenHeight
  
# Define the enemy object  
# and use and image for the sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("rock.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting positing and speed
        # of the Enemy object is randomly generated
        self.rect = self.surf.get_rect(
                center =(
                        random.randint(screenWidth + 20, screenWidth + 100),
                        random.randint(0, screenHeight),
                        )
                )
        self.speed = random.randint(5, 20)
    # Move the sprite based on speed
    # and then it will be removed when it passes the
    # left edge of the window
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)


# Set the player
player = Player()

# Create groups to hold enemy sprites
enemies = pygame.sprite.Group()
sprites = pygame.sprite.Group()
sprites.add(player)

# Setup the clock to fix the framerate
clock = pygame.time.Clock()

running = True #this is keep the loop running

while running:
    # looks at every event in the game
    # and checks what the user did to 
    # close the screen
    for event in pygame.event.get():
        # Did the user press a key?
        if event.type == KEYDOWN:
            # Did the user press the Escape key?
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the close button?        
        elif event.type == QUIT:
            running = False
        # This will add a new enemy
        elif event.type == ADDENEMY:
            # Create the new enemy
            new_enemy = Enemy()
            enemies.add(new_enemy)
            sprites.add(new_enemy)
    
    # Get the pressed keys and check user input
    pressedKeys = pygame.key.get_pressed()
    player.update(pressedKeys)
    
    # Update the enemies position
    enemies.update()
    
    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    # Draw all of the sprites
    for entity in sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # This will remove the player
        player.kill()
        # and then stop the loop
        running = False

    # Update the display
    pygame.display.flip()
    
    # The program will maintain a rate of 30 frames per second
    clock.tick(30)