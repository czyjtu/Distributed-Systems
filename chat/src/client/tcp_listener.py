import threading 
import logging
from constants import MSG_LEN 
import pickle 
from common import MsgType, Message
from common.stoppable_thread import StoppableThread
 
logger = logging.getLogger(__name__)


class TCPListener(threading.Thread):
    def __init__(self, sock, msg_writer, lock):
        threading.Thread.__init__(self)

        self._socket = sock
        self._writer = msg_writer
        self._lock = lock 

    def run(self):
        logger.info(f"Starting ...")
        self.receive_msg()

    def receive_msg(self) -> Message:
        self._socket.setblocking(True)
        while True:
            self._lock.acquire()
            received = pickle.loads(self._socket.recv(MSG_LEN))
            self.lock.release()
            logger.debug(f"Received message {received}")
            self._writer.display(received)
