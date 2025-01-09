import unittest

from __main__ import *
from circle_area import *
from facility_grid_search import *
from polygon_utils import *
from visualizations import *


class Test(unittest.TestCase):
    '''4.2.1 Rotation der Siedlungen'''
    def test_rotation1(self):
        polygon_vertices = [[-1,-200],[1,-200],[1,200],[-1,200]]
        rotation(polygon_vertices)
    def test_rotation2(self):
        polygon_vertices = [[-49,-200],[-51,-200],[49,200],[51,200]]
        rotation(polygon_vertices)
    
    '''4.2.2 Position des Gesundheitszentrums'''
    def test_facility_location1(self):
        polygon_vertices = [[-80,-80],[80,-80],[80,80],[10,80],[10,55],[55,55],[55,-55],[10.0000001,-55],[10.0000001,10],[9.9999999,10],[9.9999999,-55],[-55,-55],[-55,55],[-10,55],[-10,80],[-80,80]]
        facility_location(polygon_vertices, splits=20, depth_finish=5, depth_stop=3, visualize=False)
    def test_facility_location2(self): 
        polygon_vertices = [[-80,-80],[-5,-80],[-5,-500],[5,-500],[5,-80],[80,-80],[80,-5],[500,-5],[500,5],[80,5],[80,80],[10,80],[10,55],[55,55],[55,-55],[0.01,-55],[0.01,10],[-0.01,10],[-0.01,-55],[-55,-55],[-55,55],[-10,55],[-10,80],[-80,80]]
        facility_location(polygon_vertices, splits=20, depth_finish=5, depth_stop=3, visualize_beginning=False)
    def test_facility_location3(self): 
        polygon_vertices = [[-80,-80],[-5,-80],[-5,-500],[5,-500],[5,-80],[80,-80],[80,-5],[500,-5],[500,5],[80,5],[80,80],[10,80],[10,55],[55,55],[55,-55],[0.01,-55],[0.01,10],[-0.01,10],[-0.01,-55],[-55,-55],[-55,55],[-10,55],[-10,80],[-80,80]]
        facility_location(polygon_vertices, splits=70, depth_finish=4, depth_stop=4, visualize_beginning=False)
    def test_facility_location4(self):
        polygon_vertices = [[-80,-80],[80,-80],[80,80],[10,80],[10,55],[55,55],[55,-55],[10.0000001,-55],[10.0000001,10],[9.9999999,10],[9.9999999,-55],[-55,-55],[-55,55],[-10,55],[-10,80],[-80,80]]
        facility_location(polygon_vertices, splits=70, depth_finish=4, depth_stop=4, visualize=False)

    '''4.2.3 Ermittlung der Schnittfläche'''
    def test_get_circle_area(self):
        polygon_vertices = [[0,-100],[0,100],[50,50],[100,100],[100,-100]]
        get_circle_area(polygon_vertices, (0,0))
    
    def test_get_circle_area1(self):
        polygon_vertices = [[0,-50],[0,50],[50,50],[50,-50]]
        circle_area(polygon_vertices, (0,0))

    def test_get_circle_area2(self):
        polygon_vertices = [[110,-100],[0,-100],[0,-70],[100,-70],[30,-60],[90,-50],[90,-48],[30,-40],[100,-30]]
        circle_area(polygon_vertices, (0,0))
    def test_get_circle_area3(self):
        polygon_vertices =[[-40, -120], [30, -120], [20, -60], [100, -50], [10, -10], [100, 15], [100, 30], [0, 0], [0, -100], [-20, -100], [-20, 10], [75, 100], [70, 110], [-45, 100]]
        circle_area(polygon_vertices, (0,0))
    
    def test_get_circle_area4(self):
        polygon_vertices = [[27.59776253870874,104.0831982696689],[-102.92440236325785,79.8331785611068],[-15.203738771696887,-100.52723206892206],[-10.203738771696887,-90.52723206892206],[-91.51262838275804,76.26699919220061],[9.053629820396544,-53.541929835984725]]
        circle_area(polygon_vertices, (0,0))
    
    def test_get_circle_area5(self):
        polygon_vertices = [[0,-100],[100,-100],[100,100],[50,50]]
        circle_area(polygon_vertices, (0,0))
    
    def test_get_circle_area6(self):
        polygon_vertices = [[0.000000, 20.000000], [0.000000, 100.000000], [20.000000, 20.000000], [20.000000, 100.000000], [40.000000, 20.000000], [40.000000, 100.000000], [60.000000, 20.000000], [60.000000, 100.000000], [80.000000, 20.000000], [80.000000, 100.000000], [100.000000, 20.000000], 
                            [100.000000, 100.000000], [120.000000, 20.000000], [120.000000, 100.000000], [140.000000, 20.000000], [140.000000, 100.000000], [160.000000, 20.000000], [160.000000, 100.000000], [180.000000, 20.000000], [180.000000, 100.000000], [200.000000, -20.000000], [0.000000, -20.000000]]
        circle_anchor = (100,50)
        get_circle_area(polygon_vertices, circle_anchor)
        
    
    def test_get_circle_area7(self):
        polygon_vertices = [[20.0, 0.0], [100.0, 0.0], [100.0, 90.0], [102.0, 90.0], [102.0, 0.0], [108.0, 0.0], [108.0, 90.0], [110.0, 90.0], [110.0, 0.0], [190.0, 0.0], [190.0, 100.0], [106.0, 100.0], [106.0, 10.0], [104.0, 10.0], [104.0, 100.0], [20.0, 100.0]]
        circle_anchor = (77.375, 21.25)
        get_circle_area(polygon_vertices, circle_anchor)


def rotation(polygon_vertices):
    circle_anchor = (0,0)
    settlements = place_settlements(circle_anchor, polygon_vertices)
    visualize_polygon(polygon_vertices, circle_anchor=circle_anchor, settlements=settlements)
    polygon_edges = create_edges(polygon_vertices)
    print(f"\nAnzahl Siedlungen vor der Rotation: {len(remove_outside_settlements(polygon_edges, settlements))}")
    rotated_settlements = optimize_rotation(polygon_edges, settlements, circle_anchor)
    visualize_polygon(polygon_vertices, circle_anchor=circle_anchor, settlements=rotated_settlements)
    correct_settlements = remove_outside_settlements(polygon_edges, rotated_settlements)
    visualize_polygon(polygon_vertices, circle_anchor=circle_anchor, settlements=correct_settlements)
    print(f"Anzahl Siedlungen nach der Rotation: {len(correct_settlements)}")


def facility_location(polygon_vertices, splits=10, depth_finish=5, depth_stop=3, force_area_calculation=False, visualize=False, visualize_beginning=False):
    visualize_polygon(polygon_vertices)
    start = time.time()
    circle_anchor, _ = get_facility_location(polygon_vertices, splits=splits, depth_finish=depth_finish, depth_stop=depth_stop, force_area_calculation=force_area_calculation, visualize=visualize, visualize_beginning=visualize_beginning)
    end = time.time()
    visualize_polygon(polygon_vertices, circle_anchor=circle_anchor)
    print("\nruntime: ", "{:.2f}".format(end-start), "s")

def circle_area(polygon_vertices, circle_anchor):
    visualize_polygon(polygon_vertices, circle_anchor)
    result = get_circle_area(polygon_vertices, circle_anchor, visualize=False, visualize_result=True)
    print("\nDie Fläche beträgt ", "{:.2f}".format(result), "km^2")
        
if __name__ == '__main__':
    unittest.main()