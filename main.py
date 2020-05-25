#! ./venv/bin/python3.7

import numpy as np
import pygame
from time import sleep


nn = 35 # numero de celdas
l = 20  # tamagno de celda
gameStatus = np.zeros((nn, nn))

sizeScreen = (nn * l, nn * l)
liveColor = 250,250,250
bgColor = 10,10,10
borderColor = pygame.Color(100,100,100)

pygame.init()
screen = pygame.display.set_mode(sizeScreen)
pause = False

def getNumberNeighbor(gameStatus):
    # Calcula el numero de vecinos de cada celda, aplicando topologia toroide.
    return (gameStatus[(x-1+nn)%nn,(y-1+nn)%nn] + gameStatus[(x-1+nn)%nn,y] + gameStatus[(x-1)%nn,(y+1)%nn] +\
            gameStatus[x,(y-1+nn)%nn]                       +                 gameStatus[x,(y+1)%nn] +\
            gameStatus[(x+1)%nn,(y-1+nn)%nn] +  gameStatus[(x+1)%nn,y]   + gameStatus[(x+1)%nn,(y+1)%nn])

def polygon(x, y):
    # Cuadrado a partir de coordenadas x, y
    return [(    x * l  ,    y * l)   ,\
            (    x * l  , (y + 1) * l),\
            ((x + 1) * l, (y + 1) * l),\
            ((x + 1) * l,    y * l)   ]

running = True

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
                # Si esta muerta y tiene tres vecinos revive
                if gameStatus[x,y] == 0 and n_neigh == 3:
                    newGameStatus[x,y] = 1
                # Si esta viva muere por soledad o sobrepoblacion.
                elif gameStatus[x,y] == 1 and (n_neigh <2 or n_neigh > 3):
                    newGameStatus[x,y] = 0

            if newGameStatus[x,y] == 1:
                pygame.draw.polygon(screen, liveColor, polygon(x, y), 0)
            else:
                pygame.draw.polygon(screen, borderColor, polygon(x, y), 1)

    gameStatus = np.copy(newGameStatus)
    pygame.display.flip()
    sleep(.1)

print("\nGracias por probar este juego =D\n")
pygame.quit()
