from gen.demo_pb2 import Response
from gen.demo_pb2_grpc import greetingsServicer, add_greetingsServicer_to_server

from concurrent import futures
import grpc


class Greeter(greetingsServicer):
    def Greetings(self, request, context):
        return Response(
            text="pozdrawiam"
        )


def serve():
    # server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
    PORT = 8082
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_greetingsServicer_to_server(Greeter(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()