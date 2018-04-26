# -*- coding: utf-8 -*-


import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('/niub/scrapy/bin')
sys.path.append('/niub/scrapy')
from scrapy.cmdline import execute
#execute(["scrapy", "crawl", "stock"])
execute(["scrapy", "crawl", "bigv"])
