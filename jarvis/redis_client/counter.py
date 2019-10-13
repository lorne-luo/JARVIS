from datetime import datetime

from .client import client

DELIMITER = '='


def get_delimiter_item(key, tag):
    item = client.get(key)
    if not item or DELIMITER not in item:
        return None

    starter, value = item.split(DELIMITER)
    if starter == tag:
        return value
    else:
        return None


def set_delimiter_item(key, tag, value):
    return client.set(key, f'{tag}{DELIMITER}{value}')


# ========================================= TELSTRA SMS ==============================================
TELSTRA_SMS_MONTHLY_COUNTER = 'TELSTRA_SMS_MONTHLY_COUNTER'
TELSTRA_SMS_ACCESS_TOKEN = 'TELSTRA_SMS_ACCESS_TOKEN'
TELSTRA_SMS_DESTINATION_ADDRESS = 'TELSTRA_SMS_DESTINATION_ADDRESS'


def get_telstra_monthly_counter():
    month_str = datetime.utcnow().strftime('%Y-%m')
    value = get_delimiter_item(TELSTRA_SMS_MONTHLY_COUNTER, month_str)
    if not value:
        return 0
    return int(value)


def set_telstra_monthly_counter(value):
    month_str = datetime.utcnow().strftime('%Y-%m')
    set_delimiter_item(TELSTRA_SMS_MONTHLY_COUNTER, month_str, value)


def get_telstra_access_token():
    return client.get(TELSTRA_SMS_ACCESS_TOKEN)


def set_telstra_access_token(access_token, expires_in=3600):
    return client.setex(TELSTRA_SMS_ACCESS_TOKEN, expires_in, access_token)


def get_telstra_destination_address():
    return client.get(TELSTRA_SMS_DESTINATION_ADDRESS)


def set_telstra_destination_address(destination_address, expires_in=36000):
    return client.setex(TELSTRA_SMS_DESTINATION_ADDRESS, expires_in, destination_address)


# ========================================= Aliyun Email ==============================================
ALIYUN_EMAIL_DAILY_COUNTER = 'ALIYUN_EMAIL_DAILY_COUNTER'


def get_aliyun_email_daily_counter():
    day_str = datetime.utcnow().strftime('%Y-%m-%d')
    value = get_delimiter_item(ALIYUN_EMAIL_DAILY_COUNTER, day_str)
    if not value:
        return 0
    return int(value)


def set_aliyun_email_daily_counter(value):
    day_str = datetime.utcnow().strftime('%Y-%m-%d')
    set_delimiter_item(ALIYUN_EMAIL_DAILY_COUNTER, day_str, value)


# ========================================= CN Aliyun SMS ==============================================
ALIYUN_SMS_TOTAL_COUNTER = 'ALIYUN_SMS_TOTAL_COUNTER'


def get_aliyun_sms_counter():
    return client.get(ALIYUN_SMS_TOTAL_COUNTER) or 0


def set_aliyun_sms_counter(value):
    return client.set(ALIYUN_SMS_TOTAL_COUNTER, value)


def increase_aliyun_sms_counter():
    counter = get_aliyun_sms_counter()
    return set_aliyun_sms_counter(counter)
