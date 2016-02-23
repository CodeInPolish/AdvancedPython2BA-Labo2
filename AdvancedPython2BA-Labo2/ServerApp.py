import socket
import select
import time 
import pickle

SERVERADDRESS = (socket.gethostname(), 5001)

class EchoServer():
    def __init__(self):
        self.s = socket.socket()
        self.s.bind(SERVERADDRESS)
        self.s.listen(5)
        self.timeout = 0.05
        self.ServerRunning = False
        self.WaitingClients = []
        self.ConnectedClients = {}

    def listening(self):
        self.WaitingClients = select.select([self.s], (), (), self.timeout)[0]

        if len(self.WaitingClients) != 0:
            for client in self.WaitingClients:
                sock, ip = client.accept()
                data = self._receive(sock)
                print(data)
                cmd = data.split(";")
                if cmd[0] == "C2S":
                    self.ConnectedClients[cmd[1]] = sock
        #Récupérer le pseudo puis créer une nouvelle entrée dans le dico. dico[pseudo] = socket
        
    def run(self):
        while True:
            self.listening()
            if len(self.ConnectedClients) != 0:
                print(self.ConnectedClients.keys())
    
    def _receive(self, client):
        data = client.recv(1024)
        return data.decode()

Server = EchoServer()
Server.run()
