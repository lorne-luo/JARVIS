# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import sms_pb2 as sms__pb2


class SMSStub(object):
  """=== Service ===
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SMSAdmin = channel.unary_unary(
        '/jarvis.sms.SMS/SMSAdmin',
        request_serializer=sms__pb2.AuAdminSMSRequest.SerializeToString,
        response_deserializer=sms__pb2.AuSMSResponse.FromString,
        )
    self.SMSAu = channel.unary_unary(
        '/jarvis.sms.SMS/SMSAu',
        request_serializer=sms__pb2.AuSMSRequest.SerializeToString,
        response_deserializer=sms__pb2.AuSMSResponse.FromString,
        )
    self.SMSCn = channel.unary_unary(
        '/jarvis.sms.SMS/SMSCn',
        request_serializer=sms__pb2.CnSMSRequest.SerializeToString,
        response_deserializer=sms__pb2.CnSMSResponse.FromString,
        )


class SMSServicer(object):
  """=== Service ===
  """

  def SMSAdmin(self, request, context):
    """AU SMS
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SMSAu(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SMSCn(self, request, context):
    """CN SMS
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SMSServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SMSAdmin': grpc.unary_unary_rpc_method_handler(
          servicer.SMSAdmin,
          request_deserializer=sms__pb2.AuAdminSMSRequest.FromString,
          response_serializer=sms__pb2.AuSMSResponse.SerializeToString,
      ),
      'SMSAu': grpc.unary_unary_rpc_method_handler(
          servicer.SMSAu,
          request_deserializer=sms__pb2.AuSMSRequest.FromString,
          response_serializer=sms__pb2.AuSMSResponse.SerializeToString,
      ),
      'SMSCn': grpc.unary_unary_rpc_method_handler(
          servicer.SMSCn,
          request_deserializer=sms__pb2.CnSMSRequest.FromString,
          response_serializer=sms__pb2.CnSMSResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'jarvis.sms.SMS', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
