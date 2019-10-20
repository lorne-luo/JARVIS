import grpc
from environs import Env

from .sms import sms_pb2
from .sms import sms_pb2_grpc

env = Env()
env.read_env()

JARVIS_HOST = env.str('JARVIS_HOST', default='localhost')
JARVIS_PORT = env.int('JARVIS_PORT', default=54321)
JARVIS_SERVER = f'{JARVIS_HOST}:{JARVIS_PORT}'


def sms_admin(message, app=None):
    with grpc.insecure_channel(JARVIS_SERVER) as channel:
        stub = sms_pb2_grpc.SMSStub(channel)
        response = stub.SMSAdmin(sms_pb2.AuAdminSMSRequest(message=message, app=app))
        return response.success,response.detail


def sms_au(mobile_number, message, app=None):
    with grpc.insecure_channel(JARVIS_SERVER) as channel:
        stub = sms_pb2_grpc.SMSStub(channel)
        response = stub.SMSAu(sms_pb2.AuSMSRequest(mobile_number=mobile_number, message=message, app=app))
    return response.success, response.detail


def sms_aliyun(business_id, mobile_numbers, template_code, template_param, app=None):
    with grpc.insecure_channel(JARVIS_SERVER) as channel:
        stub = sms_pb2_grpc.SMSStub(channel)
        response = stub.SMSAliyun(
            sms_pb2.AliyunSMSRequest(business_id=business_id,
                                     mobile_numbers=mobile_numbers,
                                     template_code=template_code,
                                     template_param=template_param, app=app))
    return response.success, response.detail
