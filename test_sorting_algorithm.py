import unittest
from sorting_algorithm import sort

# test case for the algorithm
class TestSort(unittest.TestCase):
    def test_best(self):
        inp = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        ans = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        self.assertEqual(sort(inp), ans, 'Incorrectly sorted') 

    def test_worst(self):
        inp = {"NIN": 9, "ATE": 8, 'SVN': 7, 'SIX': 6, 'FIV': 5}
        ans = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        self.assertEqual(sort(inp), ans, 'Incorrectly sorted') 

    def test_average(self):
        inp = {'SVN': 7, 'FIV': 5, 'SIX': 6, 'NIN': 9, 'ATE': 8}
        ans = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        self.assertEqual(sort(inp), ans, 'Incorrectly sorted') 

if __name__ == '__main__':
    unittest.main()