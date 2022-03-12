import logging 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import socket 
from constants import FORMAT, HEADER, DISCONNECT_MSG


class Client:

    def __init__(self, client_name, server_ip, server_port):
        self.address = (server_ip, server_port)
        self.name = client_name

    def start(self):
        self._start_log()
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.address)
                
                msg = self.fetch_msg()
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
 
    def _start_log(self):
        print("press 'ctr + c' to stop")
        logger.info(f"client {self.name} started")
