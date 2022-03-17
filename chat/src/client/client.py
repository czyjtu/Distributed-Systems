import logging
from client.input_listener import InputHandler
from client.tcp_listener import TCPListener 
import socket 
from constants import FORMAT, HEADER, DISCONNECT_MSG, MSG_LEN
import signal 
import sys
from common import Message, MsgType 
import pickle 
from client.message_writer import MsgWritter
import threading 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Client:

    def __init__(self, client_name, server_ip, server_port):
        self.address = (server_ip, server_port)
        self.name = client_name
        self.msg_writer = MsgWritter()
        self.id = None
        self.tcp_listener = None 
        self.input_hendler = None 

    def start(self):
        self._start_log()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self._socket = s
            signal.signal(signal.SIGINT, self._cleanup)
            s.connect(self.address)
            self.fetch_username()

            sock_lock = threading.RLock()
            self.tcp_listener = TCPListener(self._socket, self.msg_writer, sock_lock)
            self.input_handler = InputHandler(self._socket, sock_lock, self.id)

            self.tcp_listener.start()
            self.input_handler.start()

            self.tcp_listener.join()
            self.input_handler.join()


    def fetch_username(self) -> str:
        while True:
            name = input("Enter username: ")
            msg = Message(name, MsgType.REGISTER)
            self._socket.send(pickle.dumps(msg))
            print("sent")
            received = self._socket.recv(MSG_LEN)
            response = pickle.loads(received)
            if response.type == MsgType.ACK:
                break
        self.id = name 


    def display_msg(self, msg):
        print(f"{msg.author}: {msg.text}")

    def _cleanup(self, sig, frame):
        if self.tcp_listener:
            self.tcp_listener.kill()
        if self.input_handler:
            self.input_handler.kill()
        print("SHUTTING DOWN")
        sys.exit(0)

 
    def _start_log(self):
        print("press 'ctr + c' to stop")
        logger.info(f"client {self.name} started")
