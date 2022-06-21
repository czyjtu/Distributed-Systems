from dataclasses import dataclass 
from common.msg_type import MsgType

@dataclass
class Message:
    author: str
    type: MsgType 
    text: str = ''