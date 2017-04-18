# coding:utf-8


class ArticleStatistics(object):
    REDIS_ARTICLE_ANCHOR = '%(spider_name)s:article_anchor'
    REDIS_ARTICLE_START = '%(spider_name)s:article_start'


REDIS_DB_KEY = '%(spider_name)s:db'
REDIS_REQUEST = '%(spider_name)s:requests'
REDIS_ITEM = '%(spider_name)s:items'
