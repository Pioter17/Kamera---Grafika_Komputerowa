import numpy as np
import pygame
import sys

pygame.init()
win = pygame.display.set_mode((700, 700))
win.fill((255, 255, 255))
d = 200
step = 20

class Plane:
    def __init__(self, polygon):
        # Współrzędne trzech punktów definiujących płaszczyznę
        # self.v1 = v1
        # self.v2 = v2
        # self.v3 = v3
        # self.v4 = v4
        self.polygon = polygon


class BSPTree:
    def __init__(self, plane=None):
        self.plane = plane
        self.front = None  # Przednia poddrzewo BSPTree
        self.back = None   # Tylna poddrzewo BSPTree
        self.polygons = [] # Lista przechowująca wielokąty płaszczyzny (ściany)

    def build(self, polygons):
        if not polygons or len(polygons) == 0 or len(polygons[0]) < 3:
            return
        # Wybierz pierwszy wielokąt jako podziałową płaszczyznę
        dividing_polygon = polygons[0]
        # if len(dividing_polygon) < 4:
        #     self.plane = Plane(dividing_polygon[0], dividing_polygon[1], dividing_polygon[2])
        # else:
        # self.plane = Plane(dividing_polygon[0], dividing_polygon[1], dividing_polygon[2], dividing_polygon[3])
        self.plane = Plane(dividing_polygon)
        front_polygons = []
        back_polygons = []
        # Podziel pozostałe wielokąty względem podziałowej płaszczyzny
        for polygon in polygons[1:]:
            front_points, back_points = self.split_polygon(polygon)
            if front_points:
                front_polygons.append(front_points)
            if back_points:
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
        for point in polygon:
            if self.side_of_plane(point) == "FRONT":
                front_points.append(point)
            elif self.side_of_plane(point) == "BACK":
                back_points.append(point)
            else:
                front_points.append(point)
                back_points.append(point)
        # Sprawdź, czy wielokąt przecina podziałową płaszczyznę
        # for i in range(len(polygon)):
        #     v1 = polygon[i]
        #     v2 = polygon[(i+1)%len(polygon)]
        #     if self.side_of_plane(v1) != self.side_of_plane(v2):
        #         # Oblicz punkt przecięcia krawędzi z podziałową płaszczyzną
        #         intersection_point = self.compute_intersection(v1, v2)
        #         front_points.append(intersection_point)
        #         back_points.append(intersection_point)
        # print(front_points, back_points)
        return front_points, back_points

    def side_of_plane(self, point):
        # v1 = [point[0]-self.plane.v1[0], point[1]-self.plane.v1[1], point[2] - self.plane.v1[2]]
        # u1 = [self.plane.v1[0] - self.plane.v2[0], self.plane.v1[1]-self.plane.v2[1], self.plane.v1[2] - self.plane.v2[2]]
        # u2 = [self.plane.v3[0] - self.plane.v2[0], self.plane.v3[1]-self.plane.v2[1], self.plane.v3[2] - self.plane.v2[2]]
        u1 = [self.plane.polygon[0][0] - self.plane.polygon[1][0], self.plane.polygon[0][1]-self.plane.polygon[1][1], self.plane.polygon[0][2] - self.plane.polygon[1][2]]
        u2 = [self.plane.polygon[2][0] - self.plane.polygon[1][0], self.plane.polygon[2][1]-self.plane.polygon[1][1], self.plane.polygon[2][2] - self.plane.polygon[1][2]]
        normal = np.cross(u1, u2)
        # m = -np.dot(normal, self.plane.v2)
        m = -np.dot(normal, self.plane.polygon[1])
        x = np.dot(normal, point) + m
        # Sprawdź, po której stronie podziałowej płaszczyzny znajduje się punkt
        # x = (point[0] - self.plane.v1[0]) * (self.plane.v2[1] - self.plane.v1[1]) - \
        #     (point[1] - self.plane.v1[1]) * (self.plane.v2[0] - self.plane.v1[0])
        if x > 0:
            return "FRONT"
        elif x < 0:
            return "BACK"
        else:
            return "COPLANAR"

    # def compute_intersection(self, v1, v2):
    #     # Oblicz punkt przecięcia krawędzi z podziałową płaszczyzną
    #     divisor = (v2[0] - v1[0]) * (self.plane.v1[1] - self.plane.v2[1]) - \
    #               (v2[1] - v1[1]) * (self.plane.v1[0] - self.plane.v2[0])
    #     if divisor == 0:
    #         return None  # Krawędź jest równoległa do płaszczyzny
    #     t = ((self.plane.v1[0] - v1[0]) * (self.plane.v1[0] - self.plane.v2[0]) + \
    #          (self.plane.v1[1] - v1[1]) * (self.plane.v1[1] - self.plane.v2[1])) / divisor
    #     x = v1[0] + t * (v2[0] - v1[0])
    #     y = v1[1] + t * (v2[1] - v1[1])
    #     z = v1[2] + t * (v2[2] - v1[2])
    #     return (x, y, z)

    def draw(self):
        if self.front or self.back:
            if self.side_of_plane((0, 0, 0)) == "FRONT":
                if self.back:
                    self.back.draw()
                if self.front:
                    self.front.draw()
            elif self.side_of_plane((0, 0, 0)) == "BACK":
                if self.front:
                    self.front.draw()
                if self.back:
                    self.back.draw()
            else:
                if self.front:
                    self.front.draw()
                if self.back:
                    self.back.draw()
        if self.plane:
            # if self.plane.v1[2] <= 0 or self.plane.v2[2] <= 0 or self.plane.v3[2] <= 0:
            #     return
            points = []
            for point in self.plane.polygon:
                if point[2] == 0:
                    return
                p = (350 + point[0]*d / point[2], 350 - point[1]*d / point[2])
                points.append(p)
            # p1 = (350 + self.plane.v1[0]*d / self.plane.v1[2], 350 - self.plane.v1[1]*d / self.plane.v1[2])
            # p2 = (350 + self.plane.v2[0]*d / self.plane.v2[2], 350 - self.plane.v2[1]*d / self.plane.v2[2])
            # p3 = (350 + self.plane.v3[0]*d / self.plane.v3[2], 350 - self.plane.v3[1]*d / self.plane.v3[2])
            # if self.plane.v4[2] == 0:
            #     pygame.draw.polygon(win, (0, 255, 0), [p1, p2, p3])
            # else:
            # p4 = (350 + self.plane.v4[0]*d / self.plane.v4[2], 350 + self.plane.v4[1]*d / self.plane.v4[2])
            pygame.draw.polygon(win, (0, 255, 0), points)

# Współrzędne wierzchołków sześcianów
# cube1_vertices = [[100, 100, 400], [200, 100, 400], [100, 200, 400], [200, 200, 400], [100, 100, 500], [200, 100, 500], [100, 200, 500], [200, 200, 500]]
cube2_vertices = [[100, 100, 200], [200, 100, 200], [100, 200, 200], [200, 200, 200], [100, 100, 300], [200, 100, 300], [100, 200, 300], [200, 200, 300]]
cube1_vertices = [[-100, 100, 200], [-200, 100, 200], [-100, 200, 200], [-200, 200, 200], [-100, 100, 300], [-200, 100, 300], [-100, 200, 300], [-200, 200, 300]]
# cube2_vertices = [[100, -100, 300], [200, -100, 300], [100, -200, 300], [200, -200, 300], [100, -100, 400], [200, -100, 400], [100, -200, 400], [200, -200, 400]]

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

faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]

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
    runBsp()


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
    runBsp()


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
    runBsp()


def rotate_horizontally(up):
    for i in range(len(Cubes)):
        cube = Cubes[i]
        new_cube = []
        for point in cube:
            point.append(1)
            if up:
                new_point1 = np.matmul(Mrox, point)
                new_point1 = new_point1.tolist()
                new_point1.pop()
            else:
                matrix = np.array(Mrox)
                inverse_matrix = np.linalg.inv(matrix)
                new_point1 = np.matmul(inverse_matrix, point)
                new_point1 = new_point1.tolist()
                new_point1.pop()
            new_cube.append(new_point1)
        Cubes[i] = new_cube
    win.fill((255, 255, 255))
    runBsp()


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


for i in range(len(Cubes)):
    cube = Cubes[i]
    new_cube = []
    new_normalized_cube = []
    for point in cube:
        x = point[0]
        y = point[1]
        z = point[2]


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
