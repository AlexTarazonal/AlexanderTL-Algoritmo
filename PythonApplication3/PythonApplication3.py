import pygame
import random
import sys

ANCHO = 800
ALTO = 800

ANCHO_T = 32
ALTO_T = 32

NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
VERDE  = (0, 150, 0)
ROJO = (200, 0, 0)
AZUL = (0, 200, 200)

FPS = 60


COLUMNAS = 25
FILAS = 25

escenario = [[None] * COLUMNAS for _ in range(FILAS)]

class Casilla:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = 0 if random.randint(0, 4) != 1 else 1
        self.f = 0 #f=g+h
        self.g = 0 
        self.h = 0 
        self.vecinos = []
        self.padre = None

    def addVecinos(self):
        if self.x > 0:
            self.vecinos.append(escenario[self.y][self.x - 1]) 
        if self.x < FILAS - 1:
            self.vecinos.append(escenario[self.y][self.x + 1])
        if self.y > 0:
            self.vecinos.append(escenario[self.y - 1][self.x])
        if self.y < COLUMNAS - 1:
            self.vecinos.append(escenario[self.y + 1][self.x])

    def dibuja(self):
        color = NEGRO if self.tipo == 1 else GRIS
        pygame.draw.rect(screen, color, (self.x * ANCHO_T, self.y * ALTO_T, ANCHO_T, ALTO_T))

    def dibujaOS(self):
        pygame.draw.rect(screen, VERDE, (self.x * ANCHO_T, self.y * ALTO_T, ANCHO_T, ALTO_T))

    def dibujaCS(self):
        pygame.draw.rect(screen, ROJO, (self.x * ANCHO_T, self.y * ALTO_T, ANCHO_T, ALTO_T))

    def dibujaCamino(self):
        pygame.draw.rect(screen, AZUL, (self.x * ANCHO_T, self.y * ALTO_T, ANCHO_T, ALTO_T))


# Crear el escenario y añadir vecinos
for i in range(FILAS):
    for j in range(COLUMNAS):
        escenario[i][j] = Casilla(j, i)

for i in range(FILAS):
    for j in range(COLUMNAS):
        escenario[i][j].addVecinos()


principio = escenario[0][0]
fin = escenario[COLUMNAS - 1][FILAS - 1]


openSet = [principio]

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Algoritmo A estrella")

clock = pygame.time.Clock()


def algoritmo():
    global terminado
    if not terminado:
        if openSet:
            ganador = 0
            for i in range(len(openSet)):
                if openSet[i].f < openSet[ganador].f:
                    ganador = i

            actual = openSet[ganador]

            if actual == fin:
                temporal = actual
                camino.append(temporal)
                while temporal.padre is not None:
                    temporal = temporal.padre
                    camino.append(temporal)
                print('Camino encontrado')
                terminado = True
            else:
                openSet.remove(actual)
                closedSet.append(actual)
                vecinos = actual.vecinos
                for vecino in vecinos:
                    if vecino not in closedSet and vecino.tipo != 1:
                        tempG = actual.g + 1
                        if vecino in openSet:
                            if tempG < vecino.g:
                                vecino.g = tempG
                        else:
                            vecino.g = tempG
                            openSet.append(vecino)
                        vecino.h = heuristica(vecino, fin)
                        vecino.f = vecino.g + vecino.h
                        vecino.padre = actual
        else:
            print('No hay camino posible')
            terminado = True


def heuristica(a, b):
    x = abs(a.x - b.x)  
    y = abs(a.y - b.y)
    return x + y


terminado = False
camino = []
closedSet = []
while not terminado:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminado = True

    algoritmo()

    screen.fill((255, 255, 255))

    for i in range(FILAS):
        for j in range(COLUMNAS):
            escenario[i][j].dibuja()

    for casilla in openSet:
        casilla.dibujaOS()

    for casilla in closedSet:
        casilla.dibujaCS()

    for casilla in camino:
        casilla.dibujaCamino()

    pygame.display.flip()
    clock.tick(FPS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  
            sys.exit()     
        elif event.type == pygame.KEYDOWN:
            pygame.quit()  
            sys.exit()     
