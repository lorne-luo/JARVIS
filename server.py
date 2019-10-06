import inspect
import logging
import sys

import click
import rpyc
from rpyc.utils.server import ThreadedServer

from jarvis import config
from jarvis.sms import send_to_admin

logger = logging.getLogger(__name__)


class JarvisService(rpyc.Service):

    def exposed_add(self, a, b):
        print(inspect.stack()[0][3])
        return a + b

    def exposed_sms_to_admin(self, text):
        try:
            logger.debug(f'send_to_admin: {text}')
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
    click.echo("JARVIS starting..")
    server = ThreadedServer(JarvisService, port=port)
    server.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
