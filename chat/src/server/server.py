import socket 
import threading 
import logging
import signal 
import sys
from server.tcp_handler import TCPHandler 


logger = logging.getLogger('SERVER')
logger.setLevel(logging.DEBUG)


class Server:
    def __init__(self, port):
        self.host =  socket.gethostbyname(socket.gethostname())
        self.address = (self.host, port)
        self.clients_register: dict[str, socket.socket] = dict()
        self.tcp_handlers = dict()
        self.threads = []


    def start(self, max_threads=3):
        logger.info("starting ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            signal.signal(signal.SIGINT, self._cleanup)
            self._socket = s
            self._socket.setblocking(False)
            s.bind(self.address)
            s.listen()
            self.listen()

    def listen(self):
        logger.info("listening ...")
        while True:
            try: 
                conn, addr = self._socket.accept()
            except BlockingIOError:
                continue
            handler = TCPHandler('SERVER', conn, self.clients_register)
            thread = threading.Thread(target=handler.run)
            thread.start()
            self.threads.append(thread)
            self.tcp_handlers[addr] = (handler, thread)

    def _cleanup(self, sig, frame):
        self._socket.close()
        for i, th in enumerate(self.threads):
            print(f"thread {i} stopped: {th.stop()}")
        print("SHUTTING DOWN")
        sys.exit(0)
