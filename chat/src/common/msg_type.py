from enum import Enum, auto

class MsgType(Enum):
    REGISTER = auto()
    LIST = auto()
    ACK = auto()
    NACK = auto()
    TEXT = auto()
    DISCONNECT = auto()