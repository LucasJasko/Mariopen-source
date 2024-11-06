# Example file showing a circle moving on screen
import pygame, sys, os
from pygame.locals import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#PHYSIQUE
gravity = 981.0
velocity_y = 0   # Vitesse verticale
is_jumping = False
jump_speed = -500  # Vitesse initiale du saut (négative car Y augmente vers le bas)

# Paramètres du sol et du joueur
FLOOR_HEIGHT = 100
TILE_WIDTH = 64
floor_rect = pygame.Rect(0, screen.get_height() - FLOOR_HEIGHT, screen.get_width(), FLOOR_HEIGHT)
player_radius = 40
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - FLOOR_HEIGHT - player_radius)


# Crée ou charge la texture du sol
floor_texture = pygame.Surface((screen.get_width(), FLOOR_HEIGHT))
for x in range(0, screen.get_width(), 64):
    floor_texture.blit(floor_texture, (x, 0))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Détection de l'appui sur la touche espace pour sauter
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_jumping:
            velocity_y = jump_speed
            is_jumping = True
    # Gravitée
    velocity_y += gravity * dt
    player_pos.y += velocity_y * dt
    # Collision avec le sol
    if player_pos.y > screen.get_height() - FLOOR_HEIGHT - player_radius:
        player_pos.y = screen.get_height() - FLOOR_HEIGHT - player_radius
        velocity_y = 0
        is_jumping = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    # Dessin du sol avec la texture
    screen.blit(floor_texture, floor_rect)
    pygame.draw.circle(screen, "red", player_pos, 40)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()