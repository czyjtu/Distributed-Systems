# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gen.chat_pb2 as chat__pb2


class GroupManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.JoinGroup = channel.unary_unary(
                '/GroupManager/JoinGroup',
                request_serializer=chat__pb2.JoinRequest.SerializeToString,
                response_deserializer=chat__pb2.StatusResponse.FromString,
                )
        self.GetMessages = channel.unary_stream(
                '/GroupManager/GetMessages',
                request_serializer=chat__pb2.GetMessagesRequest.SerializeToString,
                response_deserializer=chat__pb2.ChatMessage.FromString,
                )
        self.SendMessage = channel.unary_unary(
                '/GroupManager/SendMessage',
                request_serializer=chat__pb2.ChatMessage.SerializeToString,
                response_deserializer=chat__pb2.StatusResponse.FromString,
                )


class GroupManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def JoinGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GroupManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'JoinGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinGroup,
                    request_deserializer=chat__pb2.JoinRequest.FromString,
                    response_serializer=chat__pb2.StatusResponse.SerializeToString,
            ),
            'GetMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMessages,
                    request_deserializer=chat__pb2.GetMessagesRequest.FromString,
                    response_serializer=chat__pb2.ChatMessage.SerializeToString,
            ),
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=chat__pb2.ChatMessage.FromString,
                    response_serializer=chat__pb2.StatusResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'GroupManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GroupManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def JoinGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/GroupManager/JoinGroup',
            chat__pb2.JoinRequest.SerializeToString,
            chat__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/GroupManager/GetMessages',
            chat__pb2.GetMessagesRequest.SerializeToString,
            chat__pb2.ChatMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/GroupManager/SendMessage',
            chat__pb2.ChatMessage.SerializeToString,
            chat__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
