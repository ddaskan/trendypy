import unittest
import sys
sys.path.append('../')
sys.path.append('../trendypy/')
from trendypy.trendy import Trendy
from trendypy.algos import levenshtein_distance

class TestTrendy(unittest.TestCase):

    def test___init__(self):
        self.assertRaises(TypeError, Trendy)
        self.assertRaises(TypeError, Trendy, *[None])
        self.assertRaises(
                TypeError, 
                Trendy, 
                **{'n_clusters':5, 'algorithm':'error'})
        self.assertRaises(ValueError, Trendy, **{'n_clusters':'1'})
        self.assertRaises(ValueError, Trendy, **{'n_clusters':1})

        trendy = Trendy(n_clusters=3)
        self.assertEqual(trendy.n_clusters, 3)
        self.assertTrue(callable(trendy.dist_func))

        test_func = lambda x,y:abs(x-y)
        trendy = Trendy(n_clusters=3, algorithm=test_func)
        self.assertTrue(callable(trendy.dist_func))
        self.assertEqual(
        	trendy.dist_func.__code__.co_code, 
        	test_func.__code__.co_code)

    def test_fit(self):
        a = [0.8, 2, 3, 4, 5]
        b = [1, 1.9, 2.5, 4.4, 5.1]
        c = [6.2, 4, 4, 2, 0]
        d = [7, 6, 5, 4, 3, 2, 1]

        trendy = Trendy(6)
        self.assertRaises(ValueError, trendy.fit, *[[a, b, c, d]])

        trendy = Trendy(2)
        trendy.fit([a, b, c, d])
        self.assertListEqual(trendy.labels_, [0, 0, 1, 1])

        e = [3, 4, 3, 2, 5, 5.5]

        trendy = Trendy(3)
        trendy.fit([a, b, c, d, e])
        self.assertListEqual(trendy.labels_, [0, 0, 1, 1, 2])

        trendy = Trendy(5)
        trendy.fit([a, b, c, d, e])
        self.assertListEqual(trendy.labels_, [0, 1, 2, 3, 4])
        self.assertListEqual(trendy.cluster_centers_, [a, b, c, d, e])

    def test_predict(self):
        a = [0.8, 2, 3, 4, 5]
        b = [1, 1.9, 2.5, 4.4, 5.1]
        c = [6.2, 4, 4, 2, 0]
        d = [7, 6, 5, 4, 3, 2, 1]
        trendy = Trendy(2)
        trendy.fit([a, b, c, d])

        preds = trendy.predict([[0.9, 2, 2.9, 3.8, 5]])
        self.assertEqual(preds, [0])

        preds = trendy.predict([
            [0.9, 2, 2.9, 3.8, 5],
            [6.4, 4.4, 3.9, 3],
            [6, 3.5, 3.9, 3, 1.5]])
        self.assertEqual(preds, [0, 1, 1])

    def test_string_clustering(self):
        company_names = [
            'apple inc', 
            'Apple Inc.', 
            'Microsoft Corporation', 
            'Microsft Corp.']
        trendy = Trendy(n_clusters=2, algorithm=levenshtein_distance)
        trendy.fit(company_names)
        self.assertEqual(trendy.labels_, [0, 0, 1, 1])
        self.assertEqual(trendy.predict(['Apple']), [0])

if __name__ == '__main__':
    unittest.main()
