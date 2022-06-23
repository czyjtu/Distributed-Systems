import grpc, sys
from gen.cv_pb2_grpc import EdgeDetectionStub, SegmentationStub
from gen.demo_pb2_grpc import helloStub, greetingsStub
from gen.cv_pb2 import NpArray, KmeansRequest
import numpy as np 
import matplotlib.pyplot as plt 
import cv2 


def display_multiple(images, rows = 1, cols=1, figsize=(15, 15), titles=None):
    figure, ax = plt.subplots(nrows=rows,ncols=cols, figsize=figsize)
    for ind,title in enumerate(images):
        ax.ravel()[ind].imshow(title, cmap='gray')
        ax.ravel()[ind].set_axis_off()
        if titles:
            ax.ravel()[ind].set_title(titles[ind])
    plt.tight_layout()
    plt.show()


def read_img(path):
    plansza = cv2.imread(path)  
    plansza = cv2.cvtColor(plansza, cv2.COLOR_BGR2GRAY) 
    return np.array(plansza, np.float32)



def call_canny(stub, img: np.ndarray):
    request = NpArray(
        data=np.array(img, dtype=np.float32).reshape(-1).tobytes(),
        rows=img.shape[0],
        cols=img.shape[1]
    )
    response = stub.canny(request)
    result_img = np.frombuffer(response.data, dtype=np.float32).reshape(img.shape)
    display_multiple([img, result_img], 1, 2)


def call_kmeans(stub, img: np.ndarray):
    np_array = NpArray(
        data=np.array(img, dtype=np.float32).reshape(-1).tobytes(),
        rows=img.shape[0],
        cols=img.shape[1]
    )
    request = KmeansRequest(
        img=np_array,
        k=3
    )
    response = stub.kmeans(request)
    result_img = np.frombuffer(response.data, dtype=np.float32).reshape(img.shape)
    display_multiple([img, result_img], 1, 2)


def call_server2(stub):
    response = stub.Greetings(Empty())
    print(f"Server2: {response}")


if __name__ == '__main__':
    server_id = int(sys.argv[1])
    print(f"Server id {server_id}")

    img = read_img("resources/umbrella.png")
    print(img.shape)

    with grpc.insecure_channel(f'localhost:8080') as channel:
        if server_id == 1:
            stub = EdgeDetectionStub(channel)
            call_canny(stub, img)

        elif server_id == 2:
            stub = SegmentationStub(channel)
            call_kmeans(stub, img)
