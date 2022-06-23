# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gen.cv_pb2 as cv__pb2


class EdgeDetectionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.canny = channel.unary_unary(
                '/cv.EdgeDetection/canny',
                request_serializer=cv__pb2.NpArray.SerializeToString,
                response_deserializer=cv__pb2.NpArray.FromString,
                )


class EdgeDetectionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def canny(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EdgeDetectionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'canny': grpc.unary_unary_rpc_method_handler(
                    servicer.canny,
                    request_deserializer=cv__pb2.NpArray.FromString,
                    response_serializer=cv__pb2.NpArray.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cv.EdgeDetection', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EdgeDetection(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def canny(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cv.EdgeDetection/canny',
            cv__pb2.NpArray.SerializeToString,
            cv__pb2.NpArray.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class SegmentationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.kmeans = channel.unary_unary(
                '/cv.Segmentation/kmeans',
                request_serializer=cv__pb2.KmeansRequest.SerializeToString,
                response_deserializer=cv__pb2.NpArray.FromString,
                )


class SegmentationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def kmeans(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SegmentationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'kmeans': grpc.unary_unary_rpc_method_handler(
                    servicer.kmeans,
                    request_deserializer=cv__pb2.KmeansRequest.FromString,
                    response_serializer=cv__pb2.NpArray.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cv.Segmentation', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Segmentation(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def kmeans(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cv.Segmentation/kmeans',
            cv__pb2.KmeansRequest.SerializeToString,
            cv__pb2.NpArray.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)