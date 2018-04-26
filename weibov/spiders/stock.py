# -*- coding: utf-8 -*-
import scrapy
from ..util.create_url import GeneratorUrl, ARTICLE
import json
from datetime import datetime
from scrapy.http import Request
from ..items import StockItem, UserItem
import time
import os


class StockSpider(scrapy.Spider):
    name = 'stock'

    def start_requests(self):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test/have.csv')
        with open(file_path, 'r') as fl:
            iter_file = fl.readlines()
        gen_url = GeneratorUrl()
        for index, data in enumerate(iter_file):
            data = data.strip("\n").split(",")
            company = data[0].split("(")[0]
            ticker = data[-1]
            urls = gen_url.get_stock_urls(company=company, ticker=ticker)
            for url in urls:
                time.sleep(4)
                yield Request(url=url, callback=self.parse, meta={'company': company, 'ticker': ticker,
                                                                  'proxy': 'http://127.0.0.1:3128'})

    def parse(self, response):
        json_data = json.loads(response.text)
        try:
            cards = json_data["cards"].__len__()
        except KeyError:
            return
        if not cards:
            return
        user_groups = json_data["cards"][-1]["card_group"]
        items = []
        for user_card in user_groups:
            time_flag = datetime.now()
            stock_item = StockItem()
            user_mblog = user_card["mblog"]
            stock_item["attitudes_count"] = user_mblog.get("attitudes_count", 0)  # 点赞数
            stock_item["comments_count"] = user_mblog.get("comments_count", 0)  # 评论数
            stock_item["reposts_count"] = user_mblog.get("reposts_count", 0)  # 转发数
            stock_item["created_at"] = user_mblog.get("created_at", "")  # 文章创建时间
            stock_item["crawler_time"] = time_flag.strftime('%Y-%m-%d-%H')  # 爬去时间
            stock_item["reads_count"] = user_mblog.get("reads_count", 0)  # 阅读量
            stock_item["stock_name"] = response.meta['company']  # 股票名
            stock_item["content"] = user_mblog.get("text", "")  # 内容
            stock_item["source"] = 'stock'

            blog_id = user_mblog.get("id", 0)  # blog id
            stock_item["article_url"] = GeneratorUrl().get_article_url(ARTICLE, id=blog_id)  # 文章url
            user_item = UserItem()
            user = user_card["mblog"]["user"]
            user_item["name"] = user.get("name", "")
            user_item["description"] = user.get("description", "")  # 描述
            user_item["user_create_at"] = user.get("created_at", "")  # 用户创建日期
            user_item["credit_score"] = user.get("credit_score", "")  # 信用评分
            user_item["followers_count"] = user.get("followers_count", 0)  # 粉丝数
            user_item["gender"] = user.get("gender", "")  # 性别（m）
            user_item["geo_enabled"] = user.get("geo_enabled", "")  # 是否认证
            user_id = user.get("id", "")
            user_item["user_id"] = user_id  # user id
            stock_item['user_id'] = user_id
            user_item["location"] = user.get("location", "")  # 用户城市
            user_item["friends_count"] = user.get("friends_count", 0)  # 用户关注人数
            user_item["verified_level"] = user.get("verified_level", "")  # 认证级别
            user_item["statuses_count"] = user.get("statuses_count", 0)  # 全部微波数
            user_item["crawler_time"] = time_flag.strftime('%Y-%m-%d-%H')
            stock_id = response.meta['ticker']
            stock_item['stock_id'] = stock_id
            user_item['source'] = 'find_by_code'
            items.append(stock_item)
            items.append(user_item)
        return items
