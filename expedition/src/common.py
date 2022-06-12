from dataclasses import dataclass
from typing import Optional


ORDER_ECHANGE_ID = "ORDER"
CONFIRM_ECHANGE_ID = "CONFIRM"
HOST = "172.17.0.2"


@dataclass 
class Order:
    consumer: str 
    item: str 
    supllier: Optional[str] = None
    process_id: Optional[str] = None