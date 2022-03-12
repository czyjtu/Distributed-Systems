from server import Server 
from constants import PORT

def main():
    serv = Server(PORT)
    serv.start()

if __name__ == '__main__':
    main()
    

