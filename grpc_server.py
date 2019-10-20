import logging
import sys
from concurrent import futures

import click
import grpc
import redis

from jarvis.grpc.sms import sms_pb2_grpc
from jarvis.grpc.sms.service import SMS
from jarvis.redis_client import client as redis_client

logger = logging.getLogger(__name__)


@click.command()
@click.option('--port', default=50051, help='Port of JARVIS service')
def main(port):
    # test redis connection
    try:
        redis_client.test_connection()
    except redis.ConnectionError as ex:
        logger.error(str(ex))
        sys.stderr.write(f'{str(ex)}\n')
        return 1

    # grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

    sms_pb2_grpc.add_SMSServicer_to_server(SMS(), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    sys.exit(main())
