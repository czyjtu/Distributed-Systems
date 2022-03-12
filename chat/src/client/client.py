import logging 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import socket 
from constants import FORMAT, HEADER, DISCONNECT_MSG
import signal 
import sys

class Client:

    def __init__(self, client_name, server_ip, server_port):
        self.address = (server_ip, server_port)
        self.name = client_name

    def start(self):
        self._start_log()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self._socket = s
            signal.signal(signal.SIGINT, self._cleanup)
            s.connect(self.address)
            while True:                
                msg = self.fetch_msg()
                if msg:
                    self.send_message(msg, s)
                    print(f"<< {s.recv(1024).decode(FORMAT)}")

    def send_message(self, msg, s):
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        s.send(send_length)
        s.send(msg)
    
    def fetch_msg(self):
        msg = input(">> ")
        msg_encoded = msg.encode(FORMAT)
        return msg_encoded

    def _cleanup(self, sig, frame):
        self.send_message(DISCONNECT_MSG.encode(FORMAT), self._socket)
        print("SHUTTING DOWN")
        sys.exit(0)

 
    def _start_log(self):
        print("press 'ctr + c' to stop")
        logger.info(f"client {self.name} started")
