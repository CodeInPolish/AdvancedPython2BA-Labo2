import socket

SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                print(self._receive(client).decode())
                client.close()
            except OSError:
                print('Erreur lors de la réception du message.')
    
    def _receive(self, client):
        data = client.recv(1024)
        return data

Server = EchoServer()
Server.run()
