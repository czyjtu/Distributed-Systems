import threading
from common import Message, MsgType
from termcolor import colored


class MsgWritter:
    def __init__(self):
        self._lock = threading.Lock()

    def display(self, msg: Message):
        self._lock.acquire()
        if msg.type == MsgType.TEXT:
            print(colored(f"{msg.author}: {msg.text}", 'blue'))
        self._lock.release()
