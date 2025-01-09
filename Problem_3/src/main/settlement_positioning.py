from math import radians

from visualizations import *

class Settlement(object):
    def __init__(self, pos_x, pos_y): 
        self.pos_x = pos_x
        self.pos_y = pos_y


def factorial_sum(n):
    '''Wendet die Fakultät von n an, allerdings wird statt Multiplikation Addition verwendet'''
    '''Time Complexity: O(n), Auxiliary Space: O(1)'''
    result = 0
    while n > 0:
        result += n
        n -= 1
    return result
    

def place_settlements(circle_anchor, polygon_vertices, visualization=False):
    '''Platziert alle Siedlungen in Abhängigkeit von der maximalen Distanz im Polygons'''
    '''Time Complexity: etwa O(d^2) für d als maximale Distanz, Auxiliary Space: etwa O(d^2) für d als maximale Distanz'''
    #abs(vertex[0] - circle_anchor[0]) + abs(vertex[1] - circle_anchor[1])
    max_dist, pos = max(((euclidean_distance(vertex, circle_anchor), vertex) for vertex in polygon_vertices), key=lambda x: x[0])
    max_dist += 20
    if visualization:
        visualize_polygon(polygon_vertices, draw_line=(circle_anchor, pos), title='longest distance')
    settlements = []
    inner_settlements = place_inner_settlements(circle_anchor)
    outer_settlements = place_outer_settlements(circle_anchor, max_dist)
    
    settlements += inner_settlements + outer_settlements
    
        
    if visualization:
        visualize_polygon(polygon_vertices, settlements=settlements, circle_anchor=circle_anchor)
    return settlements

def place_inner_settlements(circle_anchor):
    '''Platzierung der Siedlungen innerhalb des Gesundheitszentrums in einer Hexagon-Struktur'''
    '''Time Complexity: O(1), Auxiliary Space: O(s) für s Siedlungen'''
    anchor_x, anchor_y = circle_anchor
    settlements = []
    
    # Anhand des Abstandes 10 zweier Siedlungen, Rundung von 85 auf 90
    dist = 90
    
    # Platzierung der Siedlungen links vom Mittelpunkt
    for x in range(-dist, 0+1, 10):
        # Platzierung der oben gelegenen Siedlungen
        for y in range(dist//10+1):
            pos_x = anchor_x + x + y * 5
            pos_y = anchor_y + y * 8.660254037844386
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
        # Platzierung der unten gelegenen Siedlungen
        for y in range(1, (dist+x)//10+1, 1):
            pos_x = anchor_x + x - y * 5
            pos_y = anchor_y - y * 8.660254037844386
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
    
    # Platzierung der Siedlungen rechts vom Mittelpunkt
    for x in range(10, dist+1, 10):
        # Platzierung der unten gelegenen Siedlungen
        for y in range(dist//10+1):
            pos_x = anchor_x + x - y * 5
            pos_y = anchor_y - y * 8.660254037844386
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
        # Platzierung der oben gelegenen Siedlungen
        for y in range(1, (dist-x)//10+1, 1):
            pos_x = anchor_x + x + y * 5
            pos_y = anchor_y + y * 8.660254037844386
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
    
    # Entfernen der außerhalb des Radius von 85 liegenden Siedlungen, da die Hexagon-Struktur an den Ecken aus dem Kreis hinausragt
    settlements.pop(((dist//10+1)**2)*2 + factorial_sum(dist//10-1)*2-2)
    settlements.pop(((dist//10+1)**2)*2 + factorial_sum(dist//10-1)*2-3)
    settlements.pop(((dist//10+1)**2)*2 + factorial_sum(dist//10-1)*2-1-dist//10)
    settlements.pop(((dist//10+1)**2)*2 + factorial_sum(dist//10-1)*2-2-dist//10)
    settlements.pop(((dist//10+1)**2)*2 + factorial_sum(dist//10-1)*2-3-dist//10)
    settlements.pop(((dist//10+1)**2)*2 + factorial_sum(dist//10-1)*2-4-(dist+1)//10)
    settlements.pop((dist//10+1)**2+factorial_sum(dist//10-1)-1+dist//10*3)
    settlements.pop((dist//10+1)**2+factorial_sum(dist//10-1)+dist//5)
    settlements.pop((dist//10+1)**2+factorial_sum(dist//10-1)-1+dist//10)
    settlements.pop((dist//10+1)**2+factorial_sum(dist//10-1)-1)
    settlements.pop((dist//10+1)*(dist//10)+factorial_sum(dist//10-1)-1)
    settlements.pop((dist//10+1)*(dist//10)+factorial_sum(dist//10-2)-1)
    settlements.pop((dist//10+1)*2)
    settlements.pop((dist//10+1)*2-1)
    settlements.pop(dist//10)
    settlements.pop(dist//10-1)
    settlements.pop(1)
    settlements.pop(0)

    return settlements
    

def place_outer_settlements(circle_anchor, max_dist):
    '''Platzierung der Siedlungen außerhalb des Gesundheitszentrums'''
    '''Time Complexity: etwa O(d^2) für d als maximale Distanz, Auxiliary Space: O(s) für s Siedlungen'''
    anchor_x, anchor_y = circle_anchor
    settlements = []
    dist = 90
    if max_dist-dist < 10:
        return []
    
    dist = int(max_dist//20)*20
    for x in range(-dist, -80, 20):
        for y in range(dist//20+1):
            pos_x = anchor_x + x + y * 10
            pos_y = anchor_y + y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
        for y in range(1, (dist+x)//20+1, 1):
            pos_x = anchor_x + x - y * 10
            pos_y = anchor_y - y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
    
    for x in range(-80, 0+1, 20):
        for y in range(5, dist//20+1):
            pos_x = anchor_x + x + y * 10
            pos_y = anchor_y + y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
        for y in range((80+x)//20+1, (dist+x)//20+1, 1):
            pos_x = anchor_x + x - y * 10
            pos_y = anchor_y - y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
    
    for x in range(20, 80+1, 20):
        for y in range(5, dist//20+1):
            pos_x = anchor_x + x - y * 10
            pos_y = anchor_y - y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
        for y in range((80-x)//20+1, (dist-x)//20+1, 1):
            pos_x = anchor_x + x + y * 10
            pos_y = anchor_y + y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
    
    for x in range(100, dist+1, 20):
        for y in range(dist//20+1):
            pos_x = anchor_x + x - y * 10
            pos_y = anchor_y - y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)
        for y in range(1, (dist-x)//20+1, 1):
            pos_x = anchor_x + x + y * 10
            pos_y = anchor_y + y * 8.660254037844386*2
            s = Settlement(pos_x, pos_y)
            settlements.append(s)

    return settlements


def optimize_rotation(polygon_edges, settlements, anchor, precision=1):
    '''Findet die beste Rotation der Siedlungen'''
    '''Time Complexity: O(w*s*n) w untersuchte Winkel, s Siedlungen und n Seiten des Polygons, Auxiliary Space: O(1)'''
    precision = int(precision)
    best_angle = 0
    max_settlements = 0
    
    # Ermitteln der optimalen Rotation
    for angle_degrees in range(0, 60*precision, 1):
        angle = radians(angle_degrees/precision)
        settlements_in_polygon = 0
        for settlement in settlements:
            # Anwendung der zu testenden Rotation
            new_x, new_y = rotate_point((settlement.pos_x, settlement.pos_y), anchor, angle)
            if is_point_in_polygon(polygon_edges, (new_x, new_y)):
                # Zählen der gültigen Siedlungen
                settlements_in_polygon += 1
        if settlements_in_polygon > max_settlements:
            # Merken der besten Daten
            max_settlements = settlements_in_polygon
            best_angle = angle
    
    # Anwendung der optimalen Rotation
    for settlement in settlements:
        settlement.pos_x, settlement.pos_y = rotate_point((settlement.pos_x, settlement.pos_y), anchor, best_angle)
    
    return settlements


def remove_outside_settlements(polygon_edges, settlements):
    '''Entfernt alle Siedlungen außerhalb des Polygons'''
    '''Time Complexity: O(s*n) für s Siedlungen und n Seiten des Polygons, Auxiliary Space: O(s) für s Siedlungen'''
    correct_settlements = []
    for settlement in settlements:
        if is_point_in_polygon(polygon_edges, (settlement.pos_x, settlement.pos_y)):
            # Korrekte Siedlungen werden gespeichert
            correct_settlements.append(settlement)
    return correct_settlements