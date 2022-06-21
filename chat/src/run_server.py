from server import Server 
from constants import PORT
import logging 

def main():
    logging.basicConfig(level=logging.DEBUG)
    serv = Server(PORT)
    serv.start()

if __name__ == '__main__':
    main()
    

