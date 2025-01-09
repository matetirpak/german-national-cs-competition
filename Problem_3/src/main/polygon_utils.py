import math
import sys

def rotate_point(point, anchor, angle_radians):
    '''Rotiert einen Punkt um einen anderen'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    point_x, point_y = point
    anchor_x, anchor_y = anchor

    # Der Punkt wird so verlegt, dass der Anchorpunkt dem Ursprung entspricht
    translated_x = point_x - anchor_x
    translated_y = point_y - anchor_y

    s = math.sin(angle_radians)
    c = math.cos(angle_radians)

    # Ermitteln der rotierten Koordinaten
    rotated_x = translated_x * c - translated_y * s
    rotated_y = translated_x * s + translated_y * c

    # Zurückverschieben des Punktes
    final_x = rotated_x + anchor_x
    final_y = rotated_y + anchor_y

    return (final_x, final_y)


def angle_of_point(anchor, point):
    '''Winkel eines Punkts im Einheitskreis'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    translated_point = (point[0] - anchor[0], point[1] - anchor[1])
    x, y = translated_point
    
    # Sonderfälle werden behandelt
    if x == 0:
        if y > 0:
            return math.pi/2
        else:
            return math.pi/2*3
    if y == 0:
        if x > 0:
            return 0
        else:
            return math.pi
    
    angle = math.atan(y/x)

    # Punkt liegt im 2. oder 3. Quadranten
    if x < 0:
        angle += math.pi
    # Punkt liegt im 4. Quadranten
    if x > 0 and y < 0:
        angle += math.pi*2
    
    return angle


def create_edges(vertices):
    '''Erstellt Seiten aus den n Eckpunkten des Polygons'''
    '''Time Complexity: O(n) für n Eckpunkte, Auxiliary Space: O(n) für n Eckpunkte'''
    edges = []
    for i, _ in enumerate(vertices):
        edges.append([vertices[i], vertices[(i+1) % len(vertices)]])
    return edges


def do_lines_intersect(point, edge):
    '''ray-casting mit einem Strahl nach rechts'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    p_x, p_y = point
    low_x, low_y = edge[0]
    high_x, high_y = edge[1]
    
    # Stellt sicher, dass 'high' gewiss der höhere Punkt ist
    if low_y > high_y:
        low_x, high_x = high_x, low_x
        low_y, high_y = high_y, low_y

    # Falls der Punkt in einem Eckpunkt liegt, sollen nicht 2 Schnitte für 2 anliegende Seiten registriert werden
    if p_y == low_y or p_y == high_y:
        p_y += 0.00001
    
    # Punkt liegt oberhalb, unterhalb oder weit rechts von der Seite, Schnitt nicht möglich
    if p_y > high_y or p_y < low_y or p_x > max(low_x, high_x):
        return False
    
    # Punkt liegt weit links von der Seite, Schnitt
    if p_x < min(low_x, high_x):
        return True

    # Sonderfälle werden behandelt    
    if high_x - low_x == 0:
        edge_angle = sys.float_info.max
    else:
        edge_angle = (high_y - low_y) / (high_x - low_x)
    if p_x - low_x == 0:
        if edge_angle > 0:
            point_angle = sys.float_info.max
        else:
            point_angle = sys.float_info.min
    else:
        point_angle = (p_y - low_y) / (p_x - low_x)
    
    if abs(edge_angle - sys.float_info.max) < 100 and point_angle < 0:
        edge_angle = sys.float_info.min

    # Größerer Winkel des Punktes deutet darauf hin, dass dieser links von der Seite liegt
    return point_angle > edge_angle


def is_point_in_polygon(polygon_edges, point):
    '''Bei einer ungeraden Anzahl geschnittener Seiten liegt der Punkt im Polygon'''
    '''Time Complexity: O(n) für n Seiten, Auxiliary Space: O(1)'''
    count = 0
    for edge in polygon_edges:
        if do_lines_intersect(point, edge):
            count += 1
    return count % 2 == 1


def no_point_in_triangle(triangle_vertices, polygon_vertices):
    '''Untersucht ob sich kein Punkt im Dreieck befindet, genutzt für ear clipping'''
    '''Time Complexity: O(n) für n Eckpunkte des Polygons, Auxiliary Space: O(n) für n Seiten'''
    triangle_edges = create_edges(triangle_vertices)
    for vertex in polygon_vertices:
        # Punkt entspricht einem Punkt des Dreiecks, überspringen
        if vertex in triangle_vertices:
            continue
        # Punkt liegt im Dreieck
        if is_point_in_polygon(triangle_edges, vertex):
            return False
    # Kein Punkt liegt im Dreieck
    return True


def euclidean_distance(point1, point2):
    '''Geometrischer Abstand zweier Punkte'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    x1, y1 = point1
    x2, y2 = point2
    # Pythagoras
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return distance

def is_point_in_circle(point, circle_anchor):
    '''Untersucht, ob die euklidische Distanz kleiner als der Radius ist'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    distance = euclidean_distance(point, circle_anchor)
    return distance < 85.0

