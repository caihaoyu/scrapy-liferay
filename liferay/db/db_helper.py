# coding:utf-8
from pymongo import MongoClient
from liferay.db.redis_helper import RedisHelper
from liferay.settings import MONGO_DATABASE_NAME, MONGO_HOST, MONGO_PORT
from liferay.statistics import REDIS_DB_KEY, REDIS_REQUEST


class DBHelper(object):

    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)

    def init_spider(self, spider):
        spider_name = spider.name
        self.redis = RedisHelper.get_conn()
        self.redis_db_key = REDIS_DB_KEY % {'spider_name': spider_name}
        self.redis_request_key = REDIS_REQUEST % {'spider_name': spider_name}
        db_name = self.redis.get(self.redis_db_key)
        if not db_name:
            db_name = MONGO_DATABASE_NAME.get(
                spider_name, MONGO_DATABASE_NAME['default'])
            self.redis.set(self.redis_db_key, db_name)
        else:
            db_name = db_name.decode("utf-8")
        self.db = self.client[db_name]
        self.questions = self.db.questions
        self.comments = self.db.comments
        self.answers = self.db.answers

    def close_spider(self, spider_name):
        if self.redis.llen(self.redis_request_key) == 0:
            self.redis.delete(self.redis_db_key)
        self.__close()

    def insert_question(self, item):
        self.questions.insert(item)

    def insert_comment(self, item):
        self.comments.insert(item)

    def insert_answer(self, item):
        self.answers.insert(item)

    def get_client(self):
        return self.client

    def __close(self):
        self.client.close()
