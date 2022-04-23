from dis import dis
import pygame
from pygame import *
import random
from copy import copy

class vaiseau:
    _image = None
    _pos_x = 0
    _pos_y = 0
    _game_display = None
    _scale = None
    def __init__(self, image, game_display, scale = (0, 0), pos_x = 0 , pos_y = 0):
        self._image = pygame.image.load(image)
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._game_display = game_display
        self._scale = scale
        self._image = pygame.transform.scale(self._image, scale)
    def _print(self):
        self._game_display.blit(self._image, (self._pos_x, self._pos_y))
    def get_rect(self):
        return_rect = self._image.get_rect()
        return_rect.move_ip(self._pos_x, self._pos_y)
        return return_rect

class projectile:
    _pos_x = 0
    _pos_y = 0
    _color = (0 ,0, 0)
    _size = 5
    _game_display = None
    def __init__(self, game_display ,color = (0, 0, 0), pos_x = 0 , pos_y = 0, size = 5):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self.color = color
        self._size= size
        self._game_display = game_display
    def print_circle(self):
        pygame.draw.circle(self._game_display, self.color, (self._pos_x, self._pos_y), self._size)

def end_screen(fenetre, clock):
    font = pygame.font.SysFont(None, 50)
    img = font.render("YOU LOOSE !! SPACE to restart", True, (255, 0, 0))
    while(1):
        fenetre.fill((0,0, 0))
        fenetre.blit(img, (0, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        clock.tick(60)
        pygame.display.update()

score = 0

def key_gestion(counter, asteroid_list, projectile_list, vaiseau_var, projectile_var, asteroid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile_var._pos_x = vaiseau_var._pos_x
                projectile_list.append(copy(projectile_var))
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT] and vaiseau_var._pos_x < 800 - vaiseau_var._image.get_width():
        vaiseau_var._pos_x += 5
    if pressed[pygame.K_LEFT] and vaiseau_var._pos_x > 0:
        vaiseau_var._pos_x -= 5
    if (counter % 60 == 0):
        asteroid._pos_x = random.randint(100, 500)
        asteroid_list.append(copy(asteroid))

def asteroid_gestion(asteroid_list, projectile_list):
    global score
    for node in asteroid_list:
        node._print()
        node._pos_y += 2
        if (node._pos_y > 800):
            asteroid_list.remove(node)
        for second in projectile_list:
            if node.get_rect().collidepoint(second._pos_x , second._pos_y):
                asteroid_list.remove(node)
                projectile_list.remove(second)
                score += 1

def stars(stars_var, stars_list):    
    stars_var._pos_x = random.randint(0, 800)
    stars_list.append(copy(stars_var))

    for node in stars_list:
        node.print_circle()
        node._pos_y += 5
        if (node._pos_y >= 600):
            stars_list.remove(node)
    return stars_list

def game_loop():
    global score
    pygame.init()
    counter = 0
    font = pygame.font.SysFont(None, 70)
    img = font.render("score = 0", True, (255, 255, 255))
    fenetre = pygame.display.set_mode((800, 600))
    projectile_list = []
    asteroid_list = []
    clock = pygame.time.Clock()
    vaiseau_var = vaiseau('./image/vaisseau.png', fenetre,(50, 50),300, 500)
    asteroid = vaiseau('./image/asteroid.png', fenetre, (50, 50), 0, 0)
    projectile_var = projectile(fenetre, (255, 255, 255), 300, 500)
    stars_var = projectile(fenetre, (255, 255, 255), 300, 0, 1)
    stars_list = []
    while(1):
        fenetre.fill((0,0,0))
        stars_list = stars(stars_var, stars_list)
        key_gestion(counter, asteroid_list, projectile_list, vaiseau_var, projectile_var, asteroid)
        asteroid_gestion(asteroid_list, projectile_list)
        img = font.render("score = " + str(score) , True, (255, 255, 255))
        for node in projectile_list:
            node.print_circle()
            node._pos_y -= 3
            if (node._pos_y <= 0):
                projectile_list.remove(node)
        for node in asteroid_list:
            if (node.get_rect().colliderect(vaiseau_var.get_rect()) == True):
                end_screen(fenetre, clock)
                asteroid_list = []
                projectile_list = []
                vaiseau_var = vaiseau('./image/vaisseau.png', fenetre,(50, 50),300, 500)
                score = 0
        fenetre.blit(img, (0, 0))
        vaiseau_var._print()
        clock.tick(60)
        counter += 1
        pygame.display.update()

game_loop()