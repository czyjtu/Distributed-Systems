import threading 
import logging
import pickle 
from common import Message, MsgType
from constants import MSG_LEN
from common.stoppable_thread import StoppableThread
logger = logging.getLogger(__name__)


class InputHandler(threading.Thread):
    def __init__(self, sock, lock, name):
        threading.Thread.__init__(self)

        self._socket = sock 
        self._lock = lock
        self.id = name 

    def run(self):
        logger.debug(f"running ...")
        while True:                
            msg = self.fetch_msg()
            if msg:
                self.send_message(msg)

    def send_message(self, msg):
        logger.debug(f"sending msg to {self._socket}: {msg}")
        self._lock.acquire()
        self._socket.send(msg)
        self._lock.release()

    def fetch_msg(self):
        msg = input()
        return pickle.dumps(Message(self.id, MsgType.TEXT, msg)) if msg else None
