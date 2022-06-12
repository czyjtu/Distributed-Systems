import threading 
import logging
from constants import MSG_LEN 
import pickle 
from common import MsgType, Message
from common.stoppable_thread import StoppableThread
import sys
 
logger = logging.getLogger(__name__)


class TCPListener(StoppableThread):
    def __init__(self, sock, msg_writer):
        super().__init__(self)
        self._socket = sock
        self._writer = msg_writer

    def run(self):
        logger.info(f"Starting ...")
        self.listen_for_messages()
        sys.exit(0)

    def listen_for_messages(self) -> Message:
        self._socket.setblocking(True)
        while not self.stopped():
            try:
                received = self._socket.recv(MSG_LEN)
                msg = pickle.loads(received)
            except (ConnectionError, EOFError) as e:
                logger.error(e)
                break
            logger.debug(f"Received message {msg}")
            self._writer.display(msg)
