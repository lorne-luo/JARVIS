import redis

from .. import config

client = redis.StrictRedis(host=config.REDIS_HOST,
                           port=config.REDIS_PORT,
                           db=config.REDIS_DB_NUMBER,
                           decode_responses=True)

def test_connection():
    return client.client_list()