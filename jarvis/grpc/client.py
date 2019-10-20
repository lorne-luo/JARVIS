import grpc
from environs import Env

from .sms import sms_pb2
from .sms import sms_pb2_grpc

env = Env()
env.read_env()

JARVIS_HOST = env.str('JARVIS_HOST', default='localhost')
JARVIS_PORT = env.int('JARVIS_PORT', default=50051)
JARVIS_SERVER = f'{JARVIS_HOST}:{JARVIS_PORT}'


def sms_admin(message, app):
    with grpc.insecure_channel(JARVIS_SERVER) as channel:
        stub = sms_pb2_grpc.SMSStub(channel)
        response = stub.SMSAdmin(sms_pb2.AuAdminSMSRequest(message=message, app=app))
    print(f"SMS client received: {response}")
