import pygame
import math
import random
from map import mapObjects, mapChunks

pygame.init()
screen = pygame.display.set_mode((1720, 980))
background = pygame.image.load("./assets/img/backgroundmario.png")
clock = pygame.time.Clock()
screenHeight = screen.get_height()
screenWidth = screen.get_width()
alpha = (255, 255, 255, 0)


class World:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = screen.get_height()
        self.width = 0
        self.worldHeight = 33
        self.chunckAmount = 10
        self.chuckWidth = 58
        self.gravity = 0.9
        self.scrollSpeed = 6
        self.pattern = []

    def randomise(self):
        for y in range(self.worldHeight):
            self.pattern += [[]]
            if y < self.worldHeight - 3:
                if y % 4 == 0 and y != 0:
                    self.pattern[y] += mapObjects[random.randint(1,6)]         
                else:
                    self.pattern[y] += mapObjects[0]  
            else:
                self.pattern[y] += [1] * self.chuckWidth
    
    def setChunks(self, index):
            self.pattern = mapChunks[index]
            
    def draw(self):
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[y])):
                rect = pygame.Rect(x*30 + self.x, y*30 + self.y, 30, 30)
                if self.pattern[y][x] == 1:
                    pygame.draw.rect(screen, "red", rect)
                    pygame.draw.rect(screen, "white", rect, 1)
                if self.pattern[y][x] == 2:
                    pygame.draw.rect(screen, "blue", rect)
                    pygame.draw.rect(screen, "white", rect, 1)


class Character:

    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 60)) 
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.x = x
        self.y = y
        self.can_jump = False
        self.jumpSpeed = -20
        self.initSpeed = 1
        self.capSpeed = 8
        self.vel_y = 0.3

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def setGravity(self):
        self.worldX = round((self.x - world.x) // 30)
        self.worldY = round((self.y - world.y) // 30)
        self.worldHeight = math.ceil(self.height / 30)
        self.worldwidth = math.ceil(self.width / 30)
        self.vel_y += world.gravity
        self.y += self.vel_y
        for y in range(len(world.pattern)):
            for x in range(len(world.pattern[y])):
                # Si la case est un obstacle:
                if world.pattern[y][x] == 1:
                    # Si le personnage se trouve en abscisse sur l'obstacle:
                    if self.worldX == x or self.worldX + self.worldwidth == x:
                        # Si le personnage est en train de tomber ou est au sol:
                        if self.vel_y >= 0:
                            # Si le bas du personnage touche un obstacle:
                            if self.worldY + self.worldHeight == y and self.worldY < y:
                                self.y = y * 30 - self.height
                                self.vel_y = 0
                                self.can_jump = True
                        # Si le personnage est en train de sauter:
                        elif self.vel_y < 0:
                            # Si le haut du personnage touche un obstacle:
                            if self.worldY == y:
                                self.y = (y + 1) * 30
                                self.vel_y = 0
                        

    def move(self):
        middleScreen = screenWidth / 2
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_SPACE] and self.can_jump:
            self.vel_y = self.jumpSpeed
            self.can_jump = False
        elif self.keys[pygame.K_q]:
            self.initSpeed = self.initSpeed * 1.1
            if self.initSpeed >= self.capSpeed:
                self.initSpeed = self.capSpeed
            if world.x < 0:
                if self.x <= middleScreen - 400:
                    world.x += world.scrollSpeed
                    self.x = self.x
                elif self.x > middleScreen - 400:
                    self.x -= self.initSpeed
            elif world.x >= 0:  
                world.x = 0
                self.x -= self.initSpeed
                if self.x <= 0:
                    self.x = 0
            if world.pattern[self.worldY + 1][self.worldX - 1] == 1:
                self.x = self.worldX * 30 + self.worldwidth
        elif self.keys[pygame.K_d]:
            self.initSpeed = self.initSpeed * 1.1
            if self.initSpeed >= self.capSpeed:
                self.initSpeed = self.capSpeed
            if abs(world.x) + screenWidth < world.width:
                if self.x >= middleScreen + 400:
                    world.x -= world.scrollSpeed
                    self.x = self.x
                if self.x < middleScreen + 400:
                    self.x += self.initSpeed
            else:
                world.x = world.x
                self.x += self.initSpeed
                if self.x + self.width >= screenWidth:
                    self.x = self.x - self.width
            if world.pattern[self.worldY + 1][self.worldX + 1] == 1:
                self.x = self.worldX * 30 + self.worldwidth
        else:
            self.initSpeed = 1

world = World(0, 0)
for i in range(0, world.chunckAmount * 1740, 1740):
    if i == 0:
        world.setChunks('0')
    elif i == 1740:
        world.setChunks('1')
    elif i > 1740:
        world.randomise()
    world.width += 1740

player = Character("assets/img/Ark.gif", 100, 100)

print(player.width)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()
    
    screen.blit(background, (0, 0))


    
    world.draw()
    player.draw()
    player.setGravity()
    player.move()

    clock.tick(60) 
pygame.quit()


