import logging
from constants import MSG_LEN 
import pickle 
from common import MsgType, Message  
logger = logging.getLogger(__name__)

class TCPHandler:
    def __init__(self, name, sock, register: dict):
        self.id = name 
        self._socket = sock 
        self.register = register 
        
    def run(self):
        logger.info(f"[{self.id}] running ...")
        self._socket.setblocking(True)
        connected = True 
        while connected:
            received = self._socket.recv(MSG_LEN)
            msg = pickle.loads(received)
            logger.info(f"got message {msg}")

            if msg.type == MsgType.REGISTER or msg.author not in self.register:
                self.register_client(msg)
            elif msg.type == MsgType.TEXT:
                self.broadcast(msg)
            elif msg.type == MsgType.DISCONNECT:
                connected = False
            else:
                pass 
        logger.info(f"DISCONNECTED FROM CLIENT {self._socket}")
    
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
        