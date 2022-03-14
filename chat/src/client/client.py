import logging 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import socket 
from constants import FORMAT, HEADER, DISCONNECT_MSG, MSG_LEN
import signal 
import sys
from common.message import Message
from common.msg_type import MsgType
import pickle 
import threading 

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
            self.fetch_username()

            self.tcp_listen_thread = threading.Thread(target=self.receive_msg, args=(s, ))
            self.tcp_listen_thread.start()
            while True:                
                msg = self.fetch_msg()
                if msg:
                    self.send_message(msg, s)

    def fetch_username(self) -> str:
        while True:
            name = input("Enter username: ")
            msg = Message(name, MsgType.REGISTER)
            self._socket.send(pickle.dumps(msg))
            received = self._socket.recv(MSG_LEN)
            msg = pickle.loads(received)
            if msg.type == MsgType.ACK:
                break 
        self.id = name 



    def send_message(self, msg, s):
        s.send(msg)
    
    def fetch_msg(self):
        msg = input()
        return pickle.dumps(Message(self.id, MsgType.TEXT, msg)) if msg else None

    def receive_msg(self, s) -> Message:
        s.setblocking(True)
        while True:
            received = pickle.loads(s.recv(MSG_LEN))
            if received:
                self.display_msg(received)

    def display_msg(self, msg):
        print(f"{msg.author}: {msg.text}")

    def _cleanup(self, sig, frame):
        msg = Message(self.id, MsgType.DISCONNECT)
        self.send_message(pickle.dumps(msg), self._socket)
        print("SHUTTING DOWN")
        sys.exit(0)

 
    def _start_log(self):
        print("press 'ctr + c' to stop")
        logger.info(f"client {self.name} started")
