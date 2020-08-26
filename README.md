# TrendyPy

[![PyPI](https://img.shields.io/pypi/v/trendypy)](https://pypi.org/project/trendypy/)
[![tests](https://github.com/ddaskan/trendypy/workflows/Python%20package/badge.svg)](https://github.com/ddaskan/trendypy/actions?query=workflow%3A%22Python+package%22)
[![Codecov](https://img.shields.io/codecov/c/gh/ddaskan/trendypy)](https://codecov.io/gh/ddaskan/trendypy/)
[![Documentation Status](https://readthedocs.org/projects/trendypy/badge/?version=latest)](https://trendypy.readthedocs.io/en/latest/?badge=latest)
[![PyPI - License](https://img.shields.io/pypi/l/trendypy)](https://github.com/ddaskan/trendypy/blob/master/LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/trendypy)](https://pypi.org/project/trendypy/)
[![GitHub last commit](https://img.shields.io/github/last-commit/ddaskan/trendypy)](https://github.com/ddaskan/trendypy)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fddaskan%2Ftrendypy)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fddaskan%2Ftrendypy)

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

Refer to [this extensive demo](https://trendypy.readthedocs.io/en/latest/source/seeinaction.html) to see it in action or just check [API Reference](https://trendypy.readthedocs.io/en/latest/index.html#api-reference) for details.

## Post
The idea is originated from the post [Trend Clustering](http://www.doganaskan.com/blog/posts/trendcluster.html).
