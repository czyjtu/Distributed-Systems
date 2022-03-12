import socket 
from concurrent.futures import ThreadPoolExecutor
import threading 
import logging 
from constants import FORMAT, HEADER, DISCONNECT_MSG

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Server:
    def __init__(self, port):
        self.host =  socket.gethostbyname(socket.gethostname())
        self.address = (self.host, port)


    def start(self, max_threads=3):
        print("Server starting ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.address)
            s.listen()
            print("Serve listening ...")
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()


    def handle_client(self, conn, addr):
        print(f"Conneted to client {addr}")
        connected  = True 
        while connected:
            msg_len = int(conn.recv(HEADER).decode(FORMAT))
            msg = conn.recv(msg_len).decode(FORMAT)

            print(f"[{addr}] {msg}")

            if msg == DISCONNECT_MSG:
                connected = False
            conn.send("Msg received".encode(FORMAT))
