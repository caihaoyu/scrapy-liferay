# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    added = scrapy.Field()
    data_source = scrapy.Field()


class Question(BaseItem):
    _id = scrapy.Field()
    title = scrapy.Field()
    t_title = scrapy.Field()
    url = scrapy.Field()
    context = scrapy.Field()
    t_context = scrapy.Field()
    votes = scrapy.Field()
    closed = scrapy.Field()
    answer_count = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field()


class Answer(BaseItem):
    _id = scrapy.Field()
    question_id = scrapy.Field()
    context = scrapy.Field()
    t_context = scrapy.Field()
    publish_time = scrapy.Field()
    votes = scrapy.Field()
    accepted = scrapy.Field()
    publish_time = scrapy.Field()


class Comment(BaseItem):
    _id = scrapy.Field()
    tpye_ = scrapy.Field()
    type_id = scrapy.Field()
    context = scrapy.Field()
    publish_time = scrapy.Field()
