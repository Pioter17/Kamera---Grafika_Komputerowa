import sys

import pygame
import numpy as np



pygame.init()
win = pygame.display.set_mode((700, 700))
win.fill((255, 255, 255))
pygame.display.set_caption("Draw Line Function in Pygame")
#            #       1               2               3           4               5                   6               7               8
Rectangle1 = [[100, 100, 0], [200, 100, 0], [100, 200, 0], [200, 200, 0], [100, 100, 100], [200, 100, 100], [100, 200, 100], [200, 200, 100]]
Rectangle2 = [[-100, 100, 0], [-200, 100, 0], [-100, 200, 0], [-200, 200, 0], [-100, 100, 100], [-200, 100, 100], [-100, 200, 100], [-200, 200, 100]]
Rectangle3 = [[-100, -100, 0], [-200, -100, 0], [-100, -200, 0], [-200, -200, 0], [-100, -100, 100], [-200, -100, 100], [-100, -200, 100], [-200, -200, 100]]
Rectangle4 = [[100, -100, 0], [200, -100, 0], [100, -200, 0], [200, -200, 0], [100, -100, 100], [200, -100, 100], [100, -200, 100], [200, -200, 100]]
Rectangle5 = [[100, 100, 200], [200, 100, 200], [100, 200, 200], [200, 200, 200], [100, 100, 300], [200, 100, 300], [100, 200, 300], [200, 200, 300]]
Rectangle6 = [[-100, 100, 200], [-200, 100, 200], [-100, 200, 200], [-200, 200, 200], [-100, 100, 300], [-200, 100, 300], [-100, 200, 300], [-200, 200, 300]]
Rectangle7 = [[-100, -100, 200], [-200, -100, 200], [-100, -200, 200], [-200, -200, 200], [-100, -100, 300], [-200, -100, 300], [-100, -200, 300], [-200, -200, 300]]
Rectangle8 = [[100, -100, 200], [200, -100, 200], [100, -200, 200], [200, -200, 200], [100, -100, 300], [200, -100, 300], [100, -200, 300], [200, -200, 300]]

Lanes = [[1, 2], [2, 4], [1, 3], [3, 4], [1, 5], [2, 6], [3, 7], [4, 8], [5, 6], [5, 7], [6, 8], [7, 8]]
Cubes = [Rectangle1, Rectangle2, Rectangle3, Rectangle4, Rectangle5, Rectangle6, Rectangle7, Rectangle8]

pygame.display.flip()
d = 200
step = 20

Mrox = [[1, 0, 0, 0],
        [0, np.cos(np.pi/12), -np.sin(np.pi/12), 0],
        [0, np.sin(np.pi/12), np.cos(np.pi/12), 0],
        [0, 0, 0, 1]]

Mroy = [[np.cos(np.pi/12), 0, np.sin(np.pi/12), 0],
        [0, 1, 0, 0],
        [-np.sin(np.pi/12), 0, np.cos(np.pi/12), 0],
        [0, 0, 0, 1]]

Mroz = [[np.cos(np.pi/12), -np.sin(np.pi/12), 0, 0],
        [np.sin(np.pi/12), np.cos(np.pi/12), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]

Msk = [[1.5, 0, 0, 0],
       [0, 1.5, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]]

def find_new_points(p1, p2):
    (x1, y1, z1) = p1
    (x2, y2, z2) = p2
    u = [x2-x1, y2-y1, z2-z1]
    new_x = (-d - z1/u[2])*(u[0]/x1)
    new_y = (-d - z1/u[2])*(u[1]/y1)
    new_z = (-d + step)
    return (new_x, new_y, new_z), (x2, y2, z2)


def draw_all():
    for cube in Cubes:
        for i in range(len(Lanes)):
            lane = Lanes[i]
            rect = cube[lane[0]-1]
            z1 = rect[2]
            rect2 = cube[lane[1]-1]
            z2 = rect2[2]
            if z1 <= -d and z2 <= -d:
                continue
            elif z1 <= -d:
                if rect[0] == 0 or rect[1] == 0:
                    continue
                ((x1, y1, z1), (x2, y2, z2)) = find_new_points(rect, rect2)
            elif z2 <= -d:
                if rect2[0] == 0 or rect2[1] == 0:
                    continue
                ((x2, y2, z2), (x1, y1, z1)) = find_new_points(rect2, rect)
            x1 = 350 + rect[0] * d / (z1 + d)
            y1 = 350 - rect[1] * d / (z1 + d)
            x2 = 350 + rect2[0] * d / (z2 + d)
            y2 = 350 - rect2[1] * d / (z2 + d)
            pygame.draw.line(win, (255,0,0), (x1, y1), (x2, y2), 2)
            pygame.display.flip()


def go_horizontally(is_left):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            if is_left:
                x = point[0] + step
            else:
                x = point[0] - step
            y = point[1]
            z = point[2]
            new_cube.append([x, y, z])
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    draw_all()


def go_vertically(is_up):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            if is_up:
                y = point[1] - step
            else:
                y = point[1] + step
            x = point[0]
            z = point[2]
            new_cube.append([x, y, z])
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    draw_all()


def go(forward):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            if forward:
                z = point[2] - step
            else:
                z = point[2] + step
            x = point[0]
            y = point[1]
            new_cube.append([x, y, z])
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    draw_all()


def rotate_horizontally(up):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            point.append(1)
            if up:
                new_point = np.matmul(Mrox, point)
                new_point = new_point.tolist()
                new_point.pop()
            else:
                matrix = np.array(Mrox)
                inverse_matrix = np.linalg.inv(matrix)
                new_point = np.matmul(inverse_matrix, point)
                new_point = new_point.tolist()
                new_point.pop()
            new_cube.append(new_point)
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    draw_all()


def rotate_vertically(left):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            point.append(1)
            if left:
                new_point = np.matmul(Mroy, point)
                new_point = new_point.tolist()
                new_point.pop()
            else:
                matrix = np.array(Mroy)
                inverse_matrix = np.linalg.inv(matrix)
                new_point = np.matmul(inverse_matrix, point)
                new_point = new_point.tolist()
                new_point.pop()
            new_cube.append(new_point)
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    draw_all()


def rotate(left):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            point.append(1)
            if left:
                new_point = np.matmul(Mroz, point)
                new_point = new_point.tolist()
                new_point.pop()
            else:
                matrix = np.array(Mroz)
                inverse_matrix = np.linalg.inv(matrix)
                new_point = np.matmul(inverse_matrix, point)
                new_point = new_point.tolist()
                new_point.pop()
            new_cube.append(new_point)
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    draw_all()

def zoom(more):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            z = point[2]
            point[2] = 1
            point.append(1)
            if more:
                new_point = np.matmul(Msk, point)
                new_point = new_point.tolist()
                new_point.pop()
                new_point[2] = z
            else:
                matrix = np.array(Msk)
                inverse_matrix = np.linalg.inv(matrix)
                new_point = np.matmul(inverse_matrix, point)
                new_point = new_point.tolist()
                new_point.pop()
                new_point[2] = z
            new_cube.append(new_point)
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    draw_all()


while True:
    draw_all()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                case pygame.K_a:
                    go_horizontally(True)
                case pygame.K_d:
                    go_horizontally(False)
                case pygame.K_w:
                    go_vertically(True)
                case pygame.K_s:
                    go_vertically(False)
                case pygame.K_r:
                    go(True)
                case pygame.K_f:
                    go(False)
                case pygame.K_UP:
                    rotate_horizontally(True)
                case pygame.K_DOWN:
                    rotate_horizontally(False)
                case pygame.K_LEFT:
                    rotate_vertically(True)
                case pygame.K_RIGHT:
                    rotate_vertically(False)
                case pygame.K_q:
                    rotate(True)
                case pygame.K_e:
                    rotate(False)
                case pygame.K_z:
                    zoom(True)
                case pygame.K_x:
                    zoom(False)
