# coding:utf-8
from pymongo import MongoClient
from liferay.db.redis_helper import RedisHelper
from liferay.settings import MONGO_DATABASE_NAME, MONGO_HOST, MONGO_PORT
from liferay.statistics import REDIS_DB_KEY, REDIS_REQUEST
import time


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
        self.managers = self.db.managers
        self.products = self.db.products
        self.companies = self.db.companies
        self.articles = self.db.articles

    def close_spider(self, spider_name):
        if self.redis.llen(self.redis_request_key) == 0:
            self.redis.delete(self.redis_db_key)
        self.__close()

    def insert_manager(self, item):
        parent_id = item['parent_id']
        name = item['name']
        condition = {'parent_id': parent_id, 'name': name}
        if self.validate(collection=self.managers, condition=condition):
            self.managers.insert(item)

    def insert_company(self, item):
        self.companies.insert(item)

    def insert_product(self, item):
        parent_id = item['parent_id']
        name = item['name']
        condition = {'parent_id': parent_id, 'name': name}
        if self.validate(collection=self.products, condition=condition):
            self.products.insert(item)

    def insert_article(self, item):
        item['added'] = time.time()
        self.articles.insert(item)

    def validate(self, collection, condition):
        count = collection.find(condition).count()
        return count == 0

    def get_client(self):
        return self.client

    def __close(self):
        self.client.close()

    def get_proxys(self):
        db = self.client['ippool']
        return db.ips.find({'success': True})
