import logging
import grpc
from concurrent import futures
from server.repository import MessageRepository
from server.group_manager import GroupManager
from server.const import PORT_NUMBER
import gen.chat_pb2_grpc as chat_pb2_grpc
from gen.chat_pb2 import StatusResponse


def serve():
    options = [
        # ('grpc.keepalive_time_ms', 10000),
        # # send keepalive ping every 10 second, default is 2 hours
        # ('grpc.keepalive_timeout_ms', 5000),
        # # keepalive ping time out after 5 seconds, default is 20 seoncds
        # ('grpc.keepalive_permit_without_calls', True),
        # # allow keepalive pings when there's no gRPC calls
        # ('grpc.http2.max_pings_without_data', 0),
        # # allow unlimited amount of keepalive pings without data
        # ('grpc.http2.min_time_between_pings_ms', 10000),
        # # allow grpc pings from client every 10 seconds
        # ('grpc.http2.min_ping_interval_without_data_ms',  5000),
        # # allow grpc pings from client without data every 5 seconds

    ]

    repo = MessageRepository()
    servicer = GroupManager(repo)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    chat_pb2_grpc.add_GroupManagerServicer_to_server(servicer=servicer, server=server)

    server.add_insecure_port(f'[::]:{PORT_NUMBER}')
    server.start()
    print("[Info] Server started successfully")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="")
    serve()