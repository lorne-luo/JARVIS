import logging

from . import sms_pb2
from . import sms_pb2_grpc
from ...aliyun.sms.service import send_aliyun_sms
from ...sms import send_to_admin, send_au_sms

logger = logging.getLogger(__name__)


class SMS(sms_pb2_grpc.SMSServicer):

    def SMSAdmin(self, request, context):
        try:
            success, detail = send_to_admin(request.message, request.app)
        except Exception as ex:
            logger.error(f'[SMSAdmin] {ex}, message={request.message}')
            return sms_pb2.AuSMSResponse(success=False, detail=str(ex))
        return sms_pb2.AuSMSResponse(success=success, detail=detail)

    def SMSAu(self, request, context):
        try:
            success, detail = send_au_sms(request.mobile_number, request.message, request.app)
        except Exception as ex:
            logger.error(f'[SMSAu] {ex}, mobile_number={request.mobile_number}, message={request.message}')
            return sms_pb2.AuSMSResponse(success=False, detail=str(ex))
        return sms_pb2.AuSMSResponse(success=success, detail=detail)

    def SMSAliyun(self, request, context):
        try:
            success, detail = send_aliyun_sms(request.business_id, request.mobile_numbers, request.template_code,
                                              request.template_param, request.app)
        except Exception as ex:
            logger.error(
                f'[SMSAliyun] {ex}, business_id={request.business_id}, mobile_numbers={request.mobile_numbers}, template_code={request.template_code}, template_param={request.template_param}')
            return sms_pb2.AliyunSMSResponse(success=False, detail=str(ex))
        return sms_pb2.AliyunSMSResponse(success=success, detail=str(detail))
