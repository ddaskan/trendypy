import sys
import unittest
import doctest
sys.path.append('../')
from trendypy import trendy
from trendypy import algos
from trendypy import utils

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(trendy))
    tests.addTests(doctest.DocTestSuite(algos))
    tests.addTests(doctest.DocTestSuite(utils))
    return tests

if __name__ == '__main__':
    unittest.main()
