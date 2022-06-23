from gen.cv_pb2 import NpArray, KmeansRequest
from gen.cv_pb2_grpc import SegmentationServicer, add_SegmentationServicer_to_server

from concurrent import futures
import grpc
import numpy as np 
import cv2 

class Kmeans(SegmentationServicer):
    def kmeans(self, request: KmeansRequest, context):
        print("got request")
        data = np.frombuffer(
            request.img.data, np.float32
        )
        img = data.reshape((request.img.rows, request.img.cols)).astype(np.float32)
        img_2d = img.reshape((-1, 2))
        print(img_2d.shape)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 3
        attempts=10

        ret,label,center=cv2.kmeans(img_2d,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        result_image = res.reshape((img.shape))

        print(result_image.shape)
        response = NpArray(
            data=result_image.reshape(-1).astype(np.float32).tobytes(),
            rows=result_image.shape[0],
            cols=result_image.shape[1]
        )
        print("sending response")
        return response 


def serve():
    PORT = 8082
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SegmentationServicer_to_server(Kmeans(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()