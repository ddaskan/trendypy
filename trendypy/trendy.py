from itertools import combinations
import pandas as pd
import algos

class Trendy():
    '''

    Notes:
        Scaling and missing values need to be handled externally.

    Args:
        n (int or None): Expected cluster count.
        cluster_names (iter or None): Unique expected cluster names, if None 
            and integer sequence is assigned based on `n`.
        algorithm (callable): Algorithm to calculate the difference. Default 
            is `DTW with Euclidean <#algos.dtw_distance>`_.

    '''
    clusters = None
    centers = None

    def __init__(self, n=None, cluster_names=None, algorithm=algos.dtw_distance):

        if (n is None and cluster_names is None) or \
            (n is not None and cluster_names is not None):
            raise TypeError('only one of `n`, `cluster_names` must be given')
        
        if n:
            self.n = int(n)
            self.cluster_names = list(range(1, self.n+1))
        elif cluster_names:
            self.cluster_names = list(cluster_names)
            self.n = len(self.cluster_names)
            if len(set(self.cluster_names)) != self.n:
                raise ValueError('cluster names must be unique')

        if not self.n >= 2:
            raise ValueError('cluster count must be >= 2')

        if not callable(algorithm):
            raise TypeError('distance `algorithm` must be a callable')

        self.dist_func = algorithm

    def fit(self, series_dict):
        raise NotImplementedError()

    def assign(self, series, save=False):
        raise NotImplementedError()


        
