#! ./venv/bin/python3.7

import numpy as np
import pygame
from time import sleep


nn = 35 # number of cel
maxSizeCel = 20 # max size of cel, en px

gameStatus = np.zeros((nn, nn))

liveColor = 250,250,250
bgColor = 10,10,10
borderColor = pygame.Color(100,100,100)

pygame.init()
hwWidth  = pygame.display.Info().current_w
hwHeigth = pygame.display.Info().current_h
# sets the width of a cell depending on the amount to be displayed.
l = int(hwHeigth / nn) if int(hwHeigth / nn) < maxSizeCel else maxSizeCel

# calculates the width of the screen based on the width of each cell.
screenHeigth = (l * nn) if (l * nn) < hwHeigth else hwHeigth
# for now it shows only one square of cells. Then it will show information on the right.
sizeScreen = (screenHeigth, screenHeigth)
screen = pygame.display.set_mode(sizeScreen)

def getNumberNeighbor(gameStatus):
    # Calcula el numero de vecinos de cada celda, aplicando topologia toroide.
    return (gameStatus[(x-1+nn)%nn,(y-1+nn)%nn] + gameStatus[(x-1+nn)%nn,y] + gameStatus[(x-1)%nn,(y+1)%nn] +\
            gameStatus[x,(y-1+nn)%nn]                       +                 gameStatus[x,(y+1)%nn] +\
            gameStatus[(x+1)%nn,(y-1+nn)%nn] +  gameStatus[(x+1)%nn,y]   + gameStatus[(x+1)%nn,(y+1)%nn])

def polygon(x, y):
    # Square from coordinates x, y
    return [(    x * l  ,    y * l)   ,\
            (    x * l  , (y + 1) * l),\
            ((x + 1) * l, (y + 1) * l),\
            ((x + 1) * l,    y * l)   ]

running = True
pause = True

while running:
    newGameStatus = np.copy(gameStatus)

    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
            pause = not pause

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            x, y = pygame.mouse.get_pos()
            i, j = int(np.floor(x / l)), int(np.floor(y / l))
            newGameStatus[i,j] = not mouseClick[2]


    screen.fill(bgColor)

    for y in range(0, nn):
        for x in range(0, nn):

            if not pause:
                n_neigh = getNumberNeighbor(gameStatus)
                # if is dead and have three neighbors alive again.
                if gameStatus[x,y] == 0 and n_neigh == 3:
                    newGameStatus[x,y] = 1
                # if is alive, die for loneliness or overpopulation.
                elif gameStatus[x,y] == 1 and (n_neigh <2 or n_neigh > 3):
                    newGameStatus[x,y] = 0

            if newGameStatus[x,y] == 1:
                pygame.draw.polygon(screen, liveColor, polygon(x, y), 0)
            else:
                pygame.draw.polygon(screen, borderColor, polygon(x, y), 1)

    gameStatus = np.copy(newGameStatus)
    pygame.display.flip()
    sleep(.1)

# print("\nGracias por probar este juego =D\n")
# print("\nThanks for trying this game =D\n")
# print("\nMerci d'avoir essayé ce jeu =D\n")
# print("\nDankon pro provi ĉi tiun ludon =D\n")
# print("\nDeo gratias, quia hoc ludum conatur =D\n")
pygame.quit()
