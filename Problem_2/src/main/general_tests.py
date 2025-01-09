import unittest

from __main__ import *
from bin_piece_utils import *
from structure_utils import *

class Test(unittest.TestCase):
    def test_is_insertable_simple_true(self):
        combinations = {2:[2, 3,4], 3:[3, 2], 4:[4, 2]}
        bin = [[2],[3],[2]]
        cloth = [1, 2]
        result = is_insertable(bin, cloth, combinations)
        self.assertTrue(result)
    
    def test_is_insertable_simple_false(self):
        combinations = {2:[3,4], 3:[2], 4:[2]}
        bin = [[2],[3],[2]]
        cloth = [1, 4]
        result = is_insertable(bin, cloth, combinations)
        self.assertFalse(result)

    def test_insert_piece_empty_bin(self):
        piece = [1, 2]
        expected = [[2], [], []]
        result = insert_piece([[],[],[]], piece)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()