import socket 
import threading 
import logging
import signal 
import sys
from server.tcp_handler import TCPUserHandler
from constants import MSG_LEN 
import pickle 

logger = logging.getLogger('SERVER')
logger.setLevel(logging.DEBUG)


class Server:
    def __init__(self, port):
        self.host =  socket.gethostbyname(socket.gethostname())
        self.address = (self.host, port)
        self.clients_register: dict[str, socket.socket] = dict()
        self.tcp_handlers = dict()
        self.threads = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.udp_addresses = set()
        self.dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dgram_connected = True
        self.udp_thread = threading.Thread(target=self.dgram_connection, args=(self.dgram_connected, ))

        signal.signal(signal.SIGINT, self._cleanup)

    def start(self):
        logger.info("starting ...")
        self._socket.setblocking(False)
        self._socket.bind(self.address)
        self.dgram_socket.bind(self.address)
        self.udp_thread.start()
        self.accept_users()

    def accept_users(self):
        self._socket.listen()
        logger.info("listening ...")
        while True:
            try: 
                conn, addr = self._socket.accept()
            except BlockingIOError:
                continue
            except:
                break
            handler = TCPUserHandler('SERVER', conn, self.clients_register)
            handler.start()
            self.threads.append(handler)
            self.tcp_handlers[addr] = handler

    def dgram_connection(self, connected):
        logger.info("Starting dgram connection")
        while self.dgram_connected:
            data, address = self.dgram_socket.recvfrom(MSG_LEN)
            # msg = data.decode('utf-8')
            logging.info(f"Received UDP message from the {address} {data}")
            msg = pickle.loads(data)
            for client_id, client_socket in self.clients_register.items():
                if client_id == msg.author:
                    continue 
                client_socket.send(pickle.dumps(msg))


    def _cleanup(self, sig, frame):
        for i, th in enumerate(self.threads):
            th.stop()
            print(f"thread {i} stopped")
        self.dgram_connected = False
        self.udp_thread.join(3)
        self._socket.close()
        print("SHUTTING DOWN")
