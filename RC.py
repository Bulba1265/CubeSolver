import pygame
from pygame import K_q, K_w, K_a, K_s, K_z, K_x
import os
import math

os.environ["SDL_VIDEO_CENTERED"]='1'
black, white, blue = (20, 20, 20), (255, 255, 255), (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
width, height = 800, 800

pygame.init()
pygame.display.set_caption("3D cube Projection")
screen = pygame.display.set_mode((width, height))
gui_font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
fps = 60

angle = 0
angles = [0, 0, 0]
cube_position = [width//2, height//2]
scale = 500
speed = 0.01
points = [n for n in range(8)]
cam = (0, 0, 50)

points[0] = [[-3], [-3], [3]]
points[1] = [[3], [-3], [3]]
points[2] = [[3], [3], [3]]
points[3] = [[-3], [3], [3]]
points[4] = [[-3], [-3], [-3]]
points[5] = [[3], [-3], [-3]]
points[6] = [[3], [3], [-3]]
points[7] = [[-3], [3], [-3]]

params = {
        K_q: (0, -0.05),
        K_w: (0, 0.05),
        K_a: (1, -0.05),
        K_s: (1, 0.05),
        K_z: (2, -0.05),
        K_x: (2, 0.05),
    }

projected_points = [j for j in range(len(points))]
rotated = [0 for _ in range(len(points))]

front = ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']
right = ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']
left = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']
back = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
up = ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
down = ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']


class Button:
    def __init__(self, text, w, h, pos):
        self.top_rect = pygame.Rect(pos, (w, h))
        self.top_color = '#475F77'

        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self.pressed = False

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=10)
        screen.blit(self.text_surf, self.text_rect)
        return self.check_click()

    def check_click(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                self.pressed = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False
        return action


def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum = 0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix

    else:
        print("columns of the first matrix must be equal to the rows of the second matrix")
        return None


def turn(side0, side1, side2, side3, side4, index1, index2, index3, index4, direction):
    if not direction:
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
        if index1 == -1:
            index1 -= 1
        if index2 == -1:
            index2 -= 1
        if index3 == -1:
            index3 -= 1
        if index4 == -1:
            index4 -= 1


def F(direction=True):
    turn(front, up, right, down, left, 6, 0, 2, 4, direction)


def R(direction=True):
    turn(right, up, back, down, front, 4, 0, 4, 4,  direction)


def L(direction=True):
    turn(left, up, front, down, back, 0, 0, 0, 4, direction)


def B(direction=True):
    turn(back, up, left, down, right, 2, 0, 6, 4, direction)


def U(direction=True):
    turn(up, back, right, front, left, 2, 2, 2, 2, direction)


def D(direction=True):
    turn(down, front, right, back, left, 6, 6, 6, 6, direction)


def y_rotate_cube():
    global front, right, left, back, up, down
    temp = up.pop(7)
    up.insert(0, temp)
    temp = up.pop(7)
    up.insert(0, temp)

    temp = down.pop(0)
    down.insert(7, temp)
    temp = down.pop(0)
    down.insert(7, temp)

    temp = front
    front = right
    right = back
    back = left
    left = temp


def yp_rotate_cube():
    global front, right, left, back, up, down
    temp = up.pop(0)
    up.insert(7, temp)
    temp = up.pop(0)
    up.insert(7, temp)

    temp = down.pop(7)
    down.insert(0, temp)
    temp = down.pop(7)
    down.insert(0, temp)

    temp = front
    front = left
    left = back
    back = right
    right = temp


def x_rotate_cube():
    global front, right, left, back, up, down
    temp = right.pop(7)
    right.insert(0, temp)
    temp = right.pop(7)
    right.insert(0, temp)

    temp = left.pop(0)
    left.insert(7, temp)
    temp = left.pop(0)
    left.insert(7, temp)

    temp = front
    front = down
    down = back
    back = up
    up = temp


def xp_rotate_cube():
    pass


def connect_point(i, j, k):
    a = k[i]
    b = k[j]
    pygame.draw.line(screen, black, (a[0], a[1]), (b[0], b[1]), 2)


def get_distance_3d(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)


def sort_tuples(tab):
    s = True
    while s:
        s = False
        for i in range(len(tab)-1):
            if tab[i][1] < tab[i+1][1]:
                tab[i], tab[i+1] = tab[i+1], tab[i]
                s = True
    return tab


def draw_polygon(color, cords, colors):
    # pygame.draw.polygon(screen, color, cords)
    corners = [[0, 0] for _ in range(16)]
    corners[0] = [cords[0][0], cords[0][1]]
    corners[3] = [cords[1][0], cords[1][1]]
    corners[12] = [cords[3][0], cords[3][1]]
    corners[15] = [cords[2][0], cords[2][1]]

    dx = (cords[0][0] - cords[3][0]) // 3
    dy = (cords[0][1] - cords[3][1]) // 3
    x = cords[0][0] - dx
    y = cords[0][1] - dy
    corners[4] = [x, y]
    x -= dx
    y -= dy
    corners[8] = [x, y]

    dx = (cords[1][0] - cords[2][0]) // 3
    dy = (cords[1][1] - cords[2][1]) // 3
    x = cords[1][0] - dx
    y = cords[1][1] - dy
    corners[7] = [x, y]
    x -= dx
    y -= dy
    corners[11] = [x, y]

    for i in range(1, 14, 4):
        dx = (corners[i-1][0] - corners[i+2][0])//3
        dy = (corners[i-1][1] - corners[i+2][1])//3
        x = corners[i-1][0] - dx
        y = corners[i-1][1] - dy
        corners[i] = [x, y]
        x -= dx
        y -= dy
        corners[i+1] = [x, y]

    faces = []
    # it = 0
    # for i in range(3):
    #     for j in range(3):
    #         faces += [[corners[it], corners[it+1], corners[it+5], corners[it+4]]]
    #         it += 1
    #     it += 1
    faces += [[corners[0], corners[1], corners[5], corners[4]]]
    faces += [[corners[1], corners[2], corners[6], corners[5]]]
    faces += [[corners[2], corners[3], corners[7], corners[6]]]
    faces += [[corners[6], corners[7], corners[11], corners[10]]]
    faces += [[corners[10], corners[11], corners[15], corners[14]]]
    faces += [[corners[9], corners[10], corners[14], corners[13]]]
    faces += [[corners[8], corners[9], corners[13], corners[12]]]
    faces += [[corners[4], corners[5], corners[9], corners[8]]]
    faces += [[corners[5], corners[6], corners[10], corners[9]]]

    for i in range(9):
        c = (0, 0, 0)
        if colors[i] == 'w':
            c = white
        elif colors[i] == 'g':
            c = green
        elif colors[i] == 'r':
            c = red
        elif colors[i] == 'b':
            c = blue
        elif colors[i] == 'o':
            c = orange
        elif colors[i] == 'y':
            c = yellow

        pygame.draw.polygon(screen, c, (faces[i][0], faces[i][1], faces[i][2], faces[i][3]))

    pygame.draw.line(screen, black, (corners[8][0], corners[8][1]), (corners[11][0], corners[11][1]), 3)
    pygame.draw.line(screen, black, (corners[4][0], corners[4][1]), (corners[7][0], corners[7][1]), 3)
    pygame.draw.line(screen, black, (corners[1][0], corners[1][1]), (corners[13][0], corners[13][1]), 3)
    pygame.draw.line(screen, black, (corners[2][0], corners[2][1]), (corners[14][0], corners[14][1]), 3)

    pygame.draw.line(screen, black, (corners[0][0], corners[0][1]), (corners[3][0], corners[3][1]), 3)
    pygame.draw.line(screen, black, (corners[3][0], corners[3][1]), (corners[15][0], corners[15][1]), 3)
    pygame.draw.line(screen, black, (corners[15][0], corners[15][1]), (corners[12][0], corners[12][1]), 3)
    pygame.draw.line(screen, black, (corners[12][0], corners[12][1]), (corners[0][0], corners[0][1]), 3)


def rotate_cube():
    index = 0
    rotation_x = [[1, 0, 0],
                  [0, math.cos(angles[0]), -math.sin(angles[0])],
                  [0, math.sin(angles[0]), math.cos(angles[0])]]

    rotation_y = [[math.cos(angles[1]), 0, -math.sin(angles[1])],
                  [0, 1, 0],
                  [math.sin(angles[1]), 0, math.cos(angles[1])]]

    rotation_z = [[math.cos(angles[2]), -math.sin(angles[2]), 0],
                  [math.sin(angles[2]), math.cos(angles[2]), 0],
                  [0, 0, 1]]

    for point in points:
        rotated_2d = matrix_multiplication(rotation_y, point)
        rotated_2d = matrix_multiplication(rotation_x, rotated_2d)
        rotated_2d = matrix_multiplication(rotation_z, rotated_2d)
        distance = 15
        z = 1 / (distance - rotated_2d[2][0])
        projection_matrix = [[z, 0, 0],
                             [0, z, 0]]
        projected_2d = matrix_multiplication(projection_matrix, rotated_2d)

        x = int(projected_2d[0][0] * scale) + cube_position[0]
        y = int(projected_2d[1][0] * scale) + cube_position[1]
        projected_points[index] = [x, y]
        rotated[index] = [rotated_2d[0][0], rotated_2d[1][0], rotated_2d[2][0]]
        #pygame.draw.circle(screen, blue, (x, y), 10)
        index += 1


def keys_handler(keys):
    for key in params:
        if keys[key]:
            angles[params[key][0]] += params[key][1]
    rotate_cube()


R_move = Button('R', 40, 40, (10, 10))
Rp_move = Button('R\'', 40, 40, (60, 10))
L_move = Button('L', 40, 40, (10, 60))
Lp_move = Button('L\'', 40, 40, (60, 60))
U_move = Button('U', 40, 40, (10, 110))
Up_move = Button('U\'', 40, 40, (60, 110))
D_move = Button('D', 40, 40, (10, 160))
Dp_move = Button('D\'', 40, 40, (60, 160))
F_move = Button('F', 40, 40, (10, 210))
Fp_move = Button('F\'', 40, 40, (60, 210))
B_move = Button('B', 40, 40, (10, 260))
Bp_move = Button('B\'', 40, 40, (60, 260))
y_rotate = Button('y', 40, 40, (10, 310))
yp_rotate = Button('y\'', 40, 40, (60, 310))
x_rotate = Button('x', 40, 40, (10, 360))
xp_rotate = Button('x\'', 40, 40, (60, 360))

run = True
while run:
    clock.tick(fps)
    screen.fill((230, 230, 230))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys_handler(pygame.key.get_pressed())

    #draw edges
    # for m in range(4):
    #     connect_point(m, (m+1)%4, projected_points)
    #     connect_point(m+4, (m+1)%4 + 4, projected_points)
    #     connect_point(m, m+4, projected_points)
    if R_move.draw():
        R()
    if Rp_move.draw():
        R(False)
    if L_move.draw():
        L()
    if Lp_move.draw():
        L(False)
    if U_move.draw():
        U()
    if Up_move.draw():
        U(False)
    if D_move.draw():
        D()
    if Dp_move.draw():
        D(False)
    if F_move.draw():
        F()
    if Fp_move.draw():
        F(False)
    if B_move.draw():
        B()
    if Bp_move.draw():
        B(False)
    if y_rotate.draw():
        y_rotate_cube()
    if yp_rotate.draw():
        yp_rotate_cube()
    if x_rotate.draw():
        x_rotate_cube()
    if xp_rotate.draw():
        xp_rotate_cube()

    middles = [[i, (0, 0, 0)] for i in range(6)]
    middles[0][1] = ((rotated[1][0] + rotated[4][0]) / 2, (rotated[1][1] + rotated[4][1]) / 2, (rotated[1][2] + rotated[4][2]) / 2)
    middles[1][1] = ((rotated[1][0] + rotated[3][0]) / 2, (rotated[1][1] + rotated[3][1]) / 2, (rotated[1][2] + rotated[3][2]) / 2)
    middles[2][1] = ((rotated[1][0] + rotated[6][0]) / 2, (rotated[1][1] + rotated[6][1]) / 2, (rotated[1][2] + rotated[6][2]) / 2)
    middles[3][1] = ((rotated[4][0] + rotated[6][0]) / 2, (rotated[4][1] + rotated[6][1]) / 2, (rotated[4][2] + rotated[6][2]) / 2)
    middles[4][1] = ((rotated[4][0] + rotated[3][0]) / 2, (rotated[4][1] + rotated[3][1]) / 2, (rotated[4][2] + rotated[3][2]) / 2)
    middles[5][1] = ((rotated[2][0] + rotated[7][0]) / 2, (rotated[2][1] + rotated[7][1]) / 2, (rotated[2][2] + rotated[7][2]) / 2)

    distances = [[i, 0] for i in range(6)]
    for i in range(6):
        distances[i][1] = get_distance_3d(cam, middles[i][1])

    yellow_side = [(projected_points[3][0], projected_points[3][1]),
                   (projected_points[2][0], projected_points[2][1]),
                   (projected_points[6][0], projected_points[6][1]),
                   (projected_points[7][0], projected_points[7][1])]
    white_side = [(projected_points[4][0], projected_points[4][1]),
                  (projected_points[5][0], projected_points[5][1]),
                  (projected_points[1][0], projected_points[1][1]),
                  (projected_points[0][0], projected_points[0][1])]
    green_side = [(projected_points[0][0], projected_points[0][1]),
                  (projected_points[1][0], projected_points[1][1]),
                  (projected_points[2][0], projected_points[2][1]),
                  (projected_points[3][0], projected_points[3][1])]
    blue_side = [(projected_points[5][0], projected_points[5][1]),
                 (projected_points[4][0], projected_points[4][1]),
                 (projected_points[7][0], projected_points[7][1]),
                 (projected_points[6][0], projected_points[6][1])]
    red_side = [(projected_points[1][0], projected_points[1][1]),
                (projected_points[5][0], projected_points[5][1]),
                (projected_points[6][0], projected_points[6][1]),
                (projected_points[2][0], projected_points[2][1])]
    orange_side = [(projected_points[4][0], projected_points[4][1]),
                   (projected_points[0][0], projected_points[0][1]),
                   (projected_points[3][0], projected_points[3][1]),
                   (projected_points[7][0], projected_points[7][1])]
    distances = sort_tuples(distances)
    for i in range(6):
        temp = distances[i][0]
        if temp == 0:
            draw_polygon(white, white_side, up)
        elif temp == 1:
            draw_polygon(green, green_side, front)
        elif temp == 2:
            draw_polygon(red, red_side, right)
        elif temp == 3:
            draw_polygon(blue, blue_side, back)
        elif temp == 4:
            draw_polygon(orange, orange_side, left)
        elif temp == 5:
            draw_polygon(yellow, yellow_side, down)

    angle += speed
    pygame.display.update()

pygame.quit()