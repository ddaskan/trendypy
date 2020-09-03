'''
Utility functions for the package.
'''
import numpy as np

def scale_01(x):
    '''Scales array to 0-1.

    Args:
        x (iter): 1d array of float

    Returns:
        np.array: scaled 1d array

    Example:
        >>> scale_01([1, 2, 3, 5]).tolist()
        [0.0, 0.25, 0.5, 1.0]

    '''
    arr_min = min(x)
    x = np.array(x) - float(arr_min)
    arr_max = max(x)
    return x / float(arr_max)

def abs_distance(x, y):
    '''Returns absolute distance.

    Args:
        x (float): input 1
        y (float): input 2

    Returns:
        float: \|x-y\|

    Example:
        >>> abs_distance(5, 7)
        2.0
        >>> abs_distance(4, 1)
        3.0

    '''
    return float(abs(x - y))

def euclidean_distance(x, y):
    '''Returns Euclidean distance.

    Args:
        x (float or iter): input 1
        y (float or iter): input 2

    Returns:
        float: Euclidean distance

    References:
        https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html

    Examples:
        >>> x, y = 1, 2
        >>> euclidean_distance(x, y)
        1.0
        >>> x, y = [1, 2], [4, 6]
        >>> euclidean_distance(x, y)
        5.0

    '''
    return np.linalg.norm(np.array(x) - np.array(y))

