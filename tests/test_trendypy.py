import unittest
import sys
sys.path.append('../')
sys.path.append('../trendypy/')
from trendypy.trendy import Trendy

class TestTrendy(unittest.TestCase):

    def test___init__(self):
        
        self.assertRaises(TypeError, Trendy)
        self.assertRaises(TypeError, Trendy, *[None, None])
        self.assertRaises(TypeError, Trendy, **{'n':5, 'algorithm':'error'})
        self.assertRaises(TypeError, Trendy, **{'cluster_names':2})

        self.assertRaises(ValueError, Trendy, **{'n':'1'})
        self.assertRaises(ValueError, Trendy, **{'n':1})
        self.assertRaises(ValueError, Trendy, **{'cluster_names':[1]})
        self.assertRaises(ValueError, Trendy, **{'cluster_names':[1, 1]})

        trendy = Trendy(n=3)
        self.assertEqual(trendy.n, 3)
        self.assertListEqual(trendy.cluster_names, [1, 2, 3])
        self.assertTrue(callable(trendy.dist_func))

        trendy = Trendy(cluster_names=['a', 'b', 'c'])
        self.assertEqual(trendy.n, 3)
        self.assertListEqual(trendy.cluster_names, ['a', 'b', 'c'])
        self.assertTrue(callable(trendy.dist_func))

        test_func = lambda x,y:abs(x-y)
        trendy = Trendy(n=3, algorithm=test_func)
        self.assertTrue(callable(trendy.dist_func))
        self.assertEqual(
        	trendy.dist_func.__code__.co_code, 
        	test_func.__code__.co_code)


if __name__ == '__main__':
    unittest.main()