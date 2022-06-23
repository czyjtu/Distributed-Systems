from gen.demo_pb2 import Response
from gen.demo_pb2_grpc import helloServicer, add_helloServicer_to_server

from concurrent import futures
import grpc


class Hello(helloServicer):
    def SayHello(self, request, context):
        return Response(
            text="siema"
        )


def serve():
    # with open("/etc/ssl/certs/nginx-demo.key", "rb") as f:
    #     private_key = f.read()
    # with open("/etc/ssl/certs/nginx-demo.crt", "rb") as f:
    #     crt = f.read()

    # server_credentials = grpc.ssl_server_credentials(((private_key, crt),))

    PORT = 8081
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_helloServicer_to_server(Hello(), server)
    server.add_insecure_port(f"[::]:{PORT}")

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
