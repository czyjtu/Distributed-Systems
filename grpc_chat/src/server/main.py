import grpc
from concurrent import futures
from server.repository import MessageRepository
from server.server import GroupManager
from server.const import PORT_NUMBER
import gen.chat_pb2_grpc as chat_pb2_grpc
from gen.chat_pb2 import StatusResponse


def serve():
    repo = MessageRepository()
    servicer = GroupManager(repo)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_GroupManagerServicer_to_server(servicer=servicer, server=server)

    server.add_insecure_port(f'[::]:{PORT_NUMBER}')
    server.start()
    print("[Info] Server started successfully")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()