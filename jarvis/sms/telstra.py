import datetime
import logging
import time

import Telstra_Messaging
from Telstra_Messaging.rest import ApiException

from .validator import validate_au_mobile
from .. import config
from ..redis_client import counter as redis_counter

logger = logging.getLogger(__name__)
TELSTRA_LENGTH_PER_SMS = 160
TELSTRA_MONTHLY_FREE_LIMIT = 1000


def get_token():
    access_token = redis_counter.get_telstra_access_token()
    if access_token:
        return access_token

    configuration = Telstra_Messaging.Configuration()
    api_instance = Telstra_Messaging.AuthenticationApi(Telstra_Messaging.ApiClient(configuration))
    client_id = config.TELSTRA_CLIENT_KEY
    client_secret = config.TELSTRA_CLIENT_SECRET
    grant_type = 'client_credentials'

    try:
        # Generate OAuth2 token
        api_response = api_instance.auth_token(client_id, client_secret, grant_type)
        access_token = api_response.access_token
        expires_in = int(api_response.expires_in) if api_response.expires_in.isdigit() else 3599
        redis_counter.set_telstra_access_token(access_token, expires_in)
        return access_token
    except ApiException as e:
        logger.error("Exception when calling AuthenticationApi->auth_token: %s\n" % e)
        return None


def _get_from_number():
    destination_address = redis_counter.get_telstra_destination_address()
    if destination_address:
        return destination_address

    configuration = Telstra_Messaging.Configuration()
    configuration.access_token = get_token()
    api_instance = Telstra_Messaging.ProvisioningApi(Telstra_Messaging.ApiClient(configuration))
    provision_number_request = Telstra_Messaging.ProvisionNumberRequest()  # ProvisionNumberRequest | A JSON payload containing the required attributes
    api_response = api_instance.create_subscription(provision_number_request)
    destination_address = api_response.destination_address
    expiry_timestamp = int(api_response.expiry_date / 1000)
    expires_in = expiry_timestamp - int(time.mktime(datetime.datetime.now().timetuple()))
    redis_counter.set_telstra_destination_address(destination_address, expires_in)
    return destination_address


def send_au_sms(mobile_number, message):
    counter = redis_counter.get_telstra_monthly_counter()
    counter = int(counter)
    if not counter < TELSTRA_MONTHLY_FREE_LIMIT:
        logger.info('[SMS] Telstra SMS reach 1000 free limitation.')
        return False, 'Telstra SMS reach 1000 free limitation.'

    mobile_number = validate_au_mobile(mobile_number)
    if not mobile_number:
        return False, 'INVALID_PHONE_NUMBER'

    message = str(message)
    if not message:
        return False, 'EMPTY_CONTENT'

    # Configure OAuth2 access token for authorization: auth
    configuration = Telstra_Messaging.Configuration()
    configuration.access_token = get_token()
    from_number = _get_from_number()

    # api_instance = Telstra_Messaging.ProvisioningApi(Telstra_Messaging.ApiClient(configuration))
    # provision_number_request = Telstra_Messaging.ProvisionNumberRequest()  # ProvisionNumberRequest | A JSON payload containing the required attributes
    api_instance = Telstra_Messaging.MessagingApi(Telstra_Messaging.ApiClient(configuration))
    send_sms_request = Telstra_Messaging.SendSMSRequest(mobile_number, message, from_number)

    try:
        # {'country': [{u'AUS': 1}],
        #  'message_type': 'SMS',
        #  'messages': [{'delivery_status': 'MessageWaiting',
        #                'message_id': 'd872ad3b000801660000000000462650037a0801-1261413725868',
        #                'message_status_url': 'https://tapi.telstra.com/v2/messages/sms/d872ad3b000801660000000000462650037a0801-1261413725868/status',
        #                'to': '+61413725868'}],
        #  'number_segments': 1}
        api_response = api_instance.send_sms(send_sms_request)
        success = api_response.messages[0].delivery_status == 'MessageWaiting'

        if success:
            counter = redis_counter.get_telstra_monthly_counter()
            counter = int(counter)
            counter += 1
            redis_counter.set_telstra_monthly_counter(counter)
            if counter == TELSTRA_MONTHLY_FREE_LIMIT - 1:
                send_to_admin('[Warning] Telstra sms meet monthly limitation.')
                redis_counter.set_telstra_monthly_counter(counter + 1)

            return True, 'MessageWaiting'
    except ApiException as e:
        logger.error("Exception when calling MessagingApi->send_sms: %s\n" % e)
        return False, str(e)


def send_to_admin(message):
    send_au_sms(config.ADMIN_MOBILE_NUMBER, message)
