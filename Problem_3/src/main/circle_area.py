from sympy import Eq, solve, symbols, simplify
from copy import deepcopy

from polygon_utils import *
from visualizations import *
from settlement_positioning import *

decimal_precision = 7

def get_circle_intersection_points(polygon_vertices, circle_anchor):
    '''Bestimmt die Schnittpunkte des Kreises und Polygons in O(n*m) für n Seiten bzw. Eckpunkte und das Lösen des Gleichungssystems in m'''
    '''Time Complexity: O(n*m) für n Eckpunkte des Polygons und m als Zeitkomplexität der solve Funktion aus sympy, Auxiliary Space: O(n+s) für n Eckpunkte des Polygons und s Schnittpunkte'''
    global decimal_precision
    sols = []
    intersection_edges_point = dict()

    circle_x, circle_y = circle_anchor
    r = 85
    x, y = symbols ('x y', real=True)
    circle_equation = Eq((x-circle_x)**2+(y-circle_y)**2, r**2)

    polygon_edges = create_edges(polygon_vertices)
    i = 0
    while i < len(polygon_edges):
        edge = polygon_edges[i]
        x1, y1 = edge[0]
        x2, y2 = edge[1]
        if x2-x1 == 0:
            edge_equation = Eq(x, x1)
        else:
            slope = (y2-y1) / (x2-x1)
            edge_equation = Eq(y - y1, slope * (x - x1))
        potential_sol = solve((circle_equation, edge_equation), (x, y))
        
        sol = []
        for s in potential_sol:
            s_x = s[0]
            s_y = s[1]
            if min(x1,x2) <= s_x and s_x <= max(x1,x2) and min(y1,y2) <= s_y and s_y <= max(y1,y2):
                sol.append(s)
        
                    
        if len(sol) == 2:
            sol_1 = sol[0]
            sol_2 = sol[1]
            new_point = [(sol_1[0]+sol_2[0])/2, (sol_1[1]+sol_2[1])/2]
            polygon_vertices.insert(i+1, new_point)
            polygon_edges = create_edges(polygon_vertices)
            i-=1

        elif len(sol) == 1:
            if is_point_in_circle(edge[0], circle_anchor) or is_point_in_circle(edge[1], circle_anchor):
                x_sol = custom_round(sol[0][0], decimal_precision)
                y_sol = custom_round(sol[0][1], decimal_precision)
                new_sol = (x_sol,y_sol)
                sols += [new_sol]
                
                edge_str = str(custom_round(edge[0][0],decimal_precision)) + ' ' + str(custom_round(edge[0][1],decimal_precision)) + '_' + str(custom_round(edge[1][0],decimal_precision)) + ' ' + str(custom_round(edge[1][1],decimal_precision))
                intersection_edges_point[edge_str] = new_sol
        i+=1
            
    
    return sols, circle_anchor, intersection_edges_point, polygon_vertices

def get_circle_area(polygon_vertices, circle_anchor, visualize=False, visualize_result=False):
    '''Berechnet die Schnittfläche eines Polygons und Kreises des Radius 85'''
    '''Time Complexity: O(m*n^2) für m Polygone mit n Eckpunkten, Auxiliary Space: O(e+s+z) für e Eckpunkt des Polygons im Kreis, s Schnittpunkte und z zusätziche Punkte'''
    global decimal_precision
    
    intersection_points, _, intersection_edges_point, polygon_vertices = get_circle_intersection_points(polygon_vertices, circle_anchor)
    polygon_edges = create_edges(polygon_vertices)
    
    # Es gibt höchstens einen Berührungspunkt
    if len(intersection_points) <= 1:
        # Polygon liegt im Kreis
        if euclidean_distance(polygon_vertices[0], circle_anchor) < 85:
            return calculate_polygon_area(polygon_vertices)
        # Polygon umschließt den Kreis
        elif is_point_in_polygon(polygon_edges, circle_anchor):
            return (85**2)*math.pi
        # Poly
        else:
            return 0
    
    # Alle Winkel der Schnittpunkte werden errechnet
    angles = []
    for point in intersection_points:
        angle = angle_of_point(circle_anchor, (point[0]/(10**decimal_precision),point[1]/(10**decimal_precision)))
        angles.append(angle)
    all_angles = []
    new_angles = []
    angles = sorted(angles)
    
    # Zwischen die Schnittpunkte werden zu untersuchende Punkte positioniert
    for i, angle in enumerate(angles):
        new_angle = (angle + angles[(i+1) % len(angles)]) / 2
        if len(new_angles) != 0:
            if new_angle <= max(new_angles):
                new_angle += math.pi
        new_angles.append(new_angle)
        angle_tuple = (angle, angles[(i+1) % len(angles)], new_angle)
        all_angles.append(angle_tuple)
    if visualize:
        visualize_circle(all_angles=all_angles, circle_anchor=circle_anchor)
    
    # Bei korrektem Zwischenpunkt wird ein Intervall bestehend aus den anliegenden Schnittpunkten gespeichert
    intervals = []
    correct_test_points = []
    for angle_tuple in all_angles:
        test_angle = angle_tuple[2]
        test_point = rotate_point((85+circle_anchor[0],circle_anchor[1]),circle_anchor,test_angle)
        if is_point_in_polygon(polygon_edges, test_point):
            intervals.append((angle_tuple[0], angle_tuple[1]))
            correct_test_points.append(test_point)
    if visualize:
        visualize_circle(all_angles=all_angles, correct_test_points=correct_test_points, polygon_vertices=polygon_vertices, circle_anchor=circle_anchor)

    
    # die Intervalle, gekennzeichnet durch Winkel, sollen zu Punkten transformiert werden
    intervals_points = []
    # das zugehörige Intervall soll durch beide Schnittpunkte abfragbar sein
    intersection_to_interval = dict()

    for interval in intervals:
        point1 = rotate_point((circle_anchor[0]+85,circle_anchor[1]),circle_anchor, interval[0])
        point2 = rotate_point((circle_anchor[0]+85,circle_anchor[1]),circle_anchor, interval[1])

        point1 = (custom_round(point1[0], decimal_precision), custom_round(point1[1], decimal_precision))
        point2 = (custom_round(point2[0], decimal_precision), custom_round(point2[1], decimal_precision))

        intervals_points.append((point1,point2))
        
        point1 = str(point1[0]) + ' ' + str(point1[1])
        intersection_to_interval[point1] = interval
        
        point2 = str(point2[0]) + ' ' + str(point2[1])
        intersection_to_interval[point2] = interval
    
    
    # Punkte außerhalb des Kreises sollen abgeschnitten werden
    vertices_inside_circle = []
    for i, vertex in enumerate(polygon_vertices):
        # erster Punkt liegt im Kreis
        bool_1 = euclidean_distance(vertex, circle_anchor) < 85
        if bool_1:
            vertices_inside_circle.append(vertex)
        # zweiter Punkt liegt im Kreis
        bool_2 = euclidean_distance(polygon_vertices[(i+1)%len(polygon_vertices)], circle_anchor) < 85
        # ein Punkt liegt innerhalb, der andere außerhalb, folglich existiert ein Schnitt
        if bool_1 != bool_2:
            # es wird der Schnittpunkt gesucht
            edge = [vertex, polygon_vertices[(i+1)%len(polygon_vertices)]]
            edge_str = str(custom_round(edge[0][0],decimal_precision)) + ' ' + str(custom_round(edge[0][1],decimal_precision)) + '_' + str(custom_round(edge[1][0],decimal_precision)) + ' ' + str(custom_round(edge[1][1],decimal_precision))
            
            intersection_point = intersection_edges_point[edge_str]
            # es wird die Nummer des Intervalls, zu dem der Punkt gehört, gesucht
            intersection_num = -1
            for j, interval_point in enumerate(intervals_points):
                point1 = interval_point[0]
                point2 = interval_point[1]
                if (abs(point1[0] - intersection_point[0]) < decimal_precision*10 and abs(point1[1] - intersection_point[1]) < decimal_precision*10) or (abs(point2[0] - intersection_point[0]) < decimal_precision*10 and abs(point2[1] - intersection_point[1]) < decimal_precision*10):
                    intersection_num = j
            if intersection_num == -1:
                raise Exception()
            # der Schnittpunkt wird zusammen mit seiner Intervallnummer gespeichert
            vertices_inside_circle.append((intersection_point[0], intersection_point[1], intersection_num))

    # wenn zwei Schnittpunkte nebeneinander liegen, wird dies gekennzeichnet, indem die Intervallnummer zu -1 geändert wird
    for i, vertex in enumerate(vertices_inside_circle):
        next_vertex = vertices_inside_circle[(i+1)%len(vertices_inside_circle)]
        if isinstance(vertex, tuple) and isinstance(next_vertex, tuple):
            if vertex[2] == next_vertex[2]:
                vertices_inside_circle[i] = (vertex[0],vertex[1],-1)
                vertices_inside_circle[(i+1)%len(vertices_inside_circle)] = (next_vertex[0],next_vertex[1],-1)

    # einzelne Teilflächen werden entnommen
    polygons = []
    silent_interval = []
    while len(vertices_inside_circle) > 0:
        end = True
        unique_intervals = set()
        # überprüft, ob das Endstadium erreicht ist
        for vertex in vertices_inside_circle:
            if isinstance(vertex, tuple) and vertex[2] != -1 and vertex[2] not in silent_interval:
                unique_intervals.add(vertex[2])
                if len(unique_intervals) > 0:
                    end = False
                    break
        if end:
            polygons += [vertices_inside_circle]
            vertices_inside_circle = []
            break
    
        # es wird eine Teilfläche gesucht
        objective = -2
        objective_i = -2
        i = 0
        while True:
            if i>len(vertices_inside_circle)*2-2:
                break
            vertex = vertices_inside_circle[i%len(vertices_inside_circle)]
            
            if isinstance(vertex, tuple) and vertex[2] != -1 and vertex[2] not in silent_interval:
                if objective == vertex[2]:
                    if abs(i-objective_i) == 1 and objective not in silent_interval:
                        # Intervall bildet keine eigene Teilfläche ab
                        silent_interval.append(objective)
                        continue
                    # Intervall begrenzt eine Teilfläche und wird separiert
                    if i<len(vertices_inside_circle):
                        polygons += [vertices_inside_circle[objective_i:i+1]]
                        vertices_inside_circle = vertices_inside_circle[:objective_i] + vertices_inside_circle[i+1:]
                        break
                    else:
                        polygons += [vertices_inside_circle[:i%len(vertices_inside_circle)+1] + vertices_inside_circle[objective_i:]]
                        vertices_inside_circle = vertices_inside_circle[i%len(vertices_inside_circle)+1:objective_i]
                        break
                objective = vertex[2]
                objective_i = i
            i+=1
    
    # Genaugkeit der Platzierung der Extra-Punkte zwischen 2 Schnittpunkten
    distance = 30
    angle_diff = math.pi/distance
    
    # für jedes Polygon werden die Intervalle der Kreisschnittpunkte mit Extra-Punkten gefüllt
    for i, polygon in enumerate(polygons):
        complicated = False
        for vertex in polygon:
            if isinstance(vertex, tuple):
                if vertex[2] != -1:
                    complicated = True
                    break
        
        new_polygon = deepcopy(polygon)
        
        # Polygon beinhaltet mehrere Schnittpunktsegmente
        if complicated:
            j = len(new_polygon)-2
            
            if isinstance(polygon[0], tuple):
                intersection_1 = polygon[0]
                intersection_2 = polygon[-1]
                segment = get_intersection_segment(intersection_1, intersection_2, intersection_to_interval, angle_diff, circle_anchor)

                new_polygon += segment
                
            while j > 1:
                if isinstance(new_polygon[j], tuple):
                    intersection_1 = [new_polygon[j][0], new_polygon[j][1]]
                    intersection_2 = [new_polygon[j-1][0], new_polygon[j-1][1]]
                    segment = get_intersection_segment(intersection_1, intersection_2, intersection_to_interval, angle_diff, circle_anchor)

                    new_polygon = new_polygon[:j] + segment + new_polygon[j:]
                    j-=1
                j -= 1
        # Polygon beinhaltet nur 1 Schnittpunktsegment
        else:
            if isinstance(polygon[0], tuple) and isinstance(polygon[-1], tuple):
                j = len(new_polygon)-2
                intersection_1 = polygon[0]
                intersection_2 = polygon[-1]
                segment = get_intersection_segment(intersection_1, intersection_2, intersection_to_interval, angle_diff, circle_anchor)
                new_polygon += segment
                stop = 1
            else:
                j = len(new_polygon)-1
                stop = 0
            while j > stop:
                if isinstance(new_polygon[j], tuple):
                    intersection_1 = [new_polygon[j][0], new_polygon[j][1]]
                    intersection_2 = [new_polygon[j-1][0], new_polygon[j-1][1]]
                    segment = get_intersection_segment(intersection_1, intersection_2, intersection_to_interval, angle_diff, circle_anchor)

                    new_polygon = new_polygon[:j] + segment + new_polygon[j:]
                    j-=1
                j -= 1
        polygons[i] = new_polygon
    
    # Visualisierung des Polygons aufgebaut durch die einzelnen Teilflächen
    if visualize or visualize_result:
        circle = plt.Circle(circle_anchor, 85, color='b', fill=False)
        ax = plt.gca()
        for polygon in polygons:
            if len(polygon) > 0:
                for i, vertex in enumerate(polygon):
                    if isinstance(vertex, tuple):
                        polygon[i] = [vertex[0]/(10**decimal_precision), vertex[1]/(10**decimal_precision)]

                x, y = zip(*(polygon + [polygon[0]]))
                ax.plot(x, y)
        ax.set_aspect('equal')
        ax.add_patch(circle)
        plt.show()
        
        ax = plt.gca()
        ax.set_aspect('equal')
        circle = plt.Circle(circle_anchor, 85, color='b', fill=False)
        ax.add_patch(circle)
        for polygon in polygons:
            triangles = ear_clipping(polygon)
            for triangle in triangles:
                x, y = zip(*(triangle + [triangle[0]]))
                plt.plot(x,y)
        plt.show()

    
    # Berechnung des insgesamten Flächeninhalts
    area = calculate_multiple_polygon_area(polygons)
    
    return area

def get_intersection_segment(intersection_1, intersection_2, intersection_to_interval, angle_diff, circle_anchor):
    '''Erstellt zusätzliche Punkte zwischen zwei Schnittpunkten des Kreises'''
    '''Time Complexity: O(w*d) für w als Winkeldifferenz zwischen denen zweier zusätzlicher Punkten und d als Differenz der Winkel der Schnittpunkte, 
       Auxiliary Space: äquivalent zur Zeitkomplexität, da pro Zeiteinheit genau ein Punkt geschaffen wird'''
    # Intervall wird abgefragt
    intersection_str = str(intersection_1[0]) + ' ' + str(intersection_1[1])
    interval = None
    try:
        interval = intersection_to_interval[intersection_str]
    except KeyError:
        for key, value in intersection_to_interval.items():
            num_key = key.split()
            if abs(int(num_key[0]) - intersection_1[0]) < decimal_precision*10 and abs(int(num_key[1]) - intersection_1[1]) < decimal_precision*10:
                interval = value
                break
    if interval == None:
        print('No interval')
        raise Exception()
    
    # Es wird der im Einheitskreis kleinere Winkel gesucht
    # Punkten werden ihr Winkel zugeordnet
    intersection_1 = (intersection_1[0]/(10**decimal_precision), intersection_1[1]/(10**decimal_precision))
    intersection_2 = (intersection_2[0]/(10**decimal_precision), intersection_2[1]/(10**decimal_precision))
    potentially_smaller_angle = angle_of_point(circle_anchor, intersection_1)
    potentially_bigger_angle = angle_of_point(circle_anchor, intersection_2)
    
    # Index des kleineren Winkels
    smaller_angle = 0
    if potentially_smaller_angle > potentially_bigger_angle:
        # Erster Winkel ist größer, folglich ist Index 1 der kleinere
        smaller_angle = 1
    
    # Fälschlich größerer Winkel des Intervalls überschreitet 360° und ist daher im Einheitskreis kleiner. Indexe müssen getauscht werden
    if interval[0] > interval[1]:
        if smaller_angle == 0:
            smaller_angle = 1
        else:
            smaller_angle = 0

    # Es werden die Extra-Punkte generiert
    current = interval[0] + angle_diff
    segment = []
    stop_condition = interval[1]
    if interval[1] < interval[0]:
        stop_condition += math.pi*2
    while current < stop_condition: 
        new_point = rotate_point((85+circle_anchor[0],circle_anchor[1]), circle_anchor, current)
        segment.append([new_point[0],new_point[1]])
        current += angle_diff
    
    # Segment wird in die richtige Richtung gedreht
    if smaller_angle == 0:
        reversed_segment = deepcopy(segment)
        reversed_segment.reverse()
        return reversed_segment
    else:
        return segment

def custom_round(n, decimals):
    '''convertiert float zu int und behält "decimals" Nachkommastellen in O(1)'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    n *= 10**decimals
    n = n // 1
    n = int(n)
    return n


def calculate_triangle_area(vertices):
    '''berechnet den Flächeninhalt eines Dreiecks in O(1)'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    x1, y1 = vertices[0]
    x2, y2 = vertices[1]
    x3, y3 = vertices[2]

    area = 0.5 * abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)))
    return area


def calculate_polygon_area(polygon_vertices):
    '''Berechnet den Flächeninhalt eines Polygons'''
    '''Time Complexity: O(n^2) für n Eckpunkte des Polygons, Auxiliary Space: O(n) für n Eckpunkte des Polygons'''
    triangles = ear_clipping(polygon_vertices) # Zeitkomplexität O(n^2)
    area_num = 0
    for triangle in triangles:
        area_num += calculate_triangle_area(triangle)
    return area_num


def calculate_multiple_polygon_area(polygons):
    '''Berechnet den insgesamten Flächeninhalt'''
    '''Time Complexity: O(m*n^2) für m Polygons mit n Eckpunkten, Auxiliary Space: O(m*n) für m Polygone mit m Eckpunkten'''
    area = 0
    for polygon in polygons:
        for i, vertex in enumerate(polygon):
            if isinstance(vertex, tuple):
                polygon[i] = [vertex[0]/(10**decimal_precision), vertex[1]/(10**decimal_precision)]
        area += calculate_polygon_area(polygon) # Zeitkomplexität O(n^2)
    return area


def convex_or_reflex_vertex(vertex1, main_vertex, vertex2):
    '''Gibt an, ob der Innenwinkel eines Eckpunkts convex (<=180 Grad) oder reflex (> 180 Grad) ist'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    a_x, a_y = main_vertex
    b_x, b_y = vertex1
    c_x, c_y = vertex2

    if (a_x - b_x) * (c_y - a_y) - (c_x - a_x) * (a_y - b_y) > 0:
        return 'convex'
    else:
        return 'reflex'


def ear_clipping(old_polygon_vertices, tries=0):
    '''Unterteilt ein Polygon in Dreiecke'''
    '''Time Complexity: O(n^2) für n Eckpunkte des Polygons, da n Ecken entfernt werden müssen, wobei nach jedem Entfernen neu aktualisiert werden muss, 
       Auxiliary Space: O(n) für n Eckpunkte des Polygons'''
    if tries>1:
        raise Exception()
    try:
        polygon_vertices = deepcopy(old_polygon_vertices)
        triangles = []
        
        # Winkel <= 180°
        convex_vertices = []
        # Winkel > 180°
        reflex_vertices = []
        # convex + zusammen mit den Nachbarn wird ein Dreieck gebildet, in welchem keine anderen Punkte liegen
        ears = []
        
        for i in range(len(polygon_vertices)):
            # Polygon baut sich gegen den Uhrzeigersinn auf, bei einer Linksdrehung ist der Eckpunkt convex
            vertex = polygon_vertices[i]
            result = convex_or_reflex_vertex(polygon_vertices[i-1], vertex, polygon_vertices[(i+1) % len(polygon_vertices)])

            if result == 'convex':
                convex_vertices.append(vertex)
            elif result == 'reflex':
                reflex_vertices.append(vertex)
        
        # Herausfinden der ears aus den convex Eckpunkten
        for vertex in convex_vertices:
            i = polygon_vertices.index(vertex)
            triangle_vertices = [polygon_vertices[i-1], polygon_vertices[i], polygon_vertices[(i+1) % len(polygon_vertices)]]
            if no_point_in_triangle(triangle_vertices, polygon_vertices):
                ears.append(vertex)

        while len(polygon_vertices) > 3:
            # Entnehmen des erstmöglichen Dreiecks
            ear = ears.pop()
            i = polygon_vertices.index(ear)
            neighbor1 = polygon_vertices[i-1]
            neighbor2 = polygon_vertices[(i+1) % len(polygon_vertices)]
            neighbors = [neighbor1, neighbor2]
            triangles.append([ear, neighbor1, neighbor2])
            polygon_vertices.remove(ear)
            
            # die benachbarten Eckpunkte müssen neu kategorisiert werden
            for neighbor in neighbors:
                i = polygon_vertices.index(neighbor)
                
                # neuer Typ wird ermittelt
                neighbor_type = convex_or_reflex_vertex(polygon_vertices[i-1], neighbor, polygon_vertices[(i+1) % len(polygon_vertices)])
                
                if neighbor_type == 'convex':
                    # falls der Punkt vorher nicht convex war, wird er umgeschrieben
                    if neighbor not in convex_vertices:
                        reflex_vertices.remove(neighbor)
                        convex_vertices.append(neighbor)
                    # Überprüfung ob der Punkt ear ist
                    triangle_vertices = [polygon_vertices[i-1], neighbor, polygon_vertices[(i+1) % len(polygon_vertices)]]
                    # Punkt ist ein ear
                    if no_point_in_triangle(triangle_vertices, polygon_vertices):
                        # Punkt ist nicht schon bereits ear
                        if neighbor not in ears:
                            ears.append(neighbor)
                    # Punkt hat Status ear verloren
                    elif neighbor in ears:
                        ears.remove(neighbor)
                # falls der Punkt vorher nicht reflex war, wird er umgeschrieben
                elif neighbor_type == 'reflex' and neighbor not in reflex_vertices:
                    convex_vertices.remove(neighbor)
                    reflex_vertices.append(neighbor)

        triangles.append(polygon_vertices)
        return triangles
    
    except Exception:
        # Polygon ist in falscher Richtung aufgebaut, Konflikt bei der Betrachtung von Innen- und Außenwinkeln, Neuversuch
        polygon_vertices.reverse()
        return ear_clipping(polygon_vertices, tries=tries+1)
    

def area_settlement_approximation(polygon_vertices, circle_anchor, visualize=False):
    '''Ermittelt die Siedlungen, die in einen Kreis vom Radius 85 passen'''
    '''Time Complexity: O(n) für n Eckpunkte, Auxiliary Space: O(d^2) für d als maximale Distanz im Polygon, äquivalent zur Anzahl Siedlungen'''
    polygon_edges = create_edges(polygon_vertices) # Zeitkomplexität O(n) für n Eckpunkte des Polygons
    settlements = place_inner_settlements(circle_anchor) # Zeitkomplexität O(1)
    optimal_settlements = optimize_rotation(polygon_edges, settlements, circle_anchor, precision=0) # Zeitkomplexität O(n) für n Eckpunkte des Polygons
    optimal_settlements = remove_outside_settlements(polygon_edges, optimal_settlements) # Zeitkomplexität O(n) für n Eckpunkte des Polygons
    
    if visualize:
        visualize_polygon(polygon_vertices, circle_anchor=circle_anchor, settlements=optimal_settlements)
    
    return len(optimal_settlements)