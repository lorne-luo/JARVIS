import inspect
import logging
import sys
from datetime import datetime

import click
import redis
import rpyc
from rpyc.utils.server import ThreadedServer

from jarvis import config
from jarvis.redis_client import client
from jarvis.sms import send_to_admin
from sms import send_au_sms
from telegram.bot import telegram_admin

logger = logging.getLogger(__name__)


class JarvisService(rpyc.Service):

    def exposed_add(self, a, b):
        print(inspect.stack()[0][3])
        return a + b

    # =================================== SMS =================================
    def exposed_sms_au(self, to, text, from_app):
        try:
            logger.info(f'sms_au from {from_app}: {to} @ {text}')
            return send_au_sms(to, text)
        except Exception as ex:
            logger.error(f'[{inspect.stack()[0][3]}] {ex}, text={text}')

    def exposed_sms_to_admin(self, text, from_app):
        try:
            logger.info(f'sms_to_admin from {from_app}: {text}')
            return send_to_admin(text)
        except Exception as ex:
            logger.error(f'[{inspect.stack()[0][3]}] {ex}, text={text}')

    def exposed_config(self):
        try:
            return config.__dict__
        except Exception as ex:
            logger.error(f'[{inspect.stack()[0][3]}] {ex}')


@click.command()
@click.option('--port', default=54321, help='Port of JARVIS service')
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
    start_info = f"{dt_str}# JARVIS started."
    logger.info(start_info)

    server.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
