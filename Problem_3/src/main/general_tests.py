import unittest
import matplotlib.pyplot as plt

from __main__ import *
from circle_area import *
from facility_grid_search import *
from polygon_utils import *
from visualizations import *


class Test(unittest.TestCase):
    '''do_lines_intersect'''
    def test_do_lines_intersect_optimal_case(self):
        point = (25, 50)
        line = [[0,0],[100,100]]
        result = do_lines_intersect(point, line)
        self.assertTrue(result)
    def test_do_lines_intersect_possible_zero_division(self):
        point = (0, 50)
        line = [[0,0],[0,100]]
        result = do_lines_intersect(point, line)
        self.assertFalse(result)
    def test_do_lines_intersect_point_above_line(self):
        point = (50, 150)
        line = [[0,0],[100,100]]
        result = do_lines_intersect(point, line)
        self.assertFalse(result)
    def test_do_lines_intersect_point_behind_line(self):
        point = (75, 25)
        line = [[0,0],[100,100]]
        result = do_lines_intersect(point, line)
        self.assertFalse(result)
    def test_do_lines_intersect_point_behind_line_negative(self):
        point = (-1, 50)
        line = [[0,0],[-100,100]]
        result = do_lines_intersect(point, line)
        self.assertFalse(result)

    '''is_point_in_polygon'''
    # Für zusätzliche Genauigkeit wird nicht nur das Resultat, sondern die exakte Anzahl geschnittener Seiten überprüft
    def test_is_point_in_polygon_simple_1_cross(self):
        point = (150,50)
        edges = [[[0.0, 0.0], [200.0, 0.0]], [[200.0, 0.0], [200.0, 250.0]], [[200.0, 250.0], [150.0, 100.0]], [[150.0, 100.0], [0.0, 0.0]]]
        edges_crossed = 0
        for edge in edges:
            if do_lines_intersect(point, edge):
                edges_crossed += 1
        self.assertEqual(edges_crossed, 1)
    def test_is_point_in_polygon_3_crosses(self):
        point = (50,50)
        vertices = [[0,0],[0,100],[100,100],[100,25],[200,25],[200,100],[300,100],[300,0]]
        edges = create_edges(vertices)
        edges_crossed = 0
        for edge in edges:
            if do_lines_intersect(point, edge):
                edges_crossed += 1
        self.assertEqual(edges_crossed, 3)
    
    '''rotate_point'''
    def test_rotate_point_basic(self):
        point = (50,0)
        angle = math.pi/2
        expected_x, expected_y = (0,50)
        result_x, result_y = rotate_point(point, (0,0), angle)
        self.assertTrue(abs(result_x - expected_x) < 0.000001 and abs(result_y - expected_y) < 0.000001)
    def test_rotate_point_offset(self):
        point = (50,0)
        angle = math.pi/2
        expected_x, expected_y = (50,50)
        result_x, result_y = rotate_point(point, (25,25), angle)
        self.assertTrue(abs(result_x - expected_x) < 0.000001 and abs(result_y - expected_y) < 0.000001)

    '''get_circle_intersection_points'''
    def test_get_circle_intersection_points(self):
        circle_anchor = (0,0)
        polygon_vertices = [[-100, 0],[100,0],[100,200],[-100,200]]
        result, _, _, _  = get_circle_intersection_points(polygon_vertices, circle_anchor)
        self.assertEqual(result, [(-850000000,0),(850000000,0)])
    def test_get_circle_intersection_points2(self):
        circle_anchor = (0,0)
        polygon_vertices = [[0, -100],[0,100],[100,100],[100,-100]]
        result, _, _, _ = get_circle_intersection_points(polygon_vertices, circle_anchor)
        self.assertEqual(result, [(0,-850000000),(0,850000000)])

    '''angle_of_point'''
    def test_angle_of_point0(self):
        anchor = (0,0)
        point = (85, 0)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, 0)
    def test_angle_of_point90(self):
        anchor = (0,0)
        point = (0, 85)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi/2)
    def test_angle_of_point180(self):
        anchor = (0,0)
        point = (-85, 0)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi)
    def test_angle_of_point270(self):
        anchor = (0,0)
        point = (0, -85)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi/2*3)
    def test_angle_of_point45(self):
        anchor = (0,0)
        point = (0, 85)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi/2)
    def test_angle_of_point45(self):
        anchor = (0,0)
        point = (60, 60)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi/4)
    def test_angle_of_point135(self):
        anchor = (0,0)
        point = (-60, 60)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi/4*3)
    def test_angle_of_point225(self):
        anchor = (0,0)
        point = (-60, -60)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi/4*5)
    def test_angle_of_point315(self):
        anchor = (0,0)
        point = (60, -60)
        result = angle_of_point(anchor, point)
        self.assertEqual(result, math.pi/4*7)

    
if __name__ == '__main__':
    unittest.main()