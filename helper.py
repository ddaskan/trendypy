# -*- coding: utf-8 -*-
"""
Created on Thu May 18 22:58:12 2017
@author: c0redumb
source: https://github.com/c0redumb/yahoo_quote_download/blob/master/yahoo_quote_download/yqd.py
"""

# To make print working for Python2/3
from __future__ import print_function

# Use six to import urllib so it is working for Python2/3
from six.moves import urllib
# If you don't want to use six, please comment out the line above
# and use the line below instead (for Python3 only).
#import urllib.request, urllib.parse, urllib.error

import time
import pandas as pd

'''
Starting on May 2017, Yahoo financial has terminated its service on
the well used EOD data download without warning. This is confirmed
by Yahoo employee in forum posts.
Yahoo financial EOD data, however, still works on Yahoo financial pages.
These download links uses a "crumb" for authentication with a cookie "B".
This code is provided to obtain such matching cookie and crumb.
'''

# Build the cookie handler
cookier = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cookier)
urllib.request.install_opener(opener)

# Cookie and corresponding crumb
_cookie = None
_crumb = None

# Headers to fake a user agent
_headers={
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
}

def _get_cookie_crumb():
    '''
    This function perform a query and extract the matching cookie and crumb.
    '''

    # Perform a Yahoo financial lookup on SP500
    req = urllib.request.Request('https://finance.yahoo.com/quote/^GSPC', headers=_headers)
    f = urllib.request.urlopen(req)
    alines = f.read().decode('utf-8')

    # Extract the crumb from the response
    global _crumb
    cs = alines.find('CrumbStore')
    cr = alines.find('crumb', cs + 10)
    cl = alines.find(':', cr + 5)
    q1 = alines.find('"', cl + 1)
    q2 = alines.find('"', q1 + 1)
    crumb = alines[q1 + 1:q2]
    _crumb = crumb

    # Extract the cookie from cookiejar
    global cookier, _cookie
    for c in cookier.cookiejar:
        if c.domain != '.yahoo.com':
            continue
        if c.name != 'B':
            continue
        _cookie = c.value

    # Print the cookie and crumb
    #print('Cookie:', _cookie)
    #print('Crumb:', _crumb)
    return _crumb
    