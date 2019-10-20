import inspect
import logging
import sys
from datetime import datetime
from uuid import uuid1

import click
import redis
import rpyc
from rpyc.utils.server import ThreadedServer

from jarvis.aliyun.email.smtp import send_email
from jarvis.aliyun.sms.service import send_aliyun_sms
from jarvis.redis_client import client
from jarvis.sms import send_to_admin, send_au_sms
from jarvis.telegram.bot import telegram_jarvis

logger = logging.getLogger(__name__)


class JarvisService(rpyc.Service):

    # =================================== SMS =================================
    def exposed_sms_au(self, mobile_number, message, from_app):
        try:
            logger.info(f'sms_au from {from_app}: {mobile_number} @ {message}')
            return send_au_sms(mobile_number, message)
        except Exception as ex:
            logger.error(f'[{inspect.stack()[0][3]}] {ex}, message={message}')

    def exposed_sms_admin(self, message, from_app):
        try:
            logger.info(f'sms_to_admin from {from_app}: {message}')
            return send_to_admin(message)
        except Exception as ex:
            logger.error(f'[{inspect.stack()[0][3]}] {ex}, message={message}')

    # =================================== TELEGRAM =================================
    def exposed_telegram_jarvis(self, message, from_app):
        try:
            logger.info(f'telegram_jarvis from {from_app}: {message}')
            return telegram_jarvis(message)
        except Exception as ex:
            logger.error(f'[{inspect.stack()[0][3]}] {ex}, message={message}')

    # =================================== Aliyun Email =================================
    def exposed_send_mail(self, receivers, subject, html_content, text_content=None, from_app=None):
        try:
            logger.info(f'send_email from {from_app}: to {receivers} # {html_content or text_content}')
            return send_email(receivers, subject, html_content, text_content)
        except Exception as ex:
            logger.error(f'[{inspect.stack()[0][3]}] {ex}, to {receivers} # {html_content or text_content}')

    # =================================== Aliyun SMS CN =================================
    def exposed_sms_cn(self, phone_numbers, template_code, template_param=None, business_id=None):
        try:
            business_id = business_id or uuid1()
            return send_aliyun_sms(business_id, phone_numbers, template_code, template_param)
        except Exception as ex:
            logger.error(
                f'[{inspect.stack()[0][3]}] {ex}, to {phone_numbers}, template_code={template_code}, template_param={template_param}')


@click.command()
@click.option('--port', "-p", default=54321, help='Port of JARVIS service')
def main(port):
    # test redis connection
    try:
        client.test_connection()
    except redis.ConnectionError as ex:
        logger.error(str(ex))
        sys.stderr.write(f'{str(ex)}\n')
        return 1

    server = ThreadedServer(JarvisService, port=port)

    dt_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_info = f"{dt_str}# JARVIS started, listening to port {port}."
    logger.info(start_info)

    server.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
