'''
Algorithms for the package.
'''
import sys
sys.path.append('../')
import numpy as np
from fastdtw import fastdtw
from trendypy import utils

def dtw_distance(x, y, d=utils.euclidean_distance, scaled=False):
    '''Returns the distance of two arrays with dynamic time warping method.

    Args:
        x (iter): input array 1
        y (iter): input array 2
        d (func): distance function, default is euclidean
        scaled (bool): should arrays be scaled (i.e. 0-1) before calculation

    Returns:
        float: distance, 0.0 means arrays are exactly same, upper limit is\
            positive infinity

    References:
        https://en.wikipedia.org/wiki/Dynamic_time_warping

    Examples:
        >>> dtw_distance([1, 2, 3, 4], [1, 2, 3, 4])
        0.0
        >>> dtw_distance([1, 2, 3, 4], [0, 0, 0])
        10.0
        >>> dtw_distance([1, 2, 3, 4], [0, 2, 0, 4])
        4.0
        >>> dtw_distance([1, 2, 3, 4], [10, 20, 30, 40])
        90.0
        >>> dtw_distance([1, 2, 3, 4], [10, 20, 30, 40], scaled=True)
        0.0

    '''
    if scaled:
        x = utils.scale_01(x)
        y = utils.scale_01(y)
    n = len(x) + 1
    m = len(y) + 1
    DTW = np.zeros((n, m))
    DTW[:, 0] = float('Inf')
    DTW[0, :] = float('Inf')
    DTW[0, 0] = 0
    
    for i in range(1, n):
        for j in range(1, m):
            cost = d(x[i-1], y[j-1])
            DTW[i, j] = cost + min(DTW[i-1, j], DTW[i, j-1], DTW[i-1, j-1])
            
    return DTW[n-1, m-1]

def fastdtw_distance(x, y, d=utils.euclidean_distance):
    '''Dynamic Time Warping (DTW) algorithm with an O(N) time and memory 
    complexity.

    Args:
        x (iter): input array 1
        y (iter): input array 2
        d (func): distance function, default is euclidean

    Returns:
        float: distance, 0.0 means arrays are exactly same, upper limit is\
            positive infinity

    References:
        https://pypi.org/project/fastdtw/

    Examples:
        >>> fastdtw_distance([1, 2, 3, 4], [1, 2, 3, 4])
        0.0
        >>> fastdtw_distance([1, 2, 3, 4], [0, 0, 0])
        10.0
        >>> fastdtw_distance([1, 2, 3, 4], [0, 2, 0, 4])
        4.0
        >>> fastdtw_distance([1, 2, 3, 4], [10, 20, 30, 40])
        90.0

    '''
    return fastdtw(x, y, dist=d)[0]

def levenshtein_distance(x, y):
    """Levenshtein distance for string similarity.

    Args:
        x (str): input string 1
        y (str): input string 2

    Returns:
        int: distance, 0 means strings are exactly same, upper limit is\
            positive infinity

    References:
        https://en.wikipedia.org/wiki/Levenshtein_distance

    Examples:
        >>> levenshtein_distance('Apple', 'Apple')
        0
        >>> levenshtein_distance('Apple', 'apple')
        1
        >>> levenshtein_distance('Apple Inc.', 'apple inc')
        3

    """
    m, n = len(x), len(y)
    v0 = list(range(n + 1))
    v1 = [None] * (n + 1)

    for i in range(m):
        v1[0] = i + 1

        for j in range(n):
            deletion_cost = v0[j + 1] + 1
            insertion_cost = v1[j] + 1
            if x[i] == y[j]:
                substitution_cost = v0[j]
            else:
                substitution_cost = v0[j] + 1

            v1[j + 1] = min(deletion_cost, insertion_cost, substitution_cost)

        v0, v1 = v1, v0

    return v0[n]
