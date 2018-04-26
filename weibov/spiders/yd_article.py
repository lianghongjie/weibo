# -*- coding: utf-8 -*-
import scrapy
from redis import Redis
import json
from scrapy import Request
from ..items import YDArticleItem
from datetime import datetime,timedelta
import time
from scrapy import log
from ..settings import REDIS_HOST, REDIS_PORT

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, db=1)


class YdArticleSpider(scrapy.Spider):
    name = 'yd_article'

    def iter_data(self):
        redis_name = '{0}_article'.format((datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d'))
        for index in xrange(redis.scard(redis_name)):
            yield redis.spop(redis_name)

    def start_requests(self):
        data = self.iter_data()
        for line in data:
            json_data = json.loads(line)
            url = json_data['article_url']
            log.msg('request: {0}'.format(url), level=log.INFO)
            time.sleep(3)
            yield Request(url=url, meta={'json_data': json_data}, callback=self.parse)

    def parse(self, response):
        log.msg('response: {0}'.format(str(response.status),level=log.INFO))
        json_data = response.meta['json_data']
        article_data = json.loads(response.text)
        time_flag = datetime.now()
        yd_item = YDArticleItem()
        yd_item["attitudes_count"] = article_data.get("attitudes_count", 0)  # 点赞数
        yd_item["comments_count"] = article_data.get("comments_count", 0)  # 评论数
        yd_item["reposts_count"] = article_data.get("reposts_count", 0)  # 转发数
        yd_item["crawler_time"] = time_flag.strftime('%Y-%m-%d-%H')  # 爬取时间
        yd_item['source'] = json_data.get('source')
        yd_item['stock_id'] = json_data.get('stock_id')
        yd_item['stock_name'] = json_data.get('stock_name')
        yd_item["created_at"] = json_data.get('created_at')
        yd_item["reads_count"] = json_data.get('reads_count')
        yd_item["content"] = json_data.get('content')
        yd_item['user_id'] = json_data.get('user_id')
        yd_item["article_url"] = json_data.get('article_url')

        return yd_item
