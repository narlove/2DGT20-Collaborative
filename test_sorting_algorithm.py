import unittest
from sorting_algorithm import sort

# test case for the algorithm
# doesnt actually test sequence which defeats the whole purpose of this code
class TestSort(unittest.TestCase):
    def test_best(self):
        inp = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        ans = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        self.assertDictEqual(sort(inp), ans, 'Incorrectly sorted')

    def test_worst(self):
        inp = {"NIN": 9, "ATE": 8, 'SVN': 7, 'SIX': 6, 'FIV': 5}
        ans = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        self.assertDictEqual(sort(inp), ans, 'Incorrectly sorted')

    def test_average(self):
        inp = {'SVN': 7, 'FIV': 5, 'SIX': 6, 'NIN': 9, 'ATE': 8}
        ans = {'FIV': 5, 'SIX': 6, 'SVN': 7, "ATE": 8, "NIN": 9}
        self.assertDictEqual(sort(inp), ans, 'Incorrectly sorted')

    def test_duplicate(self):
        inp = {'SVN': 7, 'FIV': 5, 'SIX': 9, 'NIN': 9, 'ATE': 8}
        ans = {'FIV': 5, 'SVN': 7, "ATE": 8, 'SIX': 9, "NIN": 9}
        self.assertDictEqual(sort(inp), ans, 'Incorrectly sorted')

    def test_required(self):
        inp = {'LON': 9, 'FIX': 6, 'SAS': 7, 'EKK': 5, 'MCD': 3}
        ans = {'LON': 9, 'SAS': 7, 'FIX': 6, 'EKK': 5, 'MCD': 3}
        self.assertDictEqual(sort(inp), ans, 'Incorrectly sorted')

if __name__ == '__main__':
    unittest.main()