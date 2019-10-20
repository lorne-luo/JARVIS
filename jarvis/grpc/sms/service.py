from . import sms_pb2
from . import sms_pb2_grpc
from ...aliyun.sms.service import send_aliyun_sms
from ...sms import send_to_admin, send_au_sms


class SMS(sms_pb2_grpc.SMSServicer):

    def SMSAdmin(self, request, context):
        success, detail = send_to_admin(request.message, request.app)
        return sms_pb2.AuSMSResponse(success=success, detail=detail)

    def SMSAu(self, request, context):
        success, detail = send_au_sms(request.mobile_number, request.message, request.app)
        return sms_pb2.AuSMSResponse(success=success, detail=detail)

    def SMSAliyun(self, request, context):
        success, detail = send_aliyun_sms(request.business_id, request.mobile_numbers, request.template_code,
                                          request.template_param, request.app)
        return sms_pb2.AliyunSMSResponse(success=success, detail=str(detail))
