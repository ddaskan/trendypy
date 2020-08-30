See in Action
-------------

In this demo, I'd like to show you how to use TrendyPy in some :download:`stock data <../stock_data.csv>` between 2018-01-01 and 2020-06-28. You can download the data from :download:`here <../stock_data.csv>` to reproduce the demo.

Let's say we have some stock data from a combination of tech and banking. And, we want to identify an unknown trend if it's a tech stock or banking. For this purpose, we'll use FB (i.e. Facebook), GOOGL (i.e. Google), AMZN (i.e Amazon), BAC (i.e. Bank of America) and WFC (i.e. Wells Fargo) for training data then AAPL (i.e. Apple) and c (i.e. Citigroup) for prediction data.

But first, here is how the data looks.

.. ipython:: python

   import pandas as pd
   import matplotlib.pyplot as plt
   df = pd.read_csv('stock_data.csv')
   @savefig ticks_raw.png
   df.plot()

If we cluster like this, the expensive stocks like GOOGL and AMZN will alone constitute one cluster which it's clearly not intended. So, let's scale first.

.. ipython:: python

   from trendypy import utils
   df = df.apply(utils.scale_01)
   @savefig ticks_scaled.png
   df.plot()

It's a bit apparent that BAC, WFC and c are different than the others. Let's put sectors side by side to see the difference better.

.. ipython:: python

   fig, axes_ = plt.subplots(nrows=1, ncols=2)
   axes_[0].set_title('Tech')
   axes_[1].set_title('Banking')
   df[['AAPL', 'FB', 'GOOGL', 'AMZN']].plot(ax=axes_[0])
   @savefig ticks_scaled_subplot.png
   df[['BAC', 'WFC', 'c']].plot(ax=axes_[1])


Now, we can use the training data to fit. Remember, we're setting AAPL and c aside to predict later and only fit by using the rest.

.. ipython:: python

   from trendypy.trendy import Trendy
   trendy = Trendy(n_clusters=2) # 2 for tech and banking
   trendy.fit([df.FB, df.GOOGL, df.AMZN, df.BAC, df.WFC])
   trendy.labels_

.. ipython:: python
   :suppress:

   assert trendy.labels_ == [0, 0, 0, 1, 1]

You can also use `fit_predict <trendy.html#trendy.Trendy.fit_predict>`_ method for this purpose, it's essentially the same.

.. ipython:: python

   trendy.fit_predict([df.FB, df.GOOGL, df.AMZN, df.BAC, df.WFC])

.. ipython:: python
   :suppress:

   assert trendy.fit_predict([df.FB, df.GOOGL, df.AMZN, df.BAC, df.WFC]) == [0, 0, 0, 1, 1]

As expected, it successfully assigns FB, GOOGL and AMZN into the first cluster (i.e. ``0``) and BAC and WFC into the second (i.e. ``1``). So, we can name ``0`` as tech and ``1`` as banking.

Now, let's make predictions on the prediction data that we set aside earlier (i.e. AAPL, c).

.. ipython:: python
   :suppress:

   assert trendy.predict([df.AAPL]) == [1]
   assert trendy.predict([df.c]) == [1]

.. ipython:: python

   trendy.predict([df.AAPL]) # expecting `0` since AAPL is a part of tech
   trendy.predict([df.c]) # expecting `1` since c is a part of banking

As seen above, it correctly predicts trends.

You can easily pickle the model object to be used later with `to_pickle <trendy.html#trendy.Trendy.to_pickle>`_ method.

.. ipython:: python

   trendy.to_pickle('my_first_trendy.pkl')

.. ipython:: python
   :suppress:

   import os
   os.remove('my_first_trendy.pkl')

And, that's all.


