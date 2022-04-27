##
## EPITECH PROJECT, 2022
## guerre_des_etoiles
## File description:
## morpion
##
import pygame
from pygame import *
import math
list1 = ""
list2 = ""
list3 = ""
activate = False
appui = False
caract = 'O'
pygame.init()

def detect_win(list1, list2, list3, caract):
    if (list1[0] == caract and list2[1] == caract and list3[2] == caract):
        print("il semblerais que " + str(caract) + " a gagner")
        return True
    if (list1[2] == caract and list2[1] == caract and list3[0] == caract):
        print("il semblerais que " + str(caract) + " a gagner")
        return True
    for i in range(3):
        if (list1[i] == caract and list2[i] == caract and list3[i] == caract):
            print("il semblerais que " + str(caract) + " a gagner")
            return True
    return False

def display(rect_tab, fenetre, score_tab):
    for i in range(len(score_tab)):
        pygame.draw.rect(fenetre, (255, 255, 255), rect_tab[i])
        fenetre.blit(score_tab[i], (rect_tab[i].x, rect_tab[i].y))

def fill_rect_tab(nb, left = 0, right = 0, height = 190, width = 190):
    rect = pygame.Rect(left, right, height, width)
    tab = [rect]
    for i in range(nb):
        for i in range(len(tab), nb):
            rect = pygame.Rect(tab[i - 1].left + 200, tab[i - 1].top, tab[i - 1].height, tab[i - 1].width)
            tab.append(rect)
        rect = pygame.Rect(0, tab[len(tab) -1].top + 200, tab[len(tab) - 1].height, tab[len(tab) - 1].width)
        nb = nb + 3
        tab.append(rect)
    return tab

def gestion_game(score_tab, rect_tab, list_tab, font):
    global appui, caract
    if (pygame.mouse.get_pressed()[0] == 1 and appui == False):
        appui = True
        for i in range(len(rect_tab)):
            if (rect_tab[i].collidepoint((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) == True 
            and list_tab[i] == ' '):
                score_tab[i] = font.render(str(caract), False, (255, 0, 0))
                list_tab[i] = caract
        if (caract == 'O'): 
            caract = 'X' 
        else: 
            caract = 'O'
    elif pygame.mouse.get_pressed()[0] == 0:
        appui = False
    return score_tab, list_tab

def detect_full(list_tab):
    count = 0
    for node in list_tab:
        if node == ' ':
            break
        count += 1
    if (count == len(list_tab)):
        print("il y a match nul")
        return True
    return False

def game_loop(fenetre):
    global activate
    rect_tab = fill_rect_tab(3)
    font = pygame.font.SysFont("police", 250)
    score_surface = font.render(str(""), False, (255, 0, 0))
    score_tab = []
    gestion_game_list = []
    list_tab = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    for i in range(10):
        score_tab.append(score_surface)
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        gestion_game_list = gestion_game(score_tab, rect_tab, list_tab, font)
        score_tab = gestion_game_list[0]
        list_tab = gestion_game_list[1]
        display(rect_tab, fenetre, score_tab)
        if (detect_win(list_tab[0:3], list_tab[3:6], list_tab[6:10], caract) == True): break
        if (detect_full(list_tab) == True) : break
        pygame.display.flip()
    
def game():
    fenetre = pygame.display.set_mode((600, 600))
    game_loop(fenetre)

game()
pygame.quit()
