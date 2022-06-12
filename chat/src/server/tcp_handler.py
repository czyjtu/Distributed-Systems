import logging
from constants import MSG_LEN 
import pickle 
from common import MsgType, Message  
from common.stoppable_thread import StoppableThread
logger = logging.getLogger(__name__)
import sys


class TCPUserHandler(StoppableThread):
    def __init__(self, name, sock, register: dict):
        super().__init__(self)
        self.id = name 
        self._socket = sock 
        self.register = register 
        self._socket.setblocking(True)

        
    def run(self):
        logger.info(f"[{self.id}] running ...")
        self._socket.settimeout(60)
        while not self.stopped():
            try:
                received = self._socket.recv(MSG_LEN)
            except ConnectionError as e:
                logger.error(e)
                break
            msg = pickle.loads(received)
            logger.info(f"got message {msg}")
            self.handle_message(msg)
        self._socket.close()
        logger.info(f"DISCONNECTED FROM CLIENT {self._socket}")
        sys.exit(0)


    def handle_message(self, msg: Message):
        if msg.type == MsgType.REGISTER or msg.author not in self.register:
            self.register_client(msg)
        elif msg.type == MsgType.TEXT:
            self.broadcast(msg)
        elif msg.type == MsgType.DISCONNECT:
            self.stop()
        else:
            logger.info(f"Don't know how to handle message of type {msg.type}")
    
    def register_client(self, msg):
        logger.info(f"registering new client {self._socket}")
        if msg.author not in self.register:
            self.register[msg.author] = self._socket
            response = Message(self.id, MsgType.ACK)
        else:
            response = Message(self.id, MsgType.NACK)
        logger.info(f"responding with {response}")
        self._socket.send(pickle.dumps(response))

    def broadcast(self, msg):
        for client_id, client_socket in self.register.items():
            if client_id == msg.author:
                continue 
            client_socket.send(pickle.dumps(msg))
            print(f"message sent to {client_id}")
        