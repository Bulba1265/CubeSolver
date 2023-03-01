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


def draw_polygon(color, cords):
    pygame.draw.polygon(screen, color, cords)
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

    pygame.draw.polygon(screen, (50, 50, 203), (faces[0][0], faces[0][1], faces[0][2], faces[0][3]))


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
            draw_polygon(white, white_side)
        elif temp == 1:
            draw_polygon(green, green_side)
        elif temp == 2:
            draw_polygon(red, red_side)
        elif temp == 3:
            draw_polygon(blue, blue_side)
        elif temp == 4:
            draw_polygon(orange, orange_side)
        elif temp == 5:
            draw_polygon(yellow, yellow_side)

    angle += speed
    pygame.display.update()

pygame.quit()