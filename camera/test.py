import numpy as np
import pygame
import sys

pygame.init()
win = pygame.display.set_mode((700, 700))
win.fill((255, 255, 255))
d = 200
step = 20

class Plane:
    def __init__(self, polygon, color):
        self.polygon = polygon
        self.color = color


class BSPTree:
    def __init__(self, plane=None):
        self.plane = plane
        self.front = None  # Przednia poddrzewo BSPTree
        self.back = None   # Tylna poddrzewo BSPTree
        self.polygons = [] # Lista przechowująca wielokąty płaszczyzny (ściany)

    def build(self, polygons):
        if not polygons:# or len(polygons) == 0 or len(polygons[0]) < 3:
            return
        # Wybierz pierwszy wielokąt jako podziałową płaszczyznę
        dividing_polygon = polygons[0]
        self.plane = Plane(dividing_polygon, dividing_polygon[0][3])
        front_polygons = []
        back_polygons = []
        # Podziel pozostałe wielokąty względem podziałowej płaszczyzny
        for polygon in polygons[1:]:
            front_points, back_points = self.split_polygon(polygon)
            if len(front_points) >= 3:
                front_polygons.append(front_points)
            if len(back_points) >= 3:
                back_polygons.append(back_points)
        # Rekurencyjnie buduj poddrzewa BSPTree dla przedniej i tylnej części
        if front_polygons:
            self.front = BSPTree()
            self.front.build(front_polygons)
        if back_polygons:
            self.back = BSPTree()
            self.back.build(back_polygons)

    def split_polygon(self, polygon):
        front_points = []
        back_points = []
        # Sprawdź, po której stronie podziałowej płaszczyzny znajdują się wierzchołki wielokąta
        # for point in polygon:
        point = polygon[0]
        if self.side_of_plane(point) == "FRONT":
            for p in polygon:
                front_points.append(p)
        elif self.side_of_plane(point) == "BACK":
            for p in polygon:
                back_points.append(p)
        else:
            for p in polygon:
                front_points.append(p)
                back_points.append(p)
        return front_points, back_points

    def side_of_plane(self, point):
        u1 = [self.plane.polygon[0][0] - self.plane.polygon[1][0], self.plane.polygon[0][1]-self.plane.polygon[1][1], self.plane.polygon[0][2] - self.plane.polygon[1][2]]
        u2 = [self.plane.polygon[2][0] - self.plane.polygon[1][0], self.plane.polygon[2][1]-self.plane.polygon[1][1], self.plane.polygon[2][2] - self.plane.polygon[1][2]]
        normal = np.cross(u1, u2)
        m = -np.dot(normal, [self.plane.polygon[1][0], self.plane.polygon[1][1], self.plane.polygon[1][2]])
        x = np.dot(normal, [point[0], point[1], point[2]]) + m
        # Sprawdź, po której stronie podziałowej płaszczyzny znajduje się punkt
        if x > 0:
            return "FRONT"
        elif x < 0:
            return "BACK"
        else:
            return "COPLANAR"

    def user_side_of_plane(self):
        u1 = [self.plane.polygon[0][0] - self.plane.polygon[1][0],
              self.plane.polygon[0][1] - self.plane.polygon[1][1],
              self.plane.polygon[0][2] - self.plane.polygon[1][2]]
        u2 = [self.plane.polygon[2][0] - self.plane.polygon[1][0],
              self.plane.polygon[2][1] - self.plane.polygon[1][1],
              self.plane.polygon[2][2] - self.plane.polygon[1][2]]
        normal = np.cross(u1, u2)
        x = -np.dot(normal, [self.plane.polygon[1][0], self.plane.polygon[1][1], self.plane.polygon[1][2]])
        # x = np.dot(normal, [0, 0, 0]) + m
        # Sprawdź, po której stronie podziałowej płaszczyzny znajduje się punkt
        if x > 0:
            return "FRONT"
        elif x < 0:
            return "BACK"
        else:
            return "COPLANAR"

    def draw(self):
        sortedP = traverse(self)
        for plane in sortedP:
            points = []
            for point in plane:
                if point[2] <= 0:
                    return
                p = (350 + point[0]*d / point[2], 350 - point[1]*d / point[2])
                points.append(p)
            if plane[0][3] == "red":
                pygame.draw.polygon(win, (255, 0, 0), points)
            else:
                pygame.draw.polygon(win, (0, 0, 255), points)


def traverse(node):
    if node is None:
        return []
    if node.side_of_plane((0, 0, 0)) == "FRONT":
        return traverse(node.back) + [node.plane.polygon] + traverse(node.front)
    elif node.side_of_plane((0, 0, 0)) == "BACK":
        return traverse(node.front) + [node.plane.polygon] + traverse(node.back)
    else:
        return traverse(node.front) + traverse(node.back)

# Współrzędne wierzchołków sześcianów
cube2_vertices = [[-50, -50, 100, "red"], [50, -50, 100, "red"], [-50, 50, 100, "red"], [50, 50, 100, "red"], [-50, -50, 200, "red"], [50, -50, 200, "red"], [-50, 50, 200, "red"], [50, 50, 200, "red"]]
cube1_vertices = [[-100, -50, 200, "blue"], [-200, -50, 200, "blue"], [-100, 50, 200, "blue"], [-200, 50, 200, "blue"], [-100, -50, 300, "blue"], [-200, -50, 300, "blue"], [-100, 50, 300, "blue"], [-200, 50, 300, "blue"]]
# Wierzchołki tworzące ściany sześcianów
cube1_faces = [
    [cube1_vertices[0], cube1_vertices[1], cube1_vertices[2], cube1_vertices[3]],
    [cube1_vertices[4], cube1_vertices[5], cube1_vertices[6], cube1_vertices[7]],
    [cube1_vertices[0], cube1_vertices[1], cube1_vertices[5], cube1_vertices[4]],
    [cube1_vertices[2], cube1_vertices[3], cube1_vertices[7], cube1_vertices[6]],
    [cube1_vertices[0], cube1_vertices[2], cube1_vertices[6], cube1_vertices[4]],
    [cube1_vertices[1], cube1_vertices[3], cube1_vertices[7], cube1_vertices[5]]
]

cube2_faces = [
    [cube2_vertices[0], cube2_vertices[1], cube2_vertices[2], cube2_vertices[3]],
    [cube2_vertices[4], cube2_vertices[5], cube2_vertices[6], cube2_vertices[7]],
    [cube2_vertices[0], cube2_vertices[1], cube2_vertices[5], cube2_vertices[4]],
    [cube2_vertices[2], cube2_vertices[3], cube2_vertices[7], cube2_vertices[6]],
    [cube2_vertices[0], cube2_vertices[2], cube2_vertices[6], cube2_vertices[4]],
    [cube2_vertices[1], cube2_vertices[3], cube2_vertices[7], cube2_vertices[5]]
]

faces = [[0, 2, 3, 1], [4, 6, 7, 5], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]

Lanes = [[1, 2], [2, 4], [1, 3], [3, 4], [1, 5], [2, 6], [3, 7], [4, 8], [5, 6], [5, 7], [6, 8], [7, 8]]
Cubes = [cube1_vertices, cube2_vertices]

pygame.display.flip()

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


# Utwórz drzewo BSPTree i zbuduj je dla sześcianów
def runBsp():
    bsptree = BSPTree()
    all_faces = []
    for cube in Cubes:
        for face in faces:
            new_face = [cube[face[0]], cube[face[1]], cube[face[2]], cube[face[3]]]
            all_faces.append(new_face)
    bsptree.build(all_faces)
    bsptree.draw()
    pygame.display.flip()

# Główna pętla gry
def find_new_points(p1, p2):
    (x1, y1, z1) = p1
    (x2, y2, z2) = p2
    u = [x2-x1, y2-y1, z2-z1]
    new_x = (-d - z1/u[2])*(u[0]/x1)
    new_y = (-d - z1/u[2])*(u[1]/y1)
    new_z = (-d + step)
    return (new_x, new_y, new_z), (x2, y2, z2)


def go_horizontally(is_left):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        color = cube[0][3]
        for point in cube:
            if is_left:
                x = point[0] + step
            else:
                x = point[0] - step
            y = point[1]
            z = point[2]
            new_cube.append([x, y, z, color])
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    runBsp()


def go_vertically(is_up):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        color = cube[0][3]
        for point in cube:
            if is_up:
                y = point[1] - step
            else:
                y = point[1] + step
            x = point[0]
            z = point[2]
            new_cube.append([x, y, z, color])
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    runBsp()


def go(forward):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        color = cube[0][3]
        for point in cube:
            if forward:
                z = point[2] - step
            else:
                z = point[2] + step
            x = point[0]
            y = point[1]
            new_cube.append([x, y, z, color])
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    runBsp()


def rotate_horizontally(up):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        color = cube[0][3]
        for point in cube:
            point[3] = 1
            if up:
                new_point1 = np.matmul(Mrox, point)
                new_point1 = new_point1.tolist()
                new_point1[3] = color
            else:
                matrix = np.array(Mrox)
                inverse_matrix = np.linalg.inv(matrix)
                new_point1 = np.matmul(inverse_matrix, point)
                new_point1 = new_point1.tolist()
                new_point1[3] = color
            new_cube.append(new_point1)
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    runBsp()


def rotate_vertically(left):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        color = cube[0][3]
        for point in cube:
            point[3] = 1
            if left:
                new_point = np.matmul(Mroy, point)
                new_point = new_point.tolist()
                new_point[3] = color
            else:
                matrix = np.array(Mroy)
                inverse_matrix = np.linalg.inv(matrix)
                new_point = np.matmul(inverse_matrix, point)
                new_point = new_point.tolist()
                new_point[3] = color
            new_cube.append(new_point)
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    runBsp()


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
    runBsp()


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
    runBsp()


while True:
    runBsp()
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
                case pygame.K_q:
                    go_vertically(True)
                case pygame.K_z:
                    go_vertically(False)
                case pygame.K_w:
                    go(True)
                case pygame.K_s:
                    go(False)
                case pygame.K_r:
                    rotate_horizontally(True)
                case pygame.K_f:
                    rotate_horizontally(False)
                case pygame.K_x:
                    rotate_vertically(True)
                case pygame.K_c:
                    rotate_vertically(False)
                case pygame.K_v:
                    rotate(True)
                case pygame.K_b:
                    rotate(False)
                case pygame.K_t:
                    zoom(True)
                case pygame.K_g:
                    zoom(False)
