import pickle
import pika, sys
from pika.exchange_type import ExchangeType

from common import HOST, ORDER_ECHANGE_ID, Order

EXIT_CMD = "--exit"

def main():
    crew_id = sys.argv[1]
    with pika.BlockingConnection(pika.ConnectionParameters(HOST)) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange=ORDER_ECHANGE_ID, exchange_type=ExchangeType.direct)


        while True:
            item_name = input("what do you need?: ")
            if item_name == EXIT_CMD:
                break 
            
            order = Order(crew_id, item_name)
            channel.basic_publish(
                exchange=ORDER_ECHANGE_ID, 
                routing_key=f"{ORDER_ECHANGE_ID}.{item_name}",
                body=pickle.dumps(order)
            )

if __name__ == '__main__':
    main()

