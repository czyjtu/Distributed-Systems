import socket 
from concurrent.futures import ThreadPoolExecutor
import threading 
import logging 
from constants import FORMAT, HEADER, DISCONNECT_MSG
import signal 
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Server:
    def __init__(self, port):
        self.host =  socket.gethostbyname(socket.gethostname())
        self.address = (self.host, port)


    def start(self, max_threads=3):
        print("Server starting ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self._socket = s
            signal.signal(signal.SIGINT, self._cleanup)
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
            received_len_msg = conn.recv(HEADER).decode(FORMAT)
            try:
                msg_len = int(received_len_msg)
            except ValueError:
                logger.warn(f"Invalid message: {received_len_msg}. Expected message length")
                continue 

            msg = conn.recv(msg_len).decode(FORMAT)
            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MSG:
                connected = False
            conn.send("Msg received".encode(FORMAT))
        print("DISCONNECTED FROM CLIENT")

    def _cleanup(self, sig, frame):
        self._socket.close()
        print("SHUTTING DOWN")
        sys.exit(0)
