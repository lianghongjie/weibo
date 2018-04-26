# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class StockItem(scrapy.Item):
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    created_at = Field()
    crawler_time = Field()
    reads_count = Field()
    stock_name = Field()
    content = Field()
    article_url = Field()
    user_id = Field()
    stock_id = Field()
    source = Field()


class UserItem(scrapy.Item):
    name = Field()
    description = Field()
    user_create_at = Field()
    credit_score = Field()
    followers_count = Field()
    gender = Field()
    crawler_time = Field()
    geo_enabled = Field()
    user_id = Field()
    location = Field()
    friends_count = Field()
    verified_level = Field()
    statuses_count = Field()
    source = Field()


class WeiboItem(scrapy.Item):
    content = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    created_at = Field()
    crawler_time = Field()
    reads_count = Field()
    article_url = Field()
    user_id = Field()
    source = Field()
    stock_id = Field()
    stock_name = Field()


class BigVItem(scrapy.Item):
    name = Field()
    description = Field()
    user_create_at = Field()
    credit_score = Field()
    followers_count = Field()
    crawler_time = Field()
    gender = Field()
    geo_enabled = Field()
    user_id = Field()
    location = Field()
    friends_count = Field()
    verified_level = Field()
    statuses_count = Field()
    source = Field()

class YDArticleItem(scrapy.Item):
    content = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    created_at = Field()
    crawler_time = Field()
    reads_count = Field()
    article_url = Field()
    user_id = Field()
    source = Field()
    stock_id = Field()
    stock_name = Field()
