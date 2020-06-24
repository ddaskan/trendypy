# TrendyPy

TrendyPy is a small Python package for trend line clustering. It is developed to create time series clusters by calculating trend similarity distance with [Dynamic Time Warping](https://en.wikipedia.org/wiki/Dynamic_time_warping).

## Installation

You can install TrendyPy with pip.

```
pip install trendypy
```

TrendyPy depends on Pandas, Numpy and fastdtw and works in Python 3.5+.

## Quickstart

Trendy has scikit-learn like api to allow easy integration to existing programs.

```python
>>> from trendypy.trendy import Trendy
>>> a = [1, 2, 3, 4, 5] # increasing trend
>>> b = [1, 2.1, 2.9, 4.4, 5.1] # increasing trend
>>> c = [6.2, 5, 4, 3, 2] # decreasing trend
>>> d = [7, 6, 5, 4, 3, 2, 1] # decreasing trend
>>> trendy = Trendy(n_clusters=2)
>>> trendy.fit([a, b, c, d])
>>> print(trendy.labels_)
[0, 0, 1, 1]
>>> trendy.predict([[0.9, 2, 3.1, 4]]) # another increasing trend
[0]
```

Refer to [this extensive demo](http://www.doganaskan.com/trendypy/source/seeinaction.html) to see it in action or just check [API Reference](http://www.doganaskan.com/trendypy/index.html#api-reference) for details.

## Post
The idea is originated from the post [Trend Clustering](http://www.doganaskan.com/blog/posts/trendcluster.html).
