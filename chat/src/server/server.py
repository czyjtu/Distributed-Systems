import socket 
from concurrent.futures import ThreadPoolExecutor
import threading 
import logging
from typing import Optional 
from constants import FORMAT, HEADER, DISCONNECT_MSG
import signal 
import sys
import pickle

from common.message import Message
from common.msg_type import MsgType 


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Server:
    def __init__(self, port):
        self.host =  socket.gethostbyname(socket.gethostname())
        self.address = (self.host, port)
        self.clients: dict[str, socket.socket] = dict()


    def start(self, max_threads=3):
        print("Server starting ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            signal.signal(signal.SIGINT, self._cleanup)
            self._socket = s
            self._socket.setblocking(False)
            s.bind(self.address)
            s.listen()
            print("Server listening ...")
            self.threads = []
            while True:
                try: 
                    conn, addr = s.accept()
                except BlockingIOError:
                    continue
                self.clients[addr] = conn
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                self.threads.append(thread)


    def handle_client(self, conn, addr):
        print(f"Conneted to client {addr}")
        conn.setblocking(True)
        connected = True 
        while connected:
            received_len_msg = conn.recv(HEADER).decode(FORMAT)
            try:
                msg_len = int(received_len_msg)
            except ValueError:
                logger.warn(f"Invalid message: {received_len_msg}. Expected message length")
                continue 

            msg = pickle.loads(conn.recv(msg_len))
            print(f"[{addr}] {msg}")
            if msg.type == MsgType.DISCONNECT:
                connected = False
            elif msg.type == MsgType.TEXT:
                self._direct_others(conn, msg)
        print("DISCONNECTED FROM CLIENT")

    def _direct_others(self, sender_socket, msg):
        for client_id, client in self.clients.items():
            if client == sender_socket:
                continue 
            msg.author = client_id
            client.send(pickle.dumps(msg))
            print(f"message sent to {client_id}")

    def _accept_client(self, s) -> Optional[tuple]:
        try: 
            conn, addr = s.accept()
        except BlockingIOError:
            return 

    def _cleanup(self, sig, frame):
        self._socket.close()
        for i, th in enumerate(self.threads):
            print(f"thread {i} joined: {th.join()}")
        print("SHUTTING DOWN")
        sys.exit(0)
