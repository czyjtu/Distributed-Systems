from client import Client
from constants import PORT
import socket 
import random 

SERVER_IP = socket.gethostbyname(socket.gethostname())

def main():
    client = Client(random.randint(0, 100), SERVER_IP, PORT)
    client.start()

if __name__ == '__main__':
    main()