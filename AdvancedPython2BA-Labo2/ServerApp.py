import socket
import time 

SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        self.__connectedclients = {"Hadrien" : "192.5.3.1", "Marcin": "192.5.3.2", "Seb" : "192.5.3.3"}
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                data = self._receive(client)
                self.__connectedclients[data] = addr[0]                
                while(1):
                    data = self._receive(client)
                    if (data == "/list"):
                        list = []
                        for pseudo, ip in self.__connectedclients.items():
                            list.append("Pseudo: '{}', IP: '{}' \n".format(pseudo, ip))
                        client.send("".join(list).encode())

            except OSError:
                print('Erreur lors de la réception du message.')
    
    def _receive(self, client):
        data = client.recv(1024)
        return data.decode()

Server = EchoServer()
Server.run()
