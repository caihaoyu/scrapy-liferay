# coding:utf-8
from liferay.settings import REDIS_HOST, REDIS_PORT
import redis


class RedisHelper(object):

    __pool = None

    @staticmethod
    def get_conn():
        if RedisHelper.__pool is None:
            __pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
        return redis.StrictRedis(connection_pool=__pool)
