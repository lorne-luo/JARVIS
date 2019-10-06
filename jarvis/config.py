from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool('DEBUG', default=False)

# === REDIS ===

PRICE_CHANNEL = 15
SYSTEM_CHANNEL = 14
ORDER_CHANNEL = 12

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_HOST')
REDIS_DB_NUMBER = env.int('REDIS_DB_NUMBER', default=0)

# === TELSTRA SMS ===

TELSTRA_CLIENT_KEY = env.str('TELSTRA_CLIENT_KEY')
TELSTRA_CLIENT_SECRET = env.str('TELSTRA_CLIENT_SECRET')
ADMIN_MOBILE_NUMBER = env.str('ADMIN_MOBILE_NUMBER', default='0413725868')
