import threading 
import logging
import pickle 
from common import Message, MsgType
from constants import MSG_LEN, DISCONNECT_MSG
from common.stoppable_thread import StoppableThread
logger = logging.getLogger(__name__)


class InputHandler(StoppableThread):
    def __init__(self, sock, dgram, server_addr, name):
        super().__init__(self)
        self._socket = sock 
        self._dgram_socket = dgram
        self.serv_addr = server_addr
        self.id = name 

    def run(self):
        logger.debug(f"running ...")
        while not self.stopped():                
            msg = self.fetch_msg()
            if msg:
                self.send_message(msg)

    def send_message(self, msg):
        logger.debug(f"sending msg to {self._socket}: {msg}")
        try:
            self._socket.send(msg)
        except ConnectionError:
            logger.error(f"message can't be sent due to broken connection")
            self.stop()

    def send_udp(self, msg):
        self._dgram_socket.send

    def fetch_msg(self):
        try:
            msg = input()
        except EOFError:
            return None 
        if not msg:
            return None 
        if msg == DISCONNECT_MSG:
            self.stop()
            return pickle.dumps(Message(self.id, MsgType.DISCONNECT, msg))
        if msg.startswith('--U'):
            msg = pickle.dumps(Message(self.id, MsgType.TEXT, msg[3:]))
            self._dgram_socket.sendto(msg, self.serv_addr)
            return None
        return pickle.dumps(Message(self.id, MsgType.TEXT, msg)) 
