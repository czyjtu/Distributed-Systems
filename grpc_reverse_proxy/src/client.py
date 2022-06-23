import grpc, sys
from gen.demo_pb2_grpc import helloStub, greetingsStub
from gen.demo_pb2 import Empty

def call_server1(stub):
    response = stub.SayHello(Empty())
    print(f"Server1: {response}")


def call_server2(stub):
    response = stub.Greetings(Empty())
    print(f"Server2: {response}")


if __name__ == '__main__':
    server_id = int(sys.argv[1])
    print(f"Server id {server_id}")
    with grpc.insecure_channel(f'localhost:8080') as channel:
        if server_id == 1:
            stub = helloStub(channel)
            call_server1(stub)

        elif server_id == 2:
            stub = greetingsStub(channel)
            call_server2(stub)
