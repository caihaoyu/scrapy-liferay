from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import dateutil.parser

import re
import json
from datetime import datetime

from liferay.items import Question, Comment, Answer
from liferay.settings import *


class Stackoverflow(CrawlSpider):
    allowed_domains = ["stackoverflow.com"]
    name = 'liferay'

    domain = 'http://stackoverflow.com/'
    list_type = 'json'
    first_list_url = ('http://stackoverflow.com/search?pagesize=50'
                      '&q=liferay')
    page_url = ('http://stackoverflow.com/search?page=%s'
                '&q=liferay&pagesize=50')
    page_sum_xpath = '//div[@class="pager fl"]/a[5]/@href'
    list_items_xpath = '//div[@class="question-summary search-result"]'
    item_url_xpath = '//div[@class="result-link"]/span/a/@href'
    item_date_xpath = '//span[@class="relativetime"]/@title'
    item_title_xpath = '//div[@class="result-link"]/span/a/@title'
    item_tags_xpath = '//a[@class="post-tag"]/text()'
    content_xpath = '//div[@class="post-text"]'

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'DNSCACHE_ENABLED': True,
    }

    def start_requests(self):
        url = self.first_list_url
        yield Request(url, dont_filter=True, callback=self.parse_first_list)

    def parse_first_list(self, response):
        i = 1
        page_sum = self.get_page_sum(response)
        print(page_sum)
        while i <= page_sum:
            url = self.get_page_url(response, i)
            yield Request(url, dont_filter=True, callback=self.parse_list)
            i += 1

    def get_page_url(self, response, index):
        return self.page_url % (str(index))

    def parse_list(self, response):
        # import pdb
        # pdb.set_trace()
        selector = Selector(response)
        items = selector.xpath(self.list_items_xpath).extract()
        for item in items:
            s = Selector(text=item)
            question = Question()
            link = self.domain + s.xpath(self.item_url_xpath).extract_first()
            if link:
                question['url'] = link
                if self.item_date_xpath:
                    question['publish_time'] = dateutil.parser.parse(
                        s.xpath(self.item_date_xpath).extract_first())
                question['title'] = s.xpath(
                    self.item_title_xpath).extract_first().strip()
                question['tags'] = s.xpath(self.item_tags_xpath).extract()
                # print(question)
                yield Request(link, meta={'question': question},
                              dont_filter=True, callback=self.parse_question)

    def get_page_sum(self, response):
        # return 2
        selector = Selector(response)
        page_sum_url = selector.xpath(self.page_sum_xpath).extract_first()
        page_sum = ''.join(list(filter(str.isdigit, str(page_sum_url))))
        # print(page_sum)
        return int(page_sum)

    def parse_question(self, response):
        selector = Selector(response)
        question = response.meta['question']
        context = ''.join(selector.xpath(self.content_xpath).extract())
        question['context'] = context
        # print(question)
        yield question
