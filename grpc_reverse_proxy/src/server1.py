from gen.cv_pb2 import NpArray
from gen.cv_pb2_grpc import EdgeDetectionServicer, add_EdgeDetectionServicer_to_server

from concurrent import futures
import grpc
import numpy as np 
import cv2 
import pickle 
import matplotlib.pyplot as plt 


class Canny(EdgeDetectionServicer):
    def canny(self, request: NpArray, context):
        print("got request")
        data = np.frombuffer(
            request.data, np.float32
        )
        img = data.reshape((request.rows, request.cols)).astype(np.uint8)
        edges = cv2.Canny(img, 0.1, 0.5)
        print(img.shape)
        response = NpArray(
            data=edges.reshape(-1).astype(np.float32).tobytes(),
            rows=edges.shape[0],
            cols=edges.shape[1]
        )
        print("sending response")
        return response 


def serve():
    PORT = 8081
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_EdgeDetectionServicer_to_server(Canny(), server)
    server.add_insecure_port(f"[::]:{PORT}")

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
