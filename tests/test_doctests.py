import sys
import unittest
import doctest
sys.path.append('../')
sys.path.append('../trendypy/')
import trendy
import algos
import utils

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(trendy))
    tests.addTests(doctest.DocTestSuite(algos))
    tests.addTests(doctest.DocTestSuite(utils))
    return tests

if __name__ == '__main__':
    unittest.main()
