'''
Algorithms for the package.
'''
import numpy as np
import utils

def dtw_distance(x, y, d=utils.distance_euclidean, scaled=False):
    '''Returns the distance of two arrays with dynamic time warping method.

    Args:
        x (iter): input array 1
        y (iter): input array 2
        d (func): distance function, default is euclidean
        scaled (bool): should arrays be scaled (i.e. 0-1) before calculation

    Returns:
        float: distance, 0.0 means arrays are exactly same, upper limit is 
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
