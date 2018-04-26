# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from settings import REDIS_HOST, REDIS_PORT
from items import StockItem, UserItem, WeiboItem, BigVItem, YDArticleItem
import os
from datetime import datetime
from redis import Redis

root_path = '/niub/abc_crawler_data/sina'

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, db=1)


class WeibovPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, StockItem):
            stock_path = datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')
            STOCK_PATH = os.path.join(root_path,'{0}_stock_article.json'.format(stock_path))
            json_data = json.dumps(dict(item))
            with open(STOCK_PATH, 'a') as fl:
                fl.write('sina_stock {0}\n'.format(json_data))
            redis.sadd('{0}_article'.format(datetime.now().strftime('%Y-%m-%d')), json_data)
        elif isinstance(item, UserItem):
            stock_path = datetime.now().strftime('%Y-%m-%d-%Hh-%Mm')
            USER_PATH = os.path.join(root_path,'{0}_stock_user.json'.format(stock_path))
            with open(USER_PATH, 'a') as fl:
                fl.write('sina_user {0}\n'.format(json.dumps(dict(item))))
        return item


class BigVPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            bigv_path = datetime.now().strftime('%Y-%m-%d')
            json_data = json.dumps(dict(item))
            WEIBO_PATH = os.path.join(root_path,'{0}bigv_article.json'.format(bigv_path))
            with open(WEIBO_PATH, 'a') as fl:
                fl.write('sina_stock {0}\n'.format(json_data))
            redis.sadd('{0}_article'.format(datetime.now().strftime('%Y-%m-%d')), json_data)
        elif isinstance(item, BigVItem):
            bigv_path = datetime.now().strftime('%Y-%m-%d')
            BIGV_PATH = os.path.join(root_path,'{0}bigv_user.json'.format(bigv_path))
            with open(BIGV_PATH, 'a') as fl:
                fl.write('sina_user {0}\n'.format(json.dumps(dict(item))))
        return item

class YDPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, YDArticleItem):
            bigv_path = datetime.now().strftime('%Y-%m-%d')
            YD_ARTICLE_PATH = os.path.join(root_path, '{0}_yd_article.json'.format(bigv_path))
            with open(YD_ARTICLE_PATH, 'a') as fl:
                fl.write('sina_stock {0}\n'.format(json.dumps(dict(item))))
