See in Action
=============

Let's see how TrendyPy works with a few use cases.

Stock Data
----------

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

   assert trendy.predict([df.AAPL]) == [0]
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


Image Clustering
----------------

If you have the proper distance metric function for the right data, you can use TrendyPy to even cluster images. In this demo, I'll use black & white images from `MPEG7 CE Shape-1 Part B <http://www.imageprocessingplace.com/root_files_V3/image_databases.htm>`_ database. The goal is to correctly cluster the images and assign new ones to the appropriate clusters. Here are some simple images that'll be used to create the clusters. Each image is slightly different than the others in the same group. You can :download:`download the images <../image_data.zip>` if you want to reproduce the demo.

+------------------------------------------+------------------------------------------+------------------------------------------+
| .. figure:: ../image_data/car-01.gif     | .. figure:: ../image_data/car-02.gif     | .. figure:: ../image_data/car-03.gif     |
|                                          |                                          |                                          |
|   car-01.gif                             |   car-02.gif                             |   car-03.gif                             |
+------------------------------------------+------------------------------------------+------------------------------------------+
| .. figure:: ../image_data/carriage-02.gif| .. figure:: ../image_data/carriage-03.gif| .. figure:: ../image_data/carriage-04.gif|
|                                          |                                          |                                          |
|   carriage-02.gif                        |   carriage-03.gif                        |   carriage-04.gif                        |
+------------------------------------------+------------------------------------------+------------------------------------------+
| .. figure:: ../image_data/chopper-01.gif | .. figure:: ../image_data/chopper-02.gif | .. figure:: ../image_data/chopper-03.gif |
|                                          |                                          |                                          |
|   chopper-01.gif                         |   chopper-02.gif                         |   chopper-03.gif                         |
+------------------------------------------+------------------------------------------+------------------------------------------+

Define a function to read the image and convert to a numpy array.

.. ipython:: python

   from PIL import Image
   import numpy as np
   def load_image(file) :
       img = Image.open(file)
       img.load()
       return np.asarray(img, dtype="int32")

Read images and assign them into lists.

.. ipython:: python

   cars = [
      load_image('image_data/car-01.gif'),
      load_image('image_data/car-02.gif'),
      load_image('image_data/car-03.gif')]
   carriages = [
      load_image('image_data/carriage-02.gif'),
      load_image('image_data/carriage-03.gif'),
      load_image('image_data/carriage-04.gif')]
   choppers = [
      load_image('image_data/chopper-01.gif'),
      load_image('image_data/chopper-02.gif'),
      load_image('image_data/chopper-03.gif')]

`Euclidean Distance <https://en.wikipedia.org/wiki/Euclidean_distance>`_ can be used to calculate the similarity between images. So, let's import `euclidean_distance <utils.html#utils.euclidean_distance>`_ from `utils <utils.html>`_ module, then assign it as `algorithm` argument during the initialization.

.. ipython:: python

   from trendypy.trendy import Trendy
   from trendypy.utils import euclidean_distance
   trendy = Trendy(n_clusters=3, algorithm=euclidean_distance)
   trendy.fit(cars + carriages + choppers)
   trendy.labels_

.. ipython:: python
   :suppress:

   assert trendy.labels_ == [0, 0, 0, 1, 1, 1, 2, 2, 2]

As expected, it correctly clusters these simple images. Let's see if it predicts new data correctly.

+------------------------------------------+------------------------------------------+------------------------------------------+
| .. figure:: ../image_data/car-20.gif     | .. figure:: ../image_data/carriage-20.gif| .. figure:: ../image_data/chopper-08.gif |
|                                          |                                          |                                          |
|   car-20.gif                             |   carriage-20.gif                        |   chopper-08.gif                         |
+------------------------------------------+------------------------------------------+------------------------------------------+

.. ipython:: python

   new_car = load_image('image_data/car-20.gif')
   new_carriage = load_image('image_data/carriage-20.gif')
   new_chopper = load_image('image_data/chopper-08.gif')
   trendy.predict([new_car, new_carriage, new_chopper])

.. ipython:: python
   :suppress:

   assert trendy.predict([new_car, new_carriage, new_chopper]) == [0, 1, 2]

Looks like it correctly predicts new data as well.

.. note::

   Because of the limitation of the selected metric function (i.e. `Euclidean Distance <https://en.wikipedia.org/wiki/Euclidean_distance>`_), I had to cherry pick images with exact same sizes (i.e. 352×288). Depending on the function you choose, you may or may not do the same.

