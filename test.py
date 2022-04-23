import pygame
from pygame import *
from copy import copy
import math

pygame.init()
continu = True
fenetre = pygame.display.set_mode((600,600))
pygame.display.set_caption("Robert & Celestine")
robert = pygame.Rect(0, 0, 50, 50)
circle_var = (1200, 0, 5)
circle_tab = []
circle_advence = []
celestine = pygame.Rect(300, 300, 50, 50)
clock = pygame.time.Clock()
press = True

def deplacement(robert):
    global time, fenetre, circle_var, press, circle_tab, circle_advence, celestine
    y_triange = celestine.y - robert.y
    x_triange = celestine.x - robert.x
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT] == True and (robert.x + robert.width) <= 600 :
        robert = robert.move(1, 0)
    if pressed[pygame.K_LEFT] == True and robert.x >= 0:
        robert = robert.move(-1, 0)
    if pressed[pygame.K_UP] == True and robert.y >= 0:
        robert = robert.move(0, -1)
    if pressed[pygame.K_DOWN] == True and (robert.y + robert.height) <= 600:
        robert = robert.move(0, 1)
    if (pressed[pygame.K_SPACE] == True and press == True):
        circle_var = (robert.x + (robert.width), robert.y + (robert.height / 2), circle_var[2])
        circle_tab.append(copy(circle_var))
        if (robert.x > celestine.x):
            circle_advence.append((-(math.cos(math.atan(y_triange / x_triange))), -(math.sin(math.atan(y_triange / x_triange)))))
        else:
            circle_advence.append(((math.cos(math.atan(y_triange / x_triange))), (math.sin(math.atan(y_triange / x_triange)))))
        press = False
    elif (pressed[pygame.K_SPACE] == False):
        press = True
    return robert

time = 0
pleure = False
while(continu == True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continu = False
    fenetre.fill((0, 0, 0))
    pygame.draw.rect(fenetre, (255, 0, 0), celestine)
    pygame.draw.rect(fenetre, (0, 100, 0), robert)
    for i in range(len(circle_tab)):
        circle_tab[i] = (circle_tab[i][0] + circle_advence[i][0] , circle_tab[i][1] + circle_advence[i][1], circle_tab[i][2])
        pygame.draw.circle(fenetre,(255, 255, 255) , (circle_tab[i][0], circle_tab[i][1]), circle_tab[i][2])

    robert = deplacement(robert)
    if (robert.colliderect(celestine) == True):
        continu = False
    for circle in circle_tab:
        if (celestine.collidepoint(circle[0], circle[1]) == True):
            pleure = True
            press = True
            circle_tab.remove(circle)
            break
            
    if (pleure == True and celestine.x <= 700):
        celestine = celestine.move(5, 0)
    clock.tick(60)
    pygame.display.flip()


