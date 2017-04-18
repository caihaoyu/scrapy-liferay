# -*- coding: utf-8 -*-

# Scrapy settings for liferay project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'liferay'

SPIDER_MODULES = ['liferay.spiders']
NEWSPIDER_MODULE = 'liferay.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# COOKIES
COOKIES_ENABLES = False
COOKIES_DEBUG = False


# The maximum number of concurrent (ie. simultaneous) requests that will
# be performed to any single domain.
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 0
# CONCURRENT_REQUESTS_PER_SPIDER = 100

DNSCACHE_ENABLED = True
# DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 20

# DEFAULT_REQUEST_HEADERS = {
#     'Referer': 'http://Google.com'
# }

# Retry many times since proxies often fail
RETRY_TIMES = 20
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 302, 304]

ITEM_PIPELINES = {
    'liferay.pipelines.MongoPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400
}
ROBOTSTXT_OBEY = False

#
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 300,
    'liferay.rotate_useragent.RotateUserAgentMiddleware': 400,
    # 'magic_mirror.spiders.rotate_useragent.RotateUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700
}

# custom settings
REDIS_HOST = '0.0.0.0'
REDIS_PORT = 6379
LOG_PATH = ''
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE_NAME = {'default': 'liferay'}

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
