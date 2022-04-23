# -*- coding: utf-8 -*-

import random
import pygame
from copy import copy

pygame.init() 

fenetre = pygame.display.set_mode( (600,600) )
pygame.display.set_caption("Space Invader Saad Berrada 1S1")
font = pygame.font.SysFont("police", 20)
imageAlien = pygame.image.load("alien.png")
imageVaisseau = pygame.image.load("vaisseau.png")
imageVaisseau = pygame.transform.scale(imageVaisseau, (64, 64))
positionVaisseau = (300,525)
positionAlien = [(0,10), (50,10), (100,10), (150,10), (200,10)]
direction = 1
bombe = (-1, -1)
bonus = (-1, -1)
stars = []
projectile = []


def dessiner():
    global imageAlien, imageVaisseau, fenetre, projectile, score_surface, reste_surface
    fenetre.fill( (0,0,0) )    
    stars.append((random.randint(0, 600), 0))
    for i in range(len(stars)):
        pygame.draw.circle(fenetre, (255,255,255), stars[i], 2) 
        stars[i] = (stars[i][0], stars[i][1] + 4)
    for node in stars:
        if (node[1] >= 600):
            stars.remove(node)
    fenetre.blit(imageVaisseau, positionVaisseau)
    for node in positionAlien:
        fenetre.blit(imageAlien, node) 
    if bombe != (-1, -1):
        pygame.draw.circle(fenetre, (255, 0, 0), bombe, 10)
    if bonus != (-1, -1):
        pygame.draw.circle(fenetre, (0, 0, 255), bonus, 10)
    fenetre.blit(score_surface, (0,50))
    fenetre.blit(reste_surface, (500 ,50))
    for node in projectile:
        if node != (-1, -1):
            pygame.draw.circle(fenetre, (0,255,0), node, 5) 
    pygame.display.flip()

press = True

def gererClavierEtSouris():
    global continuer, positionVaisseau, projectile, rect_vausseau, reste, press
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0

    touchesPressees = pygame.key.get_pressed() 
    if touchesPressees[pygame.K_SPACE] == True and press == True and reste > 0:
        reste -=1
        projectile.append((positionVaisseau[0] + (rect_vausseau.width / 2) , positionVaisseau[1]))
        press = False
    elif touchesPressees[pygame.K_SPACE] == False:
        press = True
    if touchesPressees[pygame.K_RIGHT] == True and positionVaisseau[0] + rect_vausseau.width <= 600 :
        positionVaisseau = ( positionVaisseau[0] + 5 , positionVaisseau[1] )
    if touchesPressees[pygame.K_LEFT] == True and positionVaisseau[0] >= 0:
        positionVaisseau = ( positionVaisseau[0] - 5 , positionVaisseau[1] )


clock = pygame.time.Clock()



def end_game():
    font_big = pygame.font.SysFont("police", 50)
    while(1):
        fenetre.fill((0,0, 0))
        end = font_big.render("it's the end", False, (255, 0, 0))
        fenetre.blit(end, (300, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        pygame.display.flip()

continuer = 1
score = 0
reste = 100
while continuer==1:
    rect_alien = []
    score_surface = font.render("score = " + str(score), False, (255, 0, 0))
    reste_surface =  font.render("reste = " + str(reste), False, (255, 0, 0))
    clock.tick(50)
    for i in range(len(positionAlien)):
        rect_alien.append(copy(imageAlien.get_rect()))
        positionAlien[i] = (positionAlien[i][0] + direction, positionAlien[i][1])
        rect_alien[i].move_ip(positionAlien[i])
        if (positionAlien[0][0] <= 0):
            positionAlien[i] = (positionAlien[i][0], positionAlien[i][1] + 10)
            direction = 1
        elif (positionAlien[len(positionAlien) - 1][0] + rect_alien[i].width >= 600):
            positionAlien[i] = (positionAlien[i][0], positionAlien[i][1] + 10)
            direction = -1
    dessiner()
    gererClavierEtSouris()
    for i in range(len(projectile)):
        if (projectile[i][0] <= 0):
            projectile[i] = (-1, -1)
        if projectile[i] != (-1, -1):
            projectile[i] = (projectile[i][0], projectile[i][1] - 5)
        for node in rect_alien:
            if (node.collidepoint(projectile[i]) == True):
                score += 1
                rect_alien.remove(node)
                positionAlien.remove((node.x, node.y))
                projectile[i] = (-1, -1)
    if bombe != (-1, -1):
        bombe = (bombe[0], bombe[1] + 3)
    else:
        x = random.randint(0, 10)
        if (x == 3):
            position = random.choice(positionAlien)
            bombe = (position[0], position[1])
    
    if bonus != (-1, -1):
        bonus = (bonus[0], bonus[1] + 3)
    else:
        x = random.randint(0, 50)
        if (x == 3):
            position = random.choice(positionAlien)
            bonus = (position[0], position[1])
    rect_vausseau = imageVaisseau.get_rect()
    rect_vausseau.move_ip((positionVaisseau[0], positionVaisseau[1]))
    if (bonus[1] >= 600) : bonus = (-1, -1)
    if (bombe[1] >= 600) : bombe = (-1, -1)
    if (rect_vausseau.collidepoint(bonus) == True):
        bonus = (-1, -1)
        reste = 100
    if (rect_vausseau.collidepoint(bombe) == True):
        reste -= 50
        bombe = (-1, -1)
    if (reste == 0 or len(positionAlien) == 0):
        end_game()

pygame.quit()
        