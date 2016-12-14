# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:37:24 2016

@author: ZFang
"""

from lxml import html
import requests

page = requests.get('https://app2.msci.com/webapp/indexperf/pages/IEIPerformanceRegional.jsf')
tree = html.fromstring(page.content)