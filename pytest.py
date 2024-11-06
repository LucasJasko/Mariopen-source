import pygame
import os
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
world_y = screen.get_height()

class Character:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.height = self.image.get_height()
        self.jumping = False
        self.can_jump = False
        # for i in range(1, 5):
        #     img = pygame.image.load("main-char/carotte1.png").convert()
        #     # os.path.join('images', 'hero' + str(i) + '.png')
        #     img.convert_alpha()
        #     img.set_colorkey((0, 0, 0))
        #     self.images.append(img)
        #     self.image = self.images[0]
        #     self.rect = self.image.get_rect()
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def gravity(self):
        self.y += 3.2
        if self.y + self.height > world_y:
            self.y = world_y - self.height
            self.can_jump = True
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_jump:
            self.vel_y = -15
            self.can_jump = False
            self.y = 200
        if keys[pygame.K_q]:
            self.x -= 300 * dt
        if keys[pygame.K_d]:
            self.x += 300 * dt


player = Character("main-char/carotte1.png", 100, 100)




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("blue")

    dt = clock.tick(60) / 1000

    player.draw(screen)
    player.gravity()
    player.move()
    pygame.display.update()
    clock.tick(60) 

pygame.quit()


