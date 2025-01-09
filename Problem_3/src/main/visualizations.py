import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

from polygon_utils import *


def visualize_polygon(polygon_vertices, circle_anchor = None, draw_line = None, settlements = [], triangles = [], title = ''):
    '''Erstellt Visualisierungen mit dem Polygon als Schwerpunkt'''
    # Polygon wird gezeichnet
    x, y = zip(*(polygon_vertices + [polygon_vertices[0]]))
    ax = plt.gca()
    ax.plot(x, y, color='blue')
    ax.set_aspect('equal')
    
    '''Folgende Funktionalitäten sind optional und unabhängig voneinander durchführbar'''
    # Kreis wird gezeichnet
    if circle_anchor != None:
        circle = plt.Circle((circle_anchor[0], circle_anchor[1]), 85, color='g', fill=False)
        ax.add_patch(circle)

    # Genutzt, um die größte Distanz zwischen dem Gesundheitszentrum und einem Punkt des Polygons zu visualisieren
    if draw_line != None:
        point1, point2 = draw_line
        x = [point1[0], point2[0]]
        y = [point1[1], point2[1]]
        ax.plot(x,y, color='g', linestyle = 'dotted')
    
    # Hinzufügen aller Siedlungen als Punkte
    if len(settlements) > 0:
        for settlement in settlements:
            pos_x, pos_y = settlement.pos_x, settlement.pos_y
            ax.plot(pos_x, pos_y, 'g.')
    
    # Dreiecke werden gezeichnet, genutzt, um Triangulation eines Polygons zu visualisieren
    if len(triangles) > 0:
        for triangle in triangles:
            x, y = zip(*(triangle + [triangle[0]]))
            ax.plot(x, y, color='blue')
    
    # Titel wird hinzugefügt
    if isinstance(title, str) and len(title) > 1:
        plt.title(title)
    
    plt.show()


def visualize_grid(polygon_vertices, vertices, point_list, areas=[]):
    '''Erstellt Visualisierungen mit Grid Search als Schwerpunkt'''
    # Rechteckige Grenze wird gezeichnet
    x, y = zip(*(polygon_vertices + [polygon_vertices[0]]))
    if len(areas) == 0:
        plt.plot(x, y, color='blue')
    else:
        plt.plot(x, y, color='purple')

    # Polygon wird gezeichnet
    x, y = zip(*(vertices + [vertices[0]]))
    plt.plot(x, y, color='green')

    # Untersuchungspunkte werden als Punkte hinzugefügt
    x, y = zip(*(point_list))
    if len(areas) == 0:
        plt.scatter(x, y, color='red')
    else:
        # Optional kann eine wertabhängige Färbung vorgenommen werden, was in einer Heatmap resultiert
        try:
            colors = [(0, 'blue'), (0.5, 'green'), (0.8, 'yellow'), (1, 'red')]
            cmap = LinearSegmentedColormap.from_list('custom', colors)
            sns.scatterplot(x=x, y=y, hue=areas, palette=cmap)
        # Ignorieren der Färbung beim Scheitern
        except Exception:
            plt.scatter(x, y, color='red')

    ax = plt.gca()
    ax.set_aspect('equal')
    plt.show()


def visualize_circle(all_angles = [], correct_test_points = [], polygon_vertices = [], final_angles = [], circle_anchor = (0,0)):
    '''Erstellt Visualisierungen mit einem Kreis, genutzt, um die Schnittfläche zu berechnen, als Schwerpunkt'''
    # Der Kreis wird gezeichnet 
    circle = plt.Circle(circle_anchor, 85, color='g', fill=False)
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.add_patch(circle)
    
    '''Folgende Funktionalitäten sind optional und unabhängig voneinander durchführbar'''

    if len(all_angles) > 0:
        points_x = []
        points_y = []
        test_points_x = []
        test_points_y = []

        for angle_tuple in all_angles:
            x1, y1 = rotate_point((85+circle_anchor[0],circle_anchor[1]),circle_anchor,angle_tuple[0])
            x2, y2 = rotate_point((85+circle_anchor[0],circle_anchor[1]),circle_anchor,angle_tuple[1])
            x3, y3 = rotate_point((85+circle_anchor[0],circle_anchor[1]),circle_anchor,angle_tuple[2]) 
            points_x.append(x1)
            points_x.append(x2)
            points_y.append(y1)
            points_y.append(y2)
            test_points_x.append(x3)
            test_points_y.append(y3)
        
        ax.scatter(points_x, points_y, color='blue')
        ax.scatter(test_points_x, test_points_y, color='red')

    if len(final_angles) > 0:
        points_x = []
        points_y = []
        for angle in final_angles:
            x, y = rotate_point((85+circle_anchor[0],circle_anchor[1]),circle_anchor,angle)
            points_x.append(x)
            points_y.append(y)
        ax.scatter(points_x, points_y, color='blue')

    # Im Polygon liegende Testpunkte werden farbig markiert
    if len(correct_test_points) > 0:
        x, y = zip(*correct_test_points)
        ax.scatter(x, y, color='green')
    
    # Polygon wird gezeichnet
    if len(polygon_vertices) > 0:
        x, y = zip(*(polygon_vertices + [polygon_vertices[0]]))
        ax.plot(x, y, color='green')
    
    plt.show()