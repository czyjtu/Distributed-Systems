import threading 
import logging
from constants import MSG_LEN 
import pickle 
from common import MsgType, Message
from common.stoppable_thread import StoppableThread
import sys
 
logger = logging.getLogger(__name__)


class UDPListener(StoppableThread):
    def __init__(self, sock, msg_writer, addr):
        super().__init__(self)
        self._socket = sock
        self._writer = msg_writer
        self.addr = addr

    def run(self):
        logger.info(f"Starting ...")
        self.listen_for_messages()
        sys.exit(0)

    def listen_for_messages(self) -> Message:
        self._socket.setblocking(True)
        while True:
            if self.stopped():
                return
            try:
                received, addr = self._socket.recvfrom(MSG_LEN)
            except ConnectionError as e:
                logger.error(e)
                break
            msg = pickle.loads(received)
            logger.debug(f"Received message {msg}")
            self._writer.display(msg)
