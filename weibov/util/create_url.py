# -*- encoding: utf-8 -*-

STOCK_MAX_PAGE = 1
WEIBO_ARTICAL_BASE = 'https://api.weibo.cn/2/guest/statuses_extend'
WEIBO = {
    'c': ['android'],
    'from': ['1083195010'],
    'gsid': ['_2AkMt_xuEf8NhqwJRmPESxWzhaY90wwvEieKbo-pfJRMxHRl-wT9kqkFetRV6BkKgVI4D6KhmD43KFOF0SZkHkzO5NYCu'],
    'id': [''],
    'lang': ['zh_CN'],
    's': ['2b166666'],
}

HOME_PAGE_BASE = 'https://api.weibo.cn/2/profile/statuses'
HOME_PAGE = {
 'c': ['android'],
 'containerid': ['1076032534870595_-_WEIBO_SECOND_PROFILE_WEIBO'],
 'fid': ['1076032534870595_-_WEIBO_SECOND_PROFILE_WEIBO'],
 'from': ['1083195010'],
 'gsid': ['_2AkMt-wizf8NhqwJRmPESxWzhaY90wwvEieKbp_loJRMxHRl-wT9kqkIYtRV6BkKgVNEgZchYcwoMSU8Bd-itaClQGZNX'],
 'lfid': ['100103type=1&q={}&t=2'],
 'luicode': ['10000003'],
 'page': ['1'],
 's': ['2b166666']}

ARTICLE_BASE_URL = "https://api.weibo.cn/2/guest/statuses/extend"
ARTICLE = {
    'c': ['android'],
    'from': ['1083195010'],
    'gsid': ['_2AkMt_xuEf8NhqwJRmPESxWzhaY90wwvEieKbo-pfJRMxHRl-wT9kqkFetRV6BkKgVI4D6KhmD43KFOF0SZkHkzO5NYCu'],
    'id': ['4214895640271304'],
    'lang': ['zh_CN'],
    's': ['2b166666'],
}
STOCK_BASE_URL = "http://api.weibo.cn/2/guest/page"
STOCK = {
 'c': ['android'],
 'from': ['1083195010'],
 'containerid': ['230677{stock_id}'],
 'fid': ['230677{stock_id}'],
 'gsid': ['_2AkMt_xuEf8NhqwJRmPESxWzhaY90wwvEieKbo-pfJRMxHRl-wT9kqkFetRV6BkKgVI4D6KhmD43KFOF0SZkHkzO5NYCu'],
 'lfid': ['100303type=1&q={stock_name}&t=1'],
 'page': ['1'],
 's': ['2b166666'],
}


class GeneratorUrl(object):
    def __init__(self):
        pass

    @staticmethod
    def comb_query(dict_query):
        query_str = ''
        for query in dict_query.items():
            query_item = '{0}={1}'.format(query[0], query[1][0])
            query_str = '{0}&{1}'.format(query_item, query_str)
        return query_str

    @staticmethod
    def bigv_edit_query_data(dict_query, ticker, company):
        comb_id = ['107603{0}_-_WEIBO_SECOND_PROFILE_WEIBO'.format(ticker)]
        dict_query["containerid"] = comb_id
        dict_query["fid"] = comb_id
        dict_query["lfid"] = ['100103type=1&q={0}&t=3'.format(company)]
        return dict_query

    @staticmethod
    def stock_edit_query_data(dict_query, ticker, company, page=1):
        comb_id = ['230677{0}'.format(ticker)]
        dict_query["containerid"] = comb_id
        dict_query["fid"] = comb_id
        dict_query["lfid"] = ['100303type=520&q={0}&t=3'.format(company)]
        if page < 1:
            page = 1
        dict_query["page"] = [str(page)]
        return dict_query

    def get_weibo_url(self, dict_query, id):
        dict_query['id'] = [id]
        url = '{0}?{1}'.format(WEIBO_ARTICAL_BASE, self.comb_query(dict_query))
        return url

    def get_bigv_url(self, ticker, company):
        dict_query = self.bigv_edit_query_data(HOME_PAGE, ticker=ticker, company=company)
        url = '{0}?{1}'.format(HOME_PAGE_BASE, self.comb_query(dict_query))
        return url

    def get_article_url(self, dict_query, id):
        dict_query['id'] = [id]
        url = '{0}?{1}'.format(ARTICLE_BASE_URL, self.comb_query(dict_query))
        return url

    def get_stock_urls(self, ticker, company, max_page=STOCK_MAX_PAGE):
        urls = []
        for page in xrange(1, max_page+1):
            dict_query = self.stock_edit_query_data(STOCK, ticker=ticker, company=company, page=page)
            page_url = '{0}?{1}'.format(STOCK_BASE_URL, self.comb_query(dict_query))
            urls.append(page_url)
        return urls

if __name__ == '__main__':
    a = GeneratorUrl()
    print a.get_article_url(ARTICLE, id=4212708712543307)
    print 'https://api.weibo.cn/2/guest/statuses/extend?id=4212708712543307&s=2b166666&gsid=_2AkMt_xuEf8NhqwJRmPESxWzhaY90wwvEieKbo-pfJRMxHRl-wT9kqkFetRV6BkKgVI4D6KhmD43KFOF0SZkHkzO5NYCu&from=1083195010&c=androi'
