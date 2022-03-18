import logging
from client.input_listener import InputHandler
from client.tcp_listener import TCPListener 
from client.udp_listener import UDPListener 

import socket 
from constants import FORMAT, HEADER, DISCONNECT_MSG, MSG_LEN
import signal 
import sys
from common import Message, MsgType 
import pickle 
from client.message_writer import MsgWritter
import threading 
from termcolor import colored
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Client:
    def __init__(self, client_name, server_ip, server_port):
        self.address = (server_ip, server_port)
        self.name = client_name
        self.msg_writer = MsgWritter()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_listener = TCPListener(self._socket, self.msg_writer)

        # self.input_handler = InputHandler(self._socket, self.id)
        signal.signal(signal.SIGINT, self._cleanup)
        self.id = None
        self.input_handler = None 

        self.dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_listener = UDPListener(self.dgram_socket, self.msg_writer, self.address)

    def start(self):
        self._start_log()
        self._socket.connect(self.address)


        self.fetch_username()
        self.input_handler = InputHandler(self._socket, self.dgram_socket, self.address, self.id)

        self.tcp_listener.start()
        # self.udp_listener.start()
        self.input_handler.start()

    def fetch_username(self) -> str:
        while True:
            name = input(colored("Enter username: ", "green"))
            msg = Message(name, MsgType.REGISTER)
            self._socket.send(pickle.dumps(msg))
            received = self._socket.recv(MSG_LEN)
            response = pickle.loads(received)
            if response.type == MsgType.ACK:
                break
        self.id = name 


    def display_msg(self, msg):
        print(f"{msg.author}: {msg.text}")

    def _cleanup(self, sig, frame):
        # self._socket.close()
        if self.tcp_listener:
            self.tcp_listener.stop()
        if self.input_handler:
            self.input_handler.stop()
        if self.udp_listener:
            self.udp_listener.stop()
        print("SHUTTING DOWN")

 
    def _start_log(self):
        print("press 'ctr + c' to stop")
        logger.info(f"client {self.name} started")
