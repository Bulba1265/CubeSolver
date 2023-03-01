import random
from tkinter import *


def printCube():
    printLine(up, 1, 3, "\n")
    printLine(up, 2, 3, "\n")
    printLine(up, 3, 3, "\n")
    printLine(left, 1, 0, " ")
    printLine(front, 1, 0, " ")
    printLine(right, 1, 0, " ")
    printLine(back, 1, 0, "\n")
    printLine(left, 2, 0, " ")
    printLine(front, 2, 0, " ")
    printLine(right, 2, 0, " ")
    printLine(back, 2, 0, "\n")
    printLine(left, 3, 0, " ")
    printLine(front, 3, 0, " ")
    printLine(right, 3, 0, " ")
    printLine(back, 3, 0, "\n")
    printLine(down, 1, 3, "\n")
    printLine(down, 2, 3, "\n")
    printLine(down, 3, 3, "\n")
    print()


def printLine(side, numberOfLine, a, ending):
    if (numberOfLine == 1):
        print(" " * a * 2 + side[0] + " " + side[1] + " " + side[2], end=ending)
    if (numberOfLine == 2):
        print(" " * a * 2 + side[7] + "   " + side[3], end=ending)
    if (numberOfLine == 3):
        print(" " * a * 2 + side[6] + " " + side[5] + " " + side[4], end=ending)


def turn(side0, side1, side2, side3, side4, index1, index2, index3, index4, direction):
    if direction == False:
        side2, side4 = side4, side2
        index2, index4 = index4, index2
        temp = side0.pop(0)
        side0.insert(7, temp)
        temp = side0.pop(0)
        side0.insert(7, temp)
    else:
        temp = side0.pop(7)
        side0.insert(0, temp)
        temp = side0.pop(7)
        side0.insert(0, temp)

    for i in range(1, 4):
        temp = side1[index1]
        side1[index1] = side4[index4]
        side4[index4] = side3[index3]
        side3[index3] = side2[index2]
        side2[index2] = temp
        index1 -= 1
        index2 -= 1
        index3 -= 1
        index4 -= 1

def F(direction = True):
    turn(front, up, right, down, left, 6, 0, 2, 4, direction)

def R(direction = True):
    turn(right, up, back, down, front, 4, 0, 4, 4,  direction)

def L(direction = True):
    turn(left, up, front, down, back, 0, 0, 0, 4, direction)

def B(direction = True):
    turn(back, up, left, down, right, 2, 0, 6, 4, direction)

def U(direction = True):
    turn(up, back, right, front, left, 2, 2, 2, 2, direction)

def D(direction = True):
    turn(down, front, right, back, left, 6, 6, 6, 6, direction)


front = ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']
right = ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']
left = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']
back = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
up = ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
down = ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']

printCube()

#skjd

for i in range(0, 20):
    a = random.randint(1, 6)
    b = random.randint(0, 1)
    direction = True
    if b == 1:
        direction = False

    if a == 1:
        F(direction)
    elif a == 2:
        R(direction)
    elif a == 3:
        L(direction)
    elif a == 4:
        B(direction)
    elif a == 5:
        U(direction)
    elif a == 6:
        D(direction)

printCube()
x = 0


win = Tk()
win.geometry("400x400")
c = Canvas(win, width = 400, height = 400)
c.pack()

oval = c.create_oval(0, 0, 100, 100, fill="#FF0000")
c.move(oval, 200, 200)
win.mainloop()


# while x != '0':
#     x = input()
#     if x == 'r':
#         R()
#     elif x == "rp":
#         R(False)
#     elif x == 'l':
#         L()
#     elif x == "lp":
#         L(False)
#     elif x == 'u':
#         U()
#     elif x == "up":
#         U(False)
#     elif x == 'd':
#         D()
#     elif x == "dp":
#         D(False)
#     elif x == 'f':
#         F()
#     elif x == "fp":
#         F(False)
#     elif x == 'b':
#         B()
#     elif x == "bp":
#         B(False)
#
#     printCube()


