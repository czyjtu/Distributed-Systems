import pika, sys, time, pickle
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel

from common import CONFIRM_ECHANGE_ID, ORDER_ECHANGE_ID, HOST, Order


class Supllier:
    def __init__(self, id: str, channel: BlockingChannel, items: list[str]=None):
        items = items or []

        self._id = id
        self._items = []
        self._channel = channel
        self.declare_exchanges()
        self._orders_count = 0
        for item in items:
            self.register_item(item)

    @property 
    def id(self) -> str:
        return self._id 
    
    @property 
    def items(self) -> list[str]:
        return self._items.copy()
    
    def register_item(self, item: str):
        queue = self._channel.queue_declare(item)
        self._channel.queue_bind(
            exchange=ORDER_ECHANGE_ID,
            queue=queue.method.queue,
            routing_key=f"{ORDER_ECHANGE_ID}.{item}"
        )
        channel.basic_consume(on_message_callback=self.handle_order, queue=queue.method.queue)
        self._items.append(item)

    def declare_exchanges(self):
        self._channel.exchange_declare(
            exchange=ORDER_ECHANGE_ID, 
            exchange_type=ExchangeType.direct
        )
        self._channel.exchange_declare(
            exchange=CONFIRM_ECHANGE_ID, 
            exchange_type=ExchangeType.direct
        )

    def handle_order(self, channel, method, properties, body):
        order = pickle.loads(body)
        print(f"got order from {order.consumer} for {order.item}")

        order.supplier = self._id 
        order.process_id = self._orders_count
        self._orders_count += 1
        self._produce(order.item)
        self._notify(order)
        print("sending ack")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def _produce(self, item: str):
        print(f"producing {item} ...")
        time.sleep(3)

    def _notify(self, order: Order):
        self._channel.basic_publish(
            exchange=CONFIRM_ECHANGE_ID, 
            routing_key=f"{CONFIRM_ECHANGE_ID}.{order.consumer}",
            body=pickle.dumps(order)
        )


if __name__ == '__main__':
    supllier_id = sys.argv[1]
    items = sys.argv[2:]

    with pika.BlockingConnection(pika.ConnectionParameters(HOST)) as connection:
        channel = connection.channel()
        print(items)
        supllier = Supllier(supllier_id, channel, items)
        channel.start_consuming()
