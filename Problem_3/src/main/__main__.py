import time

from facility_grid_search import *
from polygon_utils import *
from visualizations import *
from settlement_positioning import *


def main():
    visualize = ask_for_visualization()
    polygon_vertices = read_file()
    
    # Starten der Laufzeitmessung
    start_time = time.time()

    # Visualisierung des Polygons
    if visualize:
        start = time.time()
        visualize_polygon(polygon_vertices)
        end = time.time()
        start_time += end - start
    
    # Zusätzliches Umformatieren der Eckpunkte in Seiten für leichtere Weiterverarbeitung
    polygon_edges = create_edges(polygon_vertices)
    
    # Ermitteln der optimalen Position des Gesundheitszentrums
    facility_anchor, time_in_visualization = get_facility_location(polygon_vertices, splits=30, depth_finish=3, depth_stop=2, visualize_beginning=visualize, force_area_calculation=False)  
    if time_in_visualization != None:
        start_time += time_in_visualization

    # Visualisierung des Gesundheitszentrums
    if visualize:
        start = time.time()
        visualize_polygon(polygon_vertices, circle_anchor=facility_anchor)
        end = time.time()
        start_time += end - start
    
    # Platzierung der Siedlungen
    settlements = place_settlements(facility_anchor, polygon_vertices, visualization=False)
    
    # Visualisierung der aufgestellten Siedlungen
    if visualize:
        start = time.time()
        visualize_polygon(polygon_vertices, settlements=settlements, circle_anchor=facility_anchor)
        end = time.time()
        start_time += end - start
    
    # Ermitteln der optimalen Rotation
    rotated_settlements = optimize_rotation(polygon_edges, settlements, facility_anchor, 3)
    # Entfernen außerhalb liegender Siedlungen
    correct_settlements = remove_outside_settlements(polygon_edges, rotated_settlements)
    
    # Stoppen der Laufzeitmessung
    end_time = time.time()

    # Visualisieren und Ausgeben der Lösung
    visualize_polygon(polygon_vertices, settlements=correct_settlements, circle_anchor=facility_anchor)
    print('Anzahl Siedlungen: ', len(correct_settlements))
    runtime = end_time - start_time
    print('Laufzeit: ', "{:.2f}".format(runtime), "s")
    

def ask_for_visualization():
    '''Ermöglicht dem Nutzer, zusätzliche Visualisierungen zu aktivieren'''
    while True:
        ans = input("Sollen zusätzliche Visualisierungen angezeigt werden? y/n\n")
        if ans=='y':
            return True
        if ans=='n':
            return False


def read_file():
    '''Liest das Polygon aus einer Datei heraus'''
    '''Time Complexity: O(n) für n Eckpunkte des Polygons, Auxiliary Space: O(n) für n Eckpunkte des Polygons'''
    while True:
        try:
            answer = input("Geben Sie einen Dateipfad ein: ")
            # bei 2,3 gibt es verbesserungspotenzial
            answer = [line.split() for line in open(answer, 'r')]
            answer = [[float(j) for j in i] for i in answer]
            vertices = answer[1:int(answer[0][0])+1]
                
            return vertices
        except FileNotFoundError:
            pass
        except OSError:
            pass
        print("Die Datei existiert nicht. Bitte versuchen Sie es erneut")


if __name__ == '__main__':
    main()