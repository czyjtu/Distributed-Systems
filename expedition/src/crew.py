import pickle
import pika, sys
from pika.exchange_type import ExchangeType
from threading import Thread
from common import HOST, ORDER_ECHANGE_ID, Order, CONFIRM_ECHANGE_ID

EXIT_CMD = "--exit"

def main():
    crew_id = sys.argv[1]
    with pika.BlockingConnection(pika.ConnectionParameters(HOST)) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange=ORDER_ECHANGE_ID, exchange_type=ExchangeType.direct)
        listen_thread = Thread(target=listen, args=[connection, crew_id])
        listen_thread.start()


        while True:
            item_name = input("what do you need?: ")
            if item_name == EXIT_CMD:
                break 
            items = item_name.split()
            for item in items:
                order = Order(crew_id, item)
                channel.basic_publish(
                    exchange=ORDER_ECHANGE_ID, 
                    routing_key=f"{ORDER_ECHANGE_ID}.{item}",
                    body=pickle.dumps(order)
                )
        listen_thread.join()

def listen(connection, crew_id):
    with pika.BlockingConnection(pika.ConnectionParameters(HOST)) as connection:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=CONFIRM_ECHANGE_ID, 
            exchange_type=ExchangeType.direct
        )
        queue = channel.queue_declare(crew_id)
        channel.queue_bind(
            exchange=CONFIRM_ECHANGE_ID,
            queue=queue.method.queue,
            routing_key=f"{CONFIRM_ECHANGE_ID}.{crew_id}"
        )
        def handler( channel, method, properties, body):
            print(pickle.loads(body))
            channel.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(on_message_callback=handler, queue=queue.method.queue)
        channel.start_consuming()


if __name__ == '__main__':
    main()

