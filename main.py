import pygame
import sys

# Initialize Pygame and the mixer
pygame.init()
pygame.mixer.init()

# Load the music
pygame.mixer.music.load('sound/music.mp3')
pygame.mixer.music.play(-1)  # Play the music indefinitely

pygame.mixer.music.set_volume(0.1)

# Set up the display
window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
FPS = 20

# Load the image
wall_image = pygame.image.load('images/wall.png')
wall_rect = wall_image.get_rect()
wall_rect.bottom = 500  # Set the bottom of the image to the bottom of the screen

running = True

class SpriteCutter:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
    
    def cut_sprite(self, x, y, width, height):
        sprite = self.image.subsurface(pygame.Rect(x, y, width, height))
        return sprite

class Hero(pygame.sprite.Sprite):
    
    def __init__(self):
        sp_cut = SpriteCutter('images/mario.png')  # Corrected the path separator
        self.sprite_right = []
        self.sprite_left = []
        self.direction = 'right'  # Initial direction
        self.x, self.y = 6, 0  # Corrected variable assignment
        self.sprite_index = 0
        h = 50
        w = 35
        for i in range(4):
            self.sprite_left.append(sp_cut.cut_sprite(self.x, self.y, w, h))  # Corrected sprite creation
            self.x += w
            self.sprite_right.append(pygame.transform.flip(self.sprite_left[-1], True, False))

    def get_current_sprite(self):
        if self.direction == 'right':
            return self.sprite_right[self.sprite_index % 4]
        elif self.direction == 'left':
            return self.sprite_left[self.sprite_index % 4]
    
    # Inside the Hero class
    def update_position(self, keys):
        speed = 8  # Adjust the speed as needed
        if keys[pygame.K_w]:  # Move up
            self.y -= speed
            self.sprite_index += 1
        if keys[pygame.K_a]:  # Move left
            self.x -= speed
            if self.direction == 'right':
                self.sprite_index = 0
            else:
                self.sprite_index += 1
            self.direction = 'left'
        if keys[pygame.K_s]:  # Move down
            self.y += speed
            self.sprite_index += 1
        if keys[pygame.K_d]:  # Move right
            self.x += speed
            if self.direction == 'left':
                self.sprite_index = 0
            else:
                self.sprite_index += 1
            self.direction = 'right'    


    def draw(self, screen):
        current_sprite = self.get_current_sprite()
        screen.blit(current_sprite, (self.x, self.y))
    
hero = Hero()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game sprites
    keys = pygame.key.get_pressed()
    hero.update_position(keys)
    window.fill((0, 0, 0))
    # Blit the image onto the screen
    window.blit(wall_image, wall_rect)
    
    # Draw the 'mario.png' sprite
    hero.draw(window)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()