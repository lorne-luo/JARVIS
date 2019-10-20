from . import sms_pb2
from . import sms_pb2_grpc


class SMS(sms_pb2_grpc.SMSServicer):

    def SMSAdmin(self, request, context):
        # todo send
        return sms_pb2.AuSMSResponse(success=True, detail=f'Hello, {request.message}!')

