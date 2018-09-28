import numpy as np
import pandas as pd
from itertools import combinations
import time

def dtw_distance(x, y, d=lambda x,y: abs(x-y), scaled=False, fill=False):
	"""Finds the distance of two arrays by dynamic time warping method
	source: https://en.wikipedia.org/wiki/Dynamic_time_warping
	
	Dependencies:
		import numpy as np
	Args:
		x, y: arrays
		d: distance function, default is absolute difference
		scaled: boolean, should arrays be scaled before calculation
		fill: boolean, should NA values be filled with 0
	returns:
		distance as float, 0.0 means series are exactly same, upper limit is infinite
	"""
	if fill:
		x = np.nan_to_num(x)
		y = np.nan_to_num(y)
	if scaled:
		x = array_scaler(x)
		y = array_scaler(y)
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
	
def array_scaler(x):
	"""Scales array to 0-1
	
	Dependencies:
		import numpy as np
	Args:
		x: mutable iterable array of float
	returns:
		scaled x
	"""
	arr_min = min(x)
	x = np.array(x) - float(arr_min)
	arr_max = max(x)
	x = x/float(arr_max)
	return x

    
class TrendCluster():
    def __init__(self):
        self.clusters = None
        self.centers = None
        self.scale = None
        
    def fit(self, series, n=2, scale=True):
        '''
        Work-flow
        1. Create your all cluster combinations. k is for cluster count and n is for number of series. The number of items returned should be n! / k! / (n-k)!. These would be something like potential centers.
        2. For each series, calculate distances for each center in each cluster groups and assign it to the minimum one.
        3. For each cluster groups, calculate total distance within individual clusters.
        4. Choose the minimum.
        
        Args:
            series: dict, keys can be anything, values are time series as list, assumes no nulls
            n: int, cluster size
            scale: bool, if scale needed
        '''
        assert isinstance(series, dict) and isinstance(n, int) and isinstance(scale, bool), 'wrong argument type'
        assert n < len(series.keys()), 'n is too big'
        assert len(set([len(s) for s in series.values()])) == 1, 'series length not same'
        
        self.scale = scale
        
        combs = combinations(series.keys(), n)
        combs = [[c, -1] for c in combs]
  
        series_keys = pd.Series(series.keys())
        dtw_matrix = pd.DataFrame(series_keys.apply(lambda x: series_keys.apply(lambda y: dtw_distance(series[x], series[y], scaled=scale))))
        dtw_matrix.columns, dtw_matrix.index = series_keys, series_keys
        for c in combs:
            c[1] = dtw_matrix.loc[c[0], :].min(axis=0).sum()
         
        combs.sort(key=lambda x: x[1])
        self.centers = {c:series[c] for c in combs[0][0]}
        self.clusters = {c:[] for c in self.centers.keys()}

        for k, _ in series.items():
            tmp = [[c, dtw_matrix.loc[k, c]] for c in self.centers.keys()]
            tmp.sort(key=lambda x: x[1])
            cluster = tmp[0][0]
            self.clusters[cluster].append(k)

        return None
        
    def assign(self, serie, save=False):
        '''
        Assigns the serie to appropriate cluster
        
        Args:
            serie, dict: 1 element dict
            save, bool: if new serie is stored to clusters
            
        Return:
            str, assigned cluster key
        '''
        assert isinstance(serie, dict) and isinstance(save, bool), 'wrong argument type'
        assert len(serie) == 1, 'serie\'s length is not exactly 1'
        
        tmp = [[c, dtw_distance(serie.values()[0], self.centers[c], scaled=self.scale)] for c in self.centers.keys()]
        tmp.sort(key=lambda x: x[1])
        cluster = tmp[0][0]
        if save:
            self.clusters[cluster].append(serie.keys()[0])
        
        return cluster
    
    
