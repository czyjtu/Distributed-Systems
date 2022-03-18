import threading
from common import Message, MsgType
from termcolor import colored


class MsgWritter:
    def __init__(self):
        self._lock = threading.RLock()

    def display(self, msg: Message):
        if not isinstance(msg,Message):
            return
        self._lock.acquire()
        if msg.type == MsgType.TEXT:
            print(colored(f"{msg.author}: {msg.text}", 'blue'))
        self._lock.release()

    def print(self, msg):
        print(colored(f"{msg.author}: {msg.text}", 'green'))
