from itertools import combinations
import pandas as pd
import algos

class Trendy():
    '''

    Notes:
        Scaling and missing values need to be handled externally.

    Args:
        n_clusters (int): The number of clusters to form.
        algorithm (callable): Algorithm to calculate the difference. Default 
            is `DTW with Euclidean <#algos.dtw_distance>`_.

    '''
    labels_ = None
    cluster_centers_ = None

    def __init__(self, n_clusters, algorithm=algos.dtw_distance):
        
        self.n_clusters = int(n_clusters)
        if not self.n_clusters >= 2:
            raise ValueError('cluster count must be >= 2')

        self.dist_func = algorithm
        if not callable(self.dist_func):
            raise TypeError('distance `algorithm` must be a callable')

    def fit(self, X):
        '''Compute clustering based on given distance algorithm.

        Args:
            X (array of arrays): Training instances to cluster.

        Example:
            >>> a = [1, 2, 3, 4, 5]
            >>> b = [1, 2.1, 2.9, 4.4, 5.1]
            >>> c = [6.2, 5, 4, 3, 2]
            >>> d = [7, 6, 5, 4, 3, 2, 1]
            >>> trendy = Trendy(2)
            >>> trendy.fit([a, b, c, d])
            >>> print(trendy.labels_)
            [0, 0, 1, 1]

        '''
        X_len = len(X)
        if X_len < self.n_clusters:
            raise ValueError('length of `X` < `n_clusters`')

        X_idx = pd.Series(range(X_len))
        combs = combinations(X_idx, self.n_clusters)
        combs = [[c, -1] for c in combs]

        d_matrix = pd.DataFrame(
            X_idx.apply(
                lambda x: X_idx.apply(
                    lambda y: self.dist_func(X[x], X[y]))))
        d_matrix.columns, d_matrix.index = X_idx, X_idx
        for c in combs:
            c[1] = d_matrix.loc[c[0], :].min(axis=0).sum()

        combs.sort(key=lambda x: x[1])
        cluster_idx = combs[0][0]
        self.cluster_centers_ = [X[c] for c in cluster_idx]

        self.labels_ = []
        for i in X_idx:
            self.labels_.append(
                cluster_idx.index(
                    d_matrix.loc[cluster_idx, i].idxmin()))

    def predict(self, X):
        '''Predict the closest cluster each sample in X belongs to.

        Args:
            X (array of arrays): New data to predict.

        Returns:
            list: Index of the cluster each sample belongs to.

        Example:
            >>> a = [1, 2, 3, 4, 5]
            >>> b = [1, 2.1, 2.9, 4.4, 5.1]
            >>> c = [6.2, 5, 4, 3, 2]
            >>> d = [7, 6, 5, 4, 3, 2, 1]
            >>> trendy = Trendy(2)
            >>> trendy.fit([a, b, c, d])
            >>> trendy.predict([[0.9, 2, 3.1, 4]])
            [0]
            >>> trendy.predict([[0.9, 2, 3.1], [7, 6.6, 5.5, 4.4]])
            [0, 1]

        '''
        preds = []
        for x in X:
            dists = [self.dist_func(x, c) for c in self.cluster_centers_]
            preds.append(pd.Series(dists).idxmin())
        return preds

    def assign(self, X):
        '''Alias of `predict()`'''
        return self.predict(X)

    def fit_predict(self, X):
        '''Compute cluster centers and predict cluster index for each sample.

        Args:
            X (array of arrays): Training instances to cluster.

        Returns:
            list: predicted labels

        Example:
            >>> a = [1, 2, 3, 4, 5]
            >>> b = [1, 2.1, 2.9, 4.4, 5.1]
            >>> c = [6.2, 5, 4, 3, 2]
            >>> d = [7, 6, 5, 4, 3, 2, 1]
            >>> trendy = Trendy(2)
            >>> trendy.fit_predict([a, b, c, d])
            [0, 0, 1, 1]

        '''
        self.fit(X)
        return self.labels_

if __name__ == "__main__":
    import doctest
    doctest.testmod()
