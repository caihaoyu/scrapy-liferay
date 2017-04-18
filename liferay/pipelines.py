# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from liferay.items import Question, Answer, Comment
from liferay.db.db_helper import DBHelper


class LiferayPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def open_spider(self, spider):
        self.db_helper = DBHelper()
        self.db_helper.init_spider(spider)

    def close_spider(self, spider):
        self.db_helper.close_spider(spider_name=spider.name)

    def process_item(self, item, spider):
        if isinstance(item, Question):
            self.db_helper.insert_question(item=dict(item))
        elif isinstance(item, Answer):
            self.db_helper.insert_answer(item=dict(item))
        elif isinstance(item, Comment):
            self.db_helper.insert_comment(item=dict(item))
