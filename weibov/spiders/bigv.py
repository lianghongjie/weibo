# -*- coding: utf-8 -*-
import scrapy
from ..util.create_url import GeneratorUrl, WEIBO
from datetime import datetime
from ..items import BigVItem, WeiboItem
import time
from scrapy.http import Request
import json
import os


class BigvSpider(scrapy.Spider):
    name = 'bigv'
    allowed_domains = ['api.weibo.cn']
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

    def start_requests(self):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test/bigv.csv')
        with open(file_path, 'r') as fl:
            iter_file = fl.readlines()
        gen_url = GeneratorUrl()
        for index, data in enumerate(iter_file):
            data = data.strip("\n").split(",")
            user_name = data[1]
            user_id = data[0]
            source = data[2]
            url = gen_url.get_bigv_url(company=user_name, ticker=user_id)
            time.sleep(3)
            yield Request(url=url, headers=self.headers, callback=self.parse,
                          meta={'user_name': user_name, 'user_id': user_id, 'source': source,
                                'proxy': 'http://127.0.0.1:3128'})

    def parse(self, response):
        json_data = json.loads(response.text)
        try:
            cards = json_data["cards"]
        except KeyError:
            return
        if not len(cards):
            return
        items = []
        for index, card in enumerate(cards):
            time_flag = datetime.now()
            if index == 0:
                user_item = BigVItem()
                user = card["mblog"]["user"]
                user_item["name"] = response.meta['user_name']
                user_item["description"] = user.get("description", "")  # 描述
                user_item["user_create_at"] = user.get("created_at", "")  # 用户创建日期
                user_item["credit_score"] = user.get("credit_score", "")  # 信用评分
                user_item["followers_count"] = user.get("followers_count", 0)  # 粉丝数
                user_item["gender"] = user.get("gender", "")  # 性别（m）
                user_item["geo_enabled"] = user.get("geo_enabled", "")  # 是否认证
                user_id = response.meta['user_id']
                user_item["user_id"] = user_id  # user id
                user_item["location"] = user.get("location", "")  # 用户城市
                user_item["friends_count"] = user.get("friends_count", 0)  # 用户关注人数
                user_item["verified_level"] = user.get("verified_level", "")  # 认证级别
                user_item["statuses_count"] = user.get("statuses_count", 0)  # 全部微波数
                user_item["crawler_time"] = time_flag.strftime('%Y-%m-%d-%H')
                user_item['source'] = response.meta['source']
                items.append(user_item)
            stock_item = WeiboItem()
            user_mblog = card["mblog"]
            stock_item["content"] = user_mblog.get("text", "")  # 内容
            stock_item["attitudes_count"] = user_mblog.get("attitudes_count", 0)  # 点赞数
            stock_item["comments_count"] = user_mblog.get("comments_count", 0)  # 评论数
            stock_item["reposts_count"] = user_mblog.get("reposts_count", 0)  # 转发数
            stock_item["created_at"] = user_mblog.get("created_at", "")  # 文章创建时间
            stock_item["crawler_time"] = time_flag.strftime('%Y-%m-%d-%H')  # 爬取时间
            stock_item["reads_count"] = user_mblog.get("reads_count", 0)  # 阅读量
            id = user_mblog.get("id", "")
            user_id = response.meta['user_id']
            stock_item['user_id'] = user_id
            stock_item["article_url"] = GeneratorUrl().get_weibo_url(WEIBO, id=id)  # 文章url
            stock_item['source'] = 'user'
            stock_item['stock_id'] = ''
            stock_item['stock_name'] = ''
            items.append(stock_item)
        return items


