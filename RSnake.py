import pygame
import random
import tkinter as tk
from tkinter import messagebox

global width, rows
width = 500
rows = 20

class cube(object):
    rows = 20
    w = width
    def __init__(self, start, dirnx=1, dirny=0, color=(46, 140, 212)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w//self.rows
        [i, j] = self.pos
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-1, dis-1))


class circle(object):
    def __init__(self, start, color=(46, 140, 212)):
        self.pos = start
        self.color = color

    def draw(self, surface):
        dis = width//rows
        [i, j] = self.pos
        pygame.draw.circle(surface, self.color, (i*dis+dis//2, j*dis+dis//2), dis//2.5)


class Snake(object):
    body = []                                       # body has all the cube objects
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)                       # self.head has the head cube object
        self.body.append(self.head)                 # self.head concatenated to self.body

    def move(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):               # i have the cube no. and c has the cube
            p = c.pos[:]                                # c.pos has the location of the cube
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0 : c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1 : c.pos = (0, c.pos[1])
                elif c.dirny == -1 and c.pos[1] <= 0 : c.pos = (c.pos[0], c.rows-1)
                elif c.dirny == 1 and c.pos[1] >= c.rows-1 : c.pos = (c.pos[0], 0)
                else : c.move(c.dirnx, c.dirny)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface)
            else:
                c.draw(surface)

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}

def randomSnack(item):                     # here item is the snake body cube objects' position
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

def drawgrid(w, r, s):
    sizebtn = w//r
    x = 0
    y = 0
    z = 0
    for x in range(0,w,sizebtn):
        for y in range(z,w,2*sizebtn):
            pygame.draw.rect(s, (31, 41, 55), ([x,y,sizebtn,sizebtn]))
        z = sizebtn if z == 0 else 0

def redrawWindow(surface, snake, snack):
    global width, rows
    surface.fill((38, 52, 69))
    drawgrid(width, rows, surface)
    snake.draw(surface)
    snack.draw(surface)
    pygame.display.update()

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():

    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("RSnake")
    snake = Snake((46, 140, 212), (10, 10))
    snack = circle(randomSnack(snake), color= (227, 64, 50))
    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == 256:
                flag = False
                pygame.quit()

        snake.move()
        if snake.body[0].pos == snack.pos:
            snake.addCube()
            snack = circle(randomSnack(snake), color=(227, 64, 50))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z:z.pos, snake.body[x+1:])):
                print("Score : ", len(snake.body)-1)
                message_box("You lose", "Play again .....")
                snake.reset((10,10))
                break

        # print(snack.pos)
        redrawWindow(win, snake, snack)

main()