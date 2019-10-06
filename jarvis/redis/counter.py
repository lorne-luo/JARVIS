from .client import client

# ========================================= TELSTRA SMS ==============================================

TELSTRA_SMS_MONTHLY_COUNTER = 'TELSTRA_SMS_MONTHLY_COUNTER'
TELSTRA_SMS_ACCESS_TOKEN = 'TELSTRA_SMS_ACCESS_TOKEN'
TELSTRA_SMS_DESTINATION_ADDRESS = 'TELSTRA_SMS_DESTINATION_ADDRESS'


def get_telstra_monthly_counter():
    return client.get(TELSTRA_SMS_MONTHLY_COUNTER) or 0


def set_telstra_monthly_counter(value):
    return client.set(TELSTRA_SMS_MONTHLY_COUNTER, value)


def get_telstra_access_token():
    return client.get(TELSTRA_SMS_ACCESS_TOKEN)


def set_telstra_access_token(access_token, expires_in=3600):
    return client.setex(TELSTRA_SMS_ACCESS_TOKEN, expires_in, access_token)


def get_telstra_destination_address():
    return client.get(TELSTRA_SMS_DESTINATION_ADDRESS)


def set_telstra_destination_address(destination_address, expires_in=36000):
    return client.setex(TELSTRA_SMS_DESTINATION_ADDRESS, expires_in, destination_address)
