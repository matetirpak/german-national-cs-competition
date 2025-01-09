from heapq import heappush, heappop, heapify
import time

from circle_area import *
from visualizations import *

def get_facility_location(polygon_vertices, splits=10, depth_finish=5, depth_stop=3, force_area_calculation=False, visualize=False, visualize_beginning=False):
    '''Findet die beste Position des Gesundheitszentrums'''
    '''Time Complexity: O(p * O(Heuristik)), Auxiliary Space: O(h) für h Einträge im Heap'''
    polygon_edges = create_edges(polygon_vertices)
    
    # Eckpunkte des rechteckigen Untersuchungsbereichs werden ermittelt
    max_x = max(vertex[0] for vertex in polygon_vertices)
    min_x = min(vertex[0] for vertex in polygon_vertices)
    max_y = max(vertex[1] for vertex in polygon_vertices)
    min_y = min(vertex[1] for vertex in polygon_vertices)

    bottom_left = (min_x, min_y)
    bottom_right = (max_x, min_y)
    top_left = (min_x, max_y)
    top_right = (max_x, max_y)
    
    # Rechteckiger Untersuchungsbereich
    vertices = [bottom_left, bottom_right, top_right, top_left]
    
    distance_x = (max_x - min_x) / splits
    distance_y = (max_y - min_y) / splits

    # Erstellen der ersten Schicht Punkte
    points = []

    current_y = max_y-(distance_y/2)
    stop_y = min_y
    step_y = -distance_y
    
    stop_x = max_x
    step_x = distance_x
    
    while current_y > stop_y:
        current_x = min_x+(distance_x/2)
        while current_x < stop_x:
            points.append([current_x,current_y])
            current_x += step_x
        current_y += step_y

    
    # Heuristic für das Vergleichen der Kreispotenziale
    if force_area_calculation:
        get_circle_value = get_circle_area
    else:
        get_circle_value = area_settlement_approximation # O(n*m)

    
    if depth_stop >= depth_finish:
        depth_stop == depth_finish-1

    areas = []
    # Einfügen der Untersuchungspunkte in einen Heap
    # [Heuristic, Tiefe, ID, Koordinaten]
    max_heap = deepcopy(points)
    id = 0
    for i, point in enumerate(max_heap):
        #print(point)
        point_data = deepcopy(point)
        try:
            area = get_circle_value(polygon_vertices, point, visualize=False)
        except Exception:
            print(f'error: {point}')
            area = 0
        point_data = [-area, 1, id] + [point_data]
        max_heap[i] = point_data
        areas.append(int(area))
        # Verhindert, dass der Heap bei gleicher Fläche und Tiefe möglicherweise im nächsten Index unvergleichbare Datentypen zu vergleichen versucht
        id += 1

    elapsed_time_during_visualization = None
    if visualize or visualize_beginning:
        start = time.time()
        visualize_grid(polygon_vertices, vertices, points, areas=areas)
        end = time.time()
        elapsed_time_during_visualization = end - start

    heapify(max_heap)
    
    while True:
        # Daten des derzeitig wertvollsten Punktes
        area, depth, _, point = heappop(max_heap)
        
        if depth == depth_finish:
            # Lösung zurückgeben
            return point, elapsed_time_during_visualization
        
        # zu untersuchender Punkt
        x = point[0]
        y = point[1]
        
        # 9 neue Punkte werden in einem Gitter platziert, die Abstände sind halb so groß wie die der vorherigen Tiefe
        current_y = y + distance_y/(2**(depth))
        for _ in range(3):
            current_x = x - distance_x/(2**(depth))
            for _ in range(3):
                new_point = [current_x, current_y]
                # Punkt muss um Untersuchungsbereich liegen
                if point_in_area(new_point, max_x, min_x, max_y, min_y):
                    try:
                        area = get_circle_value(polygon_vertices, new_point, visualize_result=False)
                    except Exception:
                        area = 0
                    # Punkt wird nur zum Heap hinzugefügt wenn er nicht die Stop-Tiefe überschritten hat und außerhalb des Polygons liegt
                    if not (depth+1 > depth_stop and not is_point_in_polygon(polygon_edges, new_point)):
                        point_data = [-area, depth+1, id] + [new_point]
                        points.append(new_point)
                        heappush(max_heap, point_data)
                        id += 1
                current_x += distance_x/(2**(depth))
            current_y -= distance_y/(2**(depth))
        if visualize:
            visualize_grid(polygon_vertices, vertices, points)

def point_in_area(point, max_x, min_x, max_y, min_y):
    '''Ermittelt, ob sich ein Punkt im Untersuchungsbereich befindet, O(1)'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    x, y = point
    return max_x > x and x > min_x and max_y > y and x > min_y

